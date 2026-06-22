"use client";

import React, { useState, useEffect } from "react";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { useAuth } from "@/contexts/AuthContext";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { authService } from "@/services/auth";

export default function ProfilePage() {
  const { user, updateUser } = useAuth();
  
  const [language, setLanguage] = useState(user?.language || "en");
  const [budget, setBudget] = useState(user?.preferred_budget_tier || "STANDARD");
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState<{ text: string, type: "success" | "error" } | null>(null);

  useEffect(() => {
    if (user?.language) {
      setLanguage(user.language);
    }
    if (user?.preferred_budget_tier) {
      setBudget(user.preferred_budget_tier);
    }
  }, [user?.language, user?.preferred_budget_tier]);

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

  // Helper to format budget tier
  const formatBudget = (budget?: string) => {
    if (!budget) return "Not selected";
    return budget.charAt(0).toUpperCase() + budget.slice(1).toLowerCase();
  };

  const handleSave = async () => {
    setIsSaving(true);
    setMessage(null);
    try {
      const result = await authService.updatePreferences({ 
        language, 
        preferred_budget_tier: budget 
      });
      if (result.success && result.data) {
        updateUser(result.data);
        setMessage({ text: "Preferences saved successfully.", type: "success" });
      } else {
        setMessage({ text: "Failed to save preferences.", type: "error" });
      }
    } catch (error) {
      console.error(error);
      setMessage({ text: "An error occurred while saving.", type: "error" });
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <ProtectedRoute>
      <main className="max-w-4xl mx-auto pt-[140px] pb-[80px] px-6 min-h-screen relative">
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
              {message && (
                <div className={`p-3 text-sm rounded-md ${message.type === 'success' ? 'bg-green-100 text-green-800 border border-green-200' : 'bg-red-100 text-red-800 border border-red-200'}`}>
                  {message.text}
                </div>
              )}
              
              <div>
                <p className="text-xs tracking-widest uppercase font-mono text-muted-foreground mb-1">
                  Language
                </p>
                <select 
                  value={language} 
                  onChange={(e) => setLanguage(e.target.value)}
                  className="w-full mt-1 p-2 bg-background border border-input rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                >
                  <option value="en">English</option>
                  <option value="hi">Hindi</option>
                </select>
              </div>
              <div>
                <p className="text-xs tracking-widest uppercase font-mono text-muted-foreground mb-1">
                  Preferred Budget Tier
                </p>
                <select 
                  value={budget} 
                  onChange={(e) => setBudget(e.target.value)}
                  className="w-full mt-1 p-2 bg-background border border-input rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                >
                  <option value="BUDGET">Budget</option>
                  <option value="STANDARD">Standard</option>
                  <option value="PREMIUM">Premium</option>
                </select>
              </div>
              
              <div className="pt-4">
                <Button 
                  onClick={handleSave} 
                  disabled={isSaving || (language === user?.language && budget === user?.preferred_budget_tier)}
                  className="w-full"
                >
                  {isSaving ? "Saving..." : "Save Settings"}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </ProtectedRoute>
  );
}
