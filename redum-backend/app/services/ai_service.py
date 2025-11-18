from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from google import generativeai as genai
from google.api_core import exceptions as google_exceptions

from app.core.config import get_settings
from app.domain.schemas.task import TaskRead


logger = logging.getLogger(__name__)


@dataclass
class TaskSuggestion:
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[str] = None


class _EmbeddingFunctionWrapper(EmbeddingFunction[Documents]):
    """Adapter to plug sentence-transformers into ChromaDB."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self._function = SentenceTransformerEmbeddingFunction(model_name=model_name)

    def __call__(self, input: Documents) -> Embeddings:  # noqa: A003 - Chroma signature
        return self._function(input)


class RAGService:
    """Service responsible for knowledge ingestion and metadata suggestions."""

    COLLECTION_NAME = "tasks"

    def __init__(
        self,
        *,
        settings=None,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        self.settings = settings or get_settings()
        if not self.settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY must be configured to use RAGService")

        genai.configure(api_key=self.settings.GEMINI_API_KEY)

        storage_path = Path(self.settings.CHROMA_DB_PATH).expanduser().resolve()
        storage_path.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(storage_path))
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            embedding_function=_EmbeddingFunctionWrapper(model_name=embedding_model),
        )
        try:
            self._gemini_model = genai.GenerativeModel(self.settings.GEMINI_MODEL)
        except google_exceptions.GoogleAPIError as exc:
            raise ValueError(
                f"Gemini model '{self.settings.GEMINI_MODEL}' is not available: {exc}"
            ) from exc
        except Exception as exc:  # pragma: no cover - defensive fallback
            raise ValueError(
                f"Failed to initialize Gemini model '{self.settings.GEMINI_MODEL}'"
            ) from exc

    def add_task_to_kb(self, task: TaskRead) -> None:
        """Embed and upsert task data into Chroma."""

        document = self._build_task_document(task)
        metadata = {
            "task_id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "priority": task.priority,
            "status": task.status,
        }

        self._collection.upsert(
            ids=[str(task.id)],
            documents=[document],
            metadatas=[metadata],
        )

    def suggest_metadata(
        self,
        *,
        user_id: int,
        description: str,
        title: Optional[str] = None,
        priority: Optional[int] = None,
        status: Optional[str] = None,
    ) -> TaskSuggestion:
        """Generate metadata suggestions using local embeddings and Gemini."""

        query = self._build_query_prompt(description=description, title=title)
        try:
            results = self._collection.query(
                query_texts=[query],
                where={"user_id": user_id},
                n_results=5,
            )
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.warning("Chroma query failed: %s", exc)
            results = {"documents": [[]]}

        context_snippets = self._format_context(results)
        llm_prompt = self._build_llm_prompt(
            context=context_snippets,
            description=description,
            title=title,
            priority=priority,
            status=status,
        )

        try:
            response = self._gemini_model.generate_content(llm_prompt)
        except google_exceptions.GoogleAPIError as exc:
            logger.warning("Gemini generation failed: %s", exc)
            raise ValueError(
                "Gemini service is unavailable or the model does not support this request"
            ) from exc
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.warning("Gemini generation failed: %s", exc)
            raise ValueError("Gemini service encountered an unexpected error") from exc

        output = self._extract_response_text(response)
        parsed = self._parse_llm_output(output)

        suggestion = TaskSuggestion(
            title=parsed.get("title"),
            description=parsed.get("description"),
            priority=parsed.get("priority"),
            status=parsed.get("status"),
        )

        return suggestion

    def remove_task_from_kb(self, task_id: int) -> None:
        if not task_id:
            return
        try:
            self._collection.delete(ids=[str(task_id)])
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.warning("Failed to remove task %s from knowledge base: %s", task_id, exc)

    def _build_task_document(self, task: TaskRead) -> str:
        segments = [f"Title: {task.title}"]
        if task.description:
            segments.append(f"Description: {task.description}")
        if task.priority is not None:
            segments.append(f"Priority: {task.priority}")
        if task.status:
            segments.append(f"Status: {task.status}")
        return "\n".join(segments)

    def _build_query_prompt(self, *, description: str, title: Optional[str]) -> str:
        if title:
            return f"Title: {title}\nDescription: {description}"
        return description

    def _format_context(self, results: Dict[str, Any]) -> str:
        documents: List[str] = results.get("documents", [[]])[0]
        if not documents:
            return ""
        return "\n---\n".join(documents)

    def _build_llm_prompt(
        self,
        *,
        context: str,
        description: str,
        title: Optional[str],
        priority: Optional[int],
        status: Optional[str],
    ) -> str:
        instructions = [
            "You are a helpful assistant that suggests task metadata.",
            "Only fill empty fields; return JSON with keys: title, description, priority, status.",
            "If a value should not change, respond with null for that field.",
            "Priority is an integer 1 (low), 2 (medium), or 3 (high).",
            "Status must be one of: todo, in_progress, done.",
        ]
        base = {
            "title": title,
            "description": description,
            "priority": priority,
            "status": status,
        }
        prompt = "\n".join(instructions)
        if context:
            prompt += f"\n\nRelevant existing tasks:\n{context}"
        prompt += "\n\nCurrent task data (JSON):\n"
        prompt += str(base)
        prompt += "\n\nRespond with JSON only."
        return prompt

    def _extract_response_text(self, response: Any) -> str:
        if not getattr(response, "candidates", None):
            return ""
        for candidate in response.candidates:
            content = getattr(candidate, "content", None)
            if not content:
                continue
            parts = getattr(content, "parts", [])
            texts = [getattr(part, "text", "") for part in parts if getattr(part, "text", "")]
            if texts:
                return "\n".join(texts)
        return ""

    def _parse_llm_output(self, output: str) -> Dict[str, Any]:
        try:
            json_start = output.find("{")
            json_end = output.rfind("}") + 1
            if json_start == -1 or json_end == 0:
                return {}
            json_str = output[json_start:json_end]
        except Exception:
            return {}

        import json

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            return {}

        priority = data.get("priority")
        if isinstance(priority, str):
            if priority.isdigit():
                data["priority"] = int(priority)
            else:
                data["priority"] = None

        status = data.get("status")
        allowed_status = {"todo", "in_progress", "done"}
        if isinstance(status, str) and status not in allowed_status:
            data["status"] = None

        return data
