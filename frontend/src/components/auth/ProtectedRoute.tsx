"use client";

import * as React from "react";
import { useAuth } from "@/contexts/AuthContext";
import { Loading } from "@/components/ui/loading";
import { UserRole } from "@/types/auth";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRoles?: UserRole[];
}

export function ProtectedRoute({ children, requiredRoles }: ProtectedRouteProps) {
  const { status, user } = useAuth();

  // Show loading indicator while authentication status is unresolved
  if (status === "loading" || status === "idle") {
    return (
      <div className="min-h-[50vh] flex items-center justify-center">
        <Loading variant="pulse" size="lg" />
      </div>
    );
  }

  if (status === "unauthenticated") {
    return (
      <div className="min-h-[50vh] flex flex-col items-center justify-center gap-4 text-center p-6">
        <h2 className="font-heading text-3xl font-bold text-foreground">
          Authentication Required
        </h2>
        <p className="text-muted-foreground font-sans max-w-md">
          Please sign in to access this page.
        </p>
      </div>
    );
  }

  // Handle Role-Based Access Control (RBAC) if roles are strictly provided
  if (requiredRoles && requiredRoles.length > 0) {
    const hasRequiredRole = user?.role && requiredRoles.includes(user.role);
    if (!hasRequiredRole) {
      return (
        <div className="min-h-[50vh] flex flex-col items-center justify-center gap-4 text-center p-6">
          <h2 className="font-heading text-3xl font-bold text-foreground">Access Denied</h2>
          <p className="text-muted-foreground font-sans max-w-md">
            You do not have the required permissions to view this page. Please contact an administrator if you believe this is an error.
          </p>
        </div>
      );
    }
  }

  // Authenticated and Authorized
  return <>{children}</>;
}
