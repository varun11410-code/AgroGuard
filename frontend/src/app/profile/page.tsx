"use client";

import React from "react";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { useAuth } from "@/contexts/AuthContext";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function ProfilePage() {
  const { user } = useAuth();

  // Helper to format role
  const formatRole = (role?: string) => {
    if (!role) return "Unknown";
    return role.charAt(0).toUpperCase() + role.slice(1).toLowerCase();
  };

  // Helper to format created_at
  const formatMemberSince = (isoDate?: string) => {
    if (!isoDate) return "Unknown";
    try {
      const date = new Date(isoDate);
      return `Member since ${date.toLocaleDateString(undefined, { month: 'long', year: 'numeric' })}`;
    } catch {
      return "Unknown";
    }
  };

  // Helper to format language
  const formatLanguage = (lang?: string) => {
    if (!lang) return "Not configured";
    if (lang.toLowerCase() === "en") return "English";
    if (lang.toLowerCase() === "hi") return "Hindi";
    return lang;
  };

  // Helper to format budget tier
  const formatBudget = (budget?: string) => {
    if (!budget) return "Not selected";
    return budget.charAt(0).toUpperCase() + budget.slice(1).toLowerCase();
  };

  return (
    <ProtectedRoute>
      <div className="max-w-4xl mx-auto py-12 px-6">
        <h1 className="text-3xl font-bold tracking-tight font-heading mb-8">
          User Profile
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Identity Card */}
          <Card>
            <CardHeader>
              <CardTitle>Account Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-xs tracking-widest uppercase font-mono text-muted-foreground mb-1">
                  Name
                </p>
                <p className="font-sans text-lg">{user?.name || "Unknown"}</p>
              </div>
              <div>
                <p className="text-xs tracking-widest uppercase font-mono text-muted-foreground mb-1">
                  Email
                </p>
                <p className="font-sans text-lg">{user?.email || "Unknown"}</p>
              </div>
              <div>
                <p className="text-xs tracking-widest uppercase font-mono text-muted-foreground mb-1">
                  Role
                </p>
                <p className="font-sans text-lg">{formatRole(user?.role)}</p>
              </div>
              <div>
                <p className="text-xs tracking-widest uppercase font-mono text-muted-foreground mb-1">
                  Joined
                </p>
                <p className="font-sans text-lg">{formatMemberSince(user?.created_at)}</p>
              </div>
            </CardContent>
          </Card>

          {/* Preferences Card */}
          <Card>
            <CardHeader>
              <CardTitle>Preferences</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-xs tracking-widest uppercase font-mono text-muted-foreground mb-1">
                  Language
                </p>
                <p className="font-sans text-lg">{formatLanguage(user?.language)}</p>
              </div>
              <div>
                <p className="text-xs tracking-widest uppercase font-mono text-muted-foreground mb-1">
                  Preferred Budget Tier
                </p>
                <p className="font-sans text-lg">{formatBudget(user?.preferred_budget_tier)}</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </ProtectedRoute>
  );
}
