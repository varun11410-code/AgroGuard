export type AuthStatus = "idle" | "loading" | "authenticated" | "unauthenticated";

export type UserRole = "admin" | "farmer" | "researcher";

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  language?: string;
  preferred_budget_tier?: string;
  created_at?: string;
}

export interface AuthState {
  user: User | null;
  status: AuthStatus;
  error: string | null;
}

export interface AuthContextType extends AuthState {
  login: () => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (data: Partial<User>) => void;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

export interface RegisterResponse {
  success: boolean;
  data: User;
}

export interface ApiErrorResponse {
  success: boolean;
  message?: string;
  errors?: Array<{ field: string; message: string }>;
}
