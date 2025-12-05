import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, catchError, of } from 'rxjs';
import { ChatMessage, ChatRequest, ChatResponse } from '../models/chat.model';
import { environment } from '../../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class ChatService {
    private readonly http = inject(HttpClient);
    private readonly API_URL = environment.apiUrl;

    // Signal-based state for chat
    readonly messages = signal<ChatMessage[]>([]);
    readonly isLoading = signal<boolean>(false);
    readonly error = signal<string | null>(null);

    // Computed signal for checking if chat is empty
    readonly isEmpty = computed(() => this.messages().length === 0);

    /**
     * Send a message to the AI chat service.
     */
    sendMessage(message: string): Observable<ChatResponse> {
        this.isLoading.set(true);
        this.error.set(null);

        // Add user message to local state immediately for better UX
        this.messages.update(msgs => [...msgs, { role: 'user' as const, content: message }]);

        const request: ChatRequest = {
            message,
            history: this.messages().slice(0, -1) // Exclude the message we just added
        };

        return this.http.post<ChatResponse>(`${this.API_URL}/chat/`, request).pipe(
            tap(response => {
                // Add assistant response to messages
                this.messages.update(msgs => [...msgs, { role: 'assistant' as const, content: response.response }]);
                this.isLoading.set(false);
            }),
            catchError(err => {
                this.error.set(err.error?.detail || 'Failed to get response from AI');
                this.isLoading.set(false);
                // Remove the user message if the request failed
                this.messages.update(msgs => msgs.slice(0, -1));
                throw err;
            })
        );
    }

    /**
     * Clear the chat history.
     */
    clearHistory(): void {
        this.messages.set([]);
        this.error.set(null);
    }
}
