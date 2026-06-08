"use client";

import * as React from "react";
import { AuthContextType, AuthState } from "@/types/auth";

const AuthContext = React.createContext<AuthContextType | undefined>(undefined);

const initialState: AuthState = {
  user: null,
  status: "unauthenticated", // Mock state. Change to "authenticated" locally to test protected routes without a backend.
  error: null,
};

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = React.useState<AuthState>(initialState);

  // Future implementation: Fetch JWT from secure cookies or local storage,
  // validate with backend API, and populate user state.

  const login = async () => {
    console.log("Mock login triggered. Future JWT retrieval and backend auth goes here.");
    // Example of future state update:
    // setState({ user: mockUser, status: "authenticated", error: null });
  };

  const logout = async () => {
    console.log("Mock logout triggered. Future JWT destruction and cleanup goes here.");
    setState({ user: null, status: "unauthenticated", error: null });
  };

  const value = React.useMemo(
    () => ({
      ...state,
      login,
      logout,
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
