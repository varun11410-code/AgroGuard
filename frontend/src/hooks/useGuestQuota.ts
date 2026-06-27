import { useState, useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { GUEST_CONFIG } from "@/constants/guest";

export interface GuestQuotaState {
  used: number;
  version: number;
}

export interface UseGuestQuotaResult {
  used: number;
  remaining: number;
  isExhausted: boolean;
  incrementQuota: () => void;
}

const DEFAULT_STATE: GuestQuotaState = {
  used: 0,
  version: 1,
};

export function useGuestQuota(): UseGuestQuotaResult {
  const { status } = useAuth();
  const [quota, setQuota] = useState<GuestQuotaState>(DEFAULT_STATE);

  // Initialize from localStorage on mount (client-side only)
  useEffect(() => {
    try {
      const stored = localStorage.getItem(GUEST_CONFIG.STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as GuestQuotaState;
        // Basic migration/validation check
        if (parsed.version === 1 && typeof parsed.used === "number") {
          setQuota(parsed);
        } else {
          // Future versions can migrate here
          setQuota(DEFAULT_STATE);
          localStorage.setItem(GUEST_CONFIG.STORAGE_KEY, JSON.stringify(DEFAULT_STATE));
        }
      }
    } catch (e) {
      console.warn("Failed to parse guest quota from localStorage", e);
      // Reset if corrupted
      setQuota(DEFAULT_STATE);
    }
  }, []);

  const incrementQuota = () => {
    // Authenticated users never consume guest quota
    if (status === "authenticated") return;

    setQuota((prev) => {
      const newState = {
        ...prev,
        used: prev.used + 1,
      };
      try {
        localStorage.setItem(GUEST_CONFIG.STORAGE_KEY, JSON.stringify(newState));
      } catch (e) {
        console.warn("Failed to write guest quota to localStorage", e);
      }
      return newState;
    });
  };

  // If authenticated, mock unlimited scans.
  if (status === "authenticated") {
    return {
      used: 0,
      remaining: Infinity,
      isExhausted: false,
      incrementQuota: () => {}, // No-op
    };
  }

  const remaining = Math.max(0, GUEST_CONFIG.MAX_FREE_SCANS - quota.used);
  
  return {
    used: quota.used,
    remaining,
    isExhausted: remaining === 0,
    incrementQuota,
  };
}
