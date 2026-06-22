"use client";

import * as React from "react";
import { AuthContextType, AuthState, LoginCredentials } from "@/types/auth";
import { authService } from "@/services/auth";

const AuthContext = React.createContext<AuthContextType | undefined>(undefined);

const initialState: AuthState = {
  user: null,
  status: "loading", // Initialize as loading to prevent flicker during mount-and-check lifecycle.
  error: null,
};

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = React.useState<AuthState>(initialState);

  // Phase 9E: Safely restore session from localStorage on mount
  React.useEffect(() => {
    if (state.status === "loading") {
      try {
        const storedToken = localStorage.getItem("agroguard_access_token");
        const storedUserJSON = localStorage.getItem("agroguard_user");
        
        if (storedToken && storedUserJSON) {
          const parsedUser = JSON.parse(storedUserJSON);
          setState({ user: parsedUser, status: "authenticated", error: null });
        } else {
          setState({ user: null, status: "unauthenticated", error: null });
        }
      } catch (err) {
        // Corrupted JSON or storage failure: wipe clean and fail securely
        localStorage.removeItem("agroguard_access_token");
        localStorage.removeItem("agroguard_refresh_token");
        localStorage.removeItem("agroguard_user");
        setState({ user: null, status: "unauthenticated", error: null });
      }
    }
  }, [state.status]);

  // Future implementation: Fetch JWT from secure cookies or local storage,
  // validate with backend API, and populate user state.

  const login = async (credentials: LoginCredentials) => {
    // AuthContext owns login orchestration and persistence.
    const response = await authService.login(credentials);
    
    // 1. Persist to storage
    localStorage.setItem("agroguard_access_token", response.access_token);
    localStorage.setItem("agroguard_refresh_token", response.refresh_token);
    localStorage.setItem("agroguard_user", JSON.stringify(response.user));
    
    // 2. Update React State
    setState({ user: response.user, status: "authenticated", error: null });
  };

  const logout = async () => {
    // 1. Retrieve refresh token before wiping
    const refreshToken = localStorage.getItem("agroguard_refresh_token");
    
    // 2. Synchronously wipe local session to prevent trap if backend fails
    localStorage.removeItem("agroguard_access_token");
    localStorage.removeItem("agroguard_refresh_token");
    localStorage.removeItem("agroguard_user");
    setState({ user: null, status: "unauthenticated", error: null });
    
    // 3. Fire backend logout asynchronously
    if (refreshToken) {
      try {
        await authService.logout(refreshToken);
      } catch (error) {
        console.error("Backend logout failed, but local session was destroyed.", error);
      }
    }
  };

  const updateUser = (data: Partial<import("@/types/auth").User>) => {
    setState((prev) => ({
      ...prev,
      user: prev.user ? { ...prev.user, ...data } : null,
    }));
  };

  const value = React.useMemo(
    () => ({
      ...state,
      login,
      logout,
      updateUser,
    }),
    [state]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = React.useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
