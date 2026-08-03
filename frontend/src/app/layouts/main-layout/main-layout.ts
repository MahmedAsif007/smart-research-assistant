import { Component, inject, OnInit, signal, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { ApiService } from '../../core/services/api';
import { Button } from '../../shared/components/button/button';
import { ChatMessage } from '../../features/chat/chat.model';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    Button
  ],
  templateUrl: './main-layout.html',
  styleUrl: './main-layout.scss'
})
export class MainLayout implements OnInit {

  private api = inject(ApiService);

  backendStatus = signal('Checking...');

  model = signal('');

  messages = signal<ChatMessage[]>([
    {
      role: 'assistant',
      content: 'Hello! How can I help you today?'
    }
  ]);

  message = '';

  sending = signal(false);

  @ViewChild('pdfInput')
  pdfInput!: ElementRef<HTMLInputElement>;

  @ViewChild('csvInput')
  csvInput!: ElementRef<HTMLInputElement>;

  uploadingPdf = signal(false);

  uploadingCsv = signal(false);

  uploadedPdfName = signal('');

  uploadedCsvName = signal('');

  csvUploadMessage = signal('');

  ngOnInit(): void {

    this.api
      .health()
      .subscribe({
        next: (response) => {

          this.backendStatus
            .set('Connected');

          this.model
            .set(response.model);

        },

        error: () => {

          this.backendStatus
            .set('Disconnected');
        }
      });
  }

  sendMessage(): void {

    const text =
      this.message.trim();

    if (!text) {
      return;
    }

    this.messages.update(messages => [
      ...messages,
      {
        role: 'user',
        content: text
      }
    ]);

    this.sending.set(true);

    this.messages.update(messages => [
        ...messages,
        {
          role: 'assistant',
          content: '__thinking__'
        }
      ]);

    this.api
      .chat(text)
      .subscribe({

        next: (response) => {

          // this.messages.update(messages => [
          //   ...messages,
          //   {
          //     role: 'assistant',
          //     content: response.answer
          //   }
          // ]);
          this.messages.update(messages => {

          const updated = [...messages];

          updated[updated.length - 1] = {
            role: 'assistant',
            content: response.answer
          };

          return updated;
        });

          this.sending.set(false);
        },

        error: (error) => {

          console.error(error);

          // this.messages.update(messages => [
          //   ...messages,
          //   {
          //     role: 'assistant',
          //     content: 'Sorry, something went wrong while processing your request.'
          //   }
          // ]);
          this.messages.update(messages => {

        const updated = [...messages];

        updated[updated.length - 1] = {
          role: 'assistant',
          content: 'Sorry, something went wrong while processing your request.'
        };

        return updated;
      });

          this.sending.set(false);
        }
      });

    this.message = '';
  }

  openPdfUpload(): void {
    this.pdfInput.nativeElement.click();
  }

  onPdfSelected(event: Event): void {
      const file =
        (event.target as HTMLInputElement)
          .files?.[0];

      if (!file) {
        return;
      }

      this.uploadingPdf.set(true);

      this.api
        .uploadDocument(file)
        .subscribe({

          next: () => {

            this.uploadedPdfName.set(
              file.name
            );

            this.uploadingPdf.set(false);
          },

          error: (error) => {

            console.error(error);

            this.uploadingPdf.set(false);
          }

        });
    }

  openCsvUpload(): void {
    this.csvInput.nativeElement.click();
  }

  onCsvSelected(event: Event): void {

    const file =
      (event.target as HTMLInputElement)
        .files?.[0];

    if (!file) {
      return;
    }

    this.uploadingCsv.set(true);

    this.api
      .uploadCsv(file)
      .subscribe({

        next: (response:any) => {

          this.uploadedCsvName.set(
            file.name
          );

          this.csvUploadMessage.set( response?.message || 'CSV uploaded successfully' );

          this.uploadingCsv.set(false);
          setTimeout(() => {
            this.csvUploadMessage.set('');
          }, 5000);
        },

        error: (error) => {

          console.error(error);

          this.uploadingCsv.set(false);

          setTimeout(() => {
            this.csvUploadMessage.set('');
          }, 5000);
        }

      });
  }

  clearChat(): void {

  this.messages.set([
    {
      role: 'assistant',
      content: 'Hello! How can I help you today?'
    }
  ]);

}

}