"use client";

/**
 * FloatingLeaves.tsx
 *
 * Exact port of the floating leaf system from agroguard-v3.html.
 *
 * Original source values (verbatim from v3):
 * ─────────────────────────────────────────────────────────────
 * CSS .leaf {
 *   position: fixed;
 *   pointer-events: none;
 *   z-index: -8;
 *   font-size: 1.6rem;          ← base, overridden per-leaf below
 *   animation: leafFall linear infinite;
 *   opacity: 0;
 *   filter: blur(0.5px);
 * }
 *
 * @keyframes leafFall {
 *   0%   { transform: translateY(-80px) translateX(0)    rotate(0deg);   opacity: 0;   }
 *   5%   {                                                                opacity: 0.6; }
 *   90%  {                                                                opacity: 0.3; }
 *   100% { transform: translateY(110vh) translateX(120px) rotate(720deg); opacity: 0;   }
 * }
 *
 * JS loop (18 leaves):
 *   leafEmojis = ['🍃','🌿','🍀','☘️','🌱']
 *   left:              Math.random() * 100vw
 *   font-size:         1 + Math.random() * 1.4  rem   (range: 1rem – 2.4rem)
 *   animation-duration: 18 + Math.random() * 22  s    (range: 18s – 40s)
 *   animation-delay:    Math.random() * 20        s    (range: 0s  – 20s)
 *   opacity: 0  (animation drives it)
 * ─────────────────────────────────────────────────────────────
 *
 * Why a React component instead of a bare script:
 *   • useEffect runs only on the client, matching the original script's timing
 *   • Cleanup function removes leaves on HMR / unmount — no duplicates
 *   • A dedicated container div is used instead of document.body so React
 *     owns the DOM node and SSR produces no hydration mismatch
 *
 * Usage:  place <FloatingLeaves /> anywhere in the component tree that
 *         renders globally (BackgroundSystem or RootLayout).
 *         The leaves are position:fixed so their DOM parent doesn't matter.
 */

import { useEffect, useRef } from "react";

/* ─── Config — all values traced from v3 source ──────────── */

const LEAF_COUNT = 18;

const LEAF_EMOJIS = ["🍃", "🌿", "🍀", "☘️", "🌱"] as const;

/* ─── Keyframe string injected once into <head> ─────────── */

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

/* ─── Component ──────────────────────────────────────────── */

export default function FloatingLeaves() {
  // Container div — leaves are appended here, not to document.body
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    /* --------------------------------------------------
     * 1. Inject @keyframes into <head> once.
     *    A data attribute prevents duplicate injection
     *    across HMR cycles.
     * -------------------------------------------------- */
    const STYLE_ID = "agro-leaf-keyframes";
    if (!document.getElementById(STYLE_ID)) {
      const style = document.createElement("style");
      style.id = STYLE_ID;
      style.textContent = LEAF_KEYFRAMES;
      document.head.appendChild(style);
    }

    /* --------------------------------------------------
     * 2. Build leaves.
     *    Every inline style below maps 1-to-1 to the
     *    original JS loop in v3:
     *
     *    l.style.cssText = `
     *      left:              ${Math.random() * 100}vw;
     *      font-size:         ${1 + Math.random() * 1.4}rem;
     *      animation-duration: ${18 + Math.random() * 22}s;
     *      animation-delay:   ${Math.random() * 20}s;
     *      opacity: 0;
     *    `;
     * -------------------------------------------------- */
    const container = containerRef.current;
    if (!container) return;

    const leaves: HTMLDivElement[] = [];

    for (let i = 0; i < LEAF_COUNT; i++) {
      const leaf = document.createElement("div");

      // Emoji — random from the five types
      leaf.textContent =
        LEAF_EMOJIS[Math.floor(Math.random() * LEAF_EMOJIS.length)];

      // Base class styles (mirrors .leaf in v3 CSS)
      leaf.style.position        = "fixed";
      leaf.style.pointerEvents   = "none";
      leaf.style.zIndex          = "-8";
      leaf.style.filter          = "blur(0.5px)";
      leaf.style.userSelect      = "none";
      leaf.style.animationName   = "leafFall";
      leaf.style.animationTimingFunction = "linear";
      leaf.style.animationIterationCount = "infinite";

      // Per-leaf randomised values (exact formula from v3)
      leaf.style.left            = `${Math.random() * 100}vw`;
      leaf.style.fontSize        = `${1 + Math.random() * 1.4}rem`;
      leaf.style.animationDuration = `${18 + Math.random() * 22}s`;
      leaf.style.animationDelay  = `${Math.random() * 20}s`;
      leaf.style.opacity         = "0"; // animation drives it

      container.appendChild(leaf);
      leaves.push(leaf);
    }

    /* --------------------------------------------------
     * 3. Cleanup — remove leaves and injected style on
     *    unmount / HMR so they never stack up.
     * -------------------------------------------------- */
    return () => {
      leaves.forEach((leaf) => leaf.remove());
    };
  }, []);

  /*
   * The container itself is invisible (no size, no background).
   * It exists only so React can own the leaf DOM nodes.
   * aria-hidden keeps leaves out of the accessibility tree.
   */
  return (
    <div
      ref={containerRef}
      aria-hidden="true"
      style={{ position: "fixed", inset: 0, pointerEvents: "none", zIndex: -8 }}
    />
  );
}
