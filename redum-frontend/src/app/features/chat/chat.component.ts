import { Component, inject, signal, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ChatService } from '../../core/services/chat.service';

@Component({
    selector: 'app-chat',
    standalone: true,
    imports: [
        CommonModule,
        FormsModule,
        MatCardModule,
        MatButtonModule,
        MatIconModule,
        MatInputModule,
        MatFormFieldModule,
        MatProgressSpinnerModule
    ],
    templateUrl: './chat.component.html',
    styleUrls: ['./chat.component.scss']
})
export class ChatComponent implements AfterViewChecked {
    private readonly chatService = inject(ChatService);

    @ViewChild('messageContainer') private messageContainer!: ElementRef;

    readonly messages = this.chatService.messages;
    readonly isLoading = this.chatService.isLoading;
    readonly error = this.chatService.error;
    readonly isEmpty = this.chatService.isEmpty;

    currentMessage = signal('');
    private shouldScroll = false;

    ngAfterViewChecked(): void {
        if (this.shouldScroll) {
            this.scrollToBottom();
            this.shouldScroll = false;
        }
    }

    sendMessage(): void {
        const message = this.currentMessage().trim();
        if (!message || this.isLoading()) {
            return;
        }

        this.currentMessage.set('');
        this.shouldScroll = true;

        this.chatService.sendMessage(message).subscribe({
            next: () => {
                this.shouldScroll = true;
            },
            error: () => {
                // Error is handled by service
            }
        });
    }

    clearChat(): void {
        this.chatService.clearHistory();
    }

    onKeydown(event: KeyboardEvent): void {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    }

    private scrollToBottom(): void {
        if (this.messageContainer) {
            const container = this.messageContainer.nativeElement;
            container.scrollTop = container.scrollHeight;
        }
    }
}
