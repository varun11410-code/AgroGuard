export function normalizeConfidence(confidence?: number | null): number | null {
  if (confidence === undefined || confidence === null || Number.isNaN(confidence)) {
    return null;
  }
  const percentage = confidence <= 1 ? confidence * 100 : confidence;
  return Math.min(Math.max(percentage, 0), 100);
}

export function getConfidenceTheme(confidence?: number | null) {
  const normalized = normalizeConfidence(confidence);
  if (normalized === null) {
    return {
      text: "text-white/60",
      bar: "from-white/20 to-white/40",
      value: "bg-white/40"
    };
  }
  
  if (normalized >= 80) {
    return {
      text: "from-[#22c55e] to-[#86efac]", // Green
      bar: "from-[#166534] to-[#22c55e]",
      value: "bg-[#22c55e]"
    };
  } else if (normalized >= 50) {
    return {
      text: "from-yellow-400 to-yellow-200", // Yellow
      bar: "from-yellow-600 to-yellow-400",
      value: "bg-yellow-400"
    };
  } else {
    return {
      text: "from-red-500 to-red-300", // Red
      bar: "from-red-700 to-red-500",
      value: "bg-red-500"
    };
  }
}

export function getRiskTheme(riskLevel?: string | null) {
  if (!riskLevel || riskLevel.toLowerCase() === "unknown") {
    return {
      text: "text-white/60",
      badge: "bg-white/10 border-white/20 text-white/60",
      message: "Risk level cannot be determined."
    };
  }
  
  const level = riskLevel.toLowerCase();
  
  if (level === "low") {
    return {
      text: "text-[#22c55e]", // Green
      badge: "bg-[#22c55e]/10 border-[#22c55e]/20 text-[#22c55e]",
      message: "Monitor normally"
    };
  } else if (level === "medium") {
    return {
      text: "text-yellow-500", // Yellow
      badge: "bg-yellow-500/10 border-yellow-500/20 text-yellow-500",
      message: "Treatment recommended"
    };
  } else if (level === "high") {
    return {
      text: "text-red-500", // Red
      badge: "bg-red-500/10 border-red-500/20 text-red-500",
      message: "Immediate treatment recommended"
    };
  }
  
  return {
    text: "text-white/60",
    badge: "bg-white/10 border-white/20 text-white/60",
    message: "Unknown risk level"
  };
}
