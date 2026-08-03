import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

import { Observable } from 'rxjs';

import { ChatResponse } from '../models/chat-response.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private http = inject(HttpClient);

  private readonly api =
    environment.apiUrl;

  health(): Observable<any> {
    return this.http.get(
      `${this.api}/health`
    );
  }

  chat(message: string) {
    return this.http.post<ChatResponse>(
      `${this.api}/chat`,
      { message }
    );
  }

  uploadDocument(file: File) {

    const formData =
      new FormData();

    formData.append(
      'file',
      file
    );

    return this.http.post(
      `${this.api}/upload/document`,
      formData
    );
  }

  uploadCsv(file: File) {

    const formData =
      new FormData();

    formData.append(
      'file',
      file
    );

    return this.http.post(
      `${this.api}/upload/csv`,
      formData
    );
  }
}
