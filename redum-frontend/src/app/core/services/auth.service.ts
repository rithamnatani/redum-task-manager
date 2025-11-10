import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { Router } from '@angular/router';
import { 
  LoginRequest, 
  RegisterRequest, 
  AuthResponse, 
  User 
} from '../models/user.model';
import { TokenStorageService } from './token-storage.service';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly tokenStorage = inject(TokenStorageService);
  private readonly router = inject(Router);

  private readonly API_URL = environment.apiUrl;

  register(data: RegisterRequest): Observable<User> {
    return this.http.post<User>(`${this.API_URL}/auth/register`, data);
  }

  login(credentials: LoginRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.API_URL}/auth/token`, credentials).pipe(
      tap(response => {
        this.tokenStorage.saveToken(response.access_token);
      })
    );
  }

  logout(): void {
    this.tokenStorage.removeToken();
    this.router.navigate(['/login']);
  }

  isAuthenticated(): boolean {
    return this.tokenStorage.hasToken();
  }
}
