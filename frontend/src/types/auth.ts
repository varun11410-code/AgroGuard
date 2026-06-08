export type AuthStatus = "idle" | "loading" | "authenticated" | "unauthenticated";

export type UserRole = "admin" | "farmer" | "researcher";

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
}

export interface AuthState {
  user: User | null;
  status: AuthStatus;
  error: string | null;
}

export interface AuthContextType extends AuthState {
  login: () => Promise<void>;
  logout: () => Promise<void>;
}
