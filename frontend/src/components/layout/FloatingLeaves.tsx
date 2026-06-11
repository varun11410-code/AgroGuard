"use client";

import { useEffect, useRef } from "react";

const LEAF_COUNT = 18;
const LEAF_EMOJIS = ["🍃", "🌿", "🍀", "☘️", "🌱"] as const;

const LEAF_KEYFRAMES = `
@keyframes leafFall {
  0%   {
    transform: translateY(-80px) translateX(0) rotate(0deg);
    opacity: 0;
  }
  5%   { opacity: 0.6; }
  90%  { opacity: 0.3; }
  100% {
    transform: translateY(110vh) translateX(120px) rotate(720deg);
    opacity: 0;
  }
}
`;

export default function FloatingLeaves() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const STYLE_ID = "agro-leaf-keyframes";
    if (!document.getElementById(STYLE_ID)) {
      const style = document.createElement("style");
      style.id = STYLE_ID;
      style.textContent = LEAF_KEYFRAMES;
      document.head.appendChild(style);
    }

    const container = containerRef.current;
    if (!container) return;

    const leaves: HTMLDivElement[] = [];

    for (let i = 0; i < LEAF_COUNT; i++) {
      const leaf = document.createElement("div");
      leaf.textContent = LEAF_EMOJIS[Math.floor(Math.random() * LEAF_EMOJIS.length)];

      leaf.style.position        = "fixed";
      leaf.style.pointerEvents   = "none";
      leaf.style.zIndex          = "-8";
      leaf.style.filter          = "blur(0.5px)";
      leaf.style.userSelect      = "none";
      leaf.style.animationName   = "leafFall";
      leaf.style.animationTimingFunction = "linear";
      leaf.style.animationIterationCount = "infinite";

      leaf.style.left            = `${Math.random() * 100}vw`;
      leaf.style.fontSize        = `${1 + Math.random() * 1.4}rem`;
      leaf.style.animationDuration = `${18 + Math.random() * 22}s`;
      leaf.style.animationDelay  = `${Math.random() * 20}s`;
      leaf.style.opacity         = "0";

      container.appendChild(leaf);
      leaves.push(leaf);
    }

    return () => {
      leaves.forEach((leaf) => leaf.remove());
    };
  }, []);

  return (
    <div
      ref={containerRef}
      aria-hidden="true"
      style={{ position: "fixed", inset: 0, pointerEvents: "none", zIndex: -8 }}
    />
  );
}
