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

  // Phase 9D: Immediately resolve "loading" to "unauthenticated" on mount.
  // Phase 9E will replace this with actual token validation.
  React.useEffect(() => {
    if (state.status === "loading") {
      setState((prev) => ({ ...prev, status: "unauthenticated" }));
    }
  }, []);

  // Future implementation: Fetch JWT from secure cookies or local storage,
  // validate with backend API, and populate user state.

  const login = async (credentials: LoginCredentials) => {
    // AuthContext owns login orchestration. The page simply awaits this function.
    const response = await authService.login(credentials);
    setState({ user: response.user, status: "authenticated", error: null });
  };

  const logout = async () => {
    console.log("Mock logout triggered. Future JWT destruction and cleanup goes here.");
    setState({ user: null, status: "unauthenticated", error: null });
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
