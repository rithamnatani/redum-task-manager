from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, Enum
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base
import enum


class TaskStatus(enum.Enum):
    """Task status enumeration for Kanban board"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    priority = Column(Integer, nullable=True)
    status = Column(
        Enum(
            TaskStatus,
            values_callable=lambda enum: [member.value for member in enum],
            name="taskstatus",
        ),
        nullable=False,
        default=TaskStatus.TODO.value,
        server_default=TaskStatus.TODO.value,
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="tasks")
