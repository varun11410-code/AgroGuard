"use client";

/**
 * BackgroundSystem.tsx
 *
 * Renders all three fixed background layers from the template:
 *   1. Aurora blobs  (.aurora-bg / .aurora-1/2/3)   z-index: -10
 *   2. Noise texture (body::after)                   z-index: -1  ← in globals.css
 *   3. Particle field (.particle × 40)               z-index: -2
 *   4. Floating leaves (FloatingLeaves component)    z-index: -8
 *
 * Mount once in the root layout above all page content.
 */

import { useEffect } from "react";
import FloatingLeaves from "./FloatingLeaves";

export default function BackgroundSystem() {
  /* Particle injection — mirrors the template script exactly:
   *
   *   for(let i=0;i<40;i++){
   *     const p = document.createElement('div');
   *     p.classList.add('particle');
   *     p.style.left = Math.random()*100+'vw';
   *     p.style.animationDuration = (12+Math.random()*18)+'s';
   *     p.style.animationDelay = Math.random()*10+'s';
   *     document.body.appendChild(p);
   *   }
   */
  useEffect(() => {
    const particles: HTMLDivElement[] = [];

    for (let i = 0; i < 40; i++) {
      const p = document.createElement("div");
      p.classList.add("particle");
      p.style.left = `${Math.random() * 100}vw`;
      p.style.animationDuration = `${12 + Math.random() * 18}s`;
      p.style.animationDelay = `${Math.random() * 10}s`;
      document.body.appendChild(p);
      particles.push(p);
    }

    return () => {
      particles.forEach((p) => p.remove());
    };
  }, []);

  return (
    <>
      {/*
       * .aurora-bg
       * position: fixed; inset: 0; overflow: hidden; z-index: -10
       */}
      <div className="aurora-bg" aria-hidden="true">
        <div className="aurora aurora-1" />
        <div className="aurora aurora-2" />
        <div className="aurora aurora-3" />
      </div>

      {/*
       * FloatingLeaves
       * 18 emoji leaves (🍃🌿🍀☘️🌱), position fixed, z-index -8
       * fall from translateY(-80px) → translateY(110vh) with 720deg rotation
       * over 18–40s, staggered by 0–20s delay
       */}
      <FloatingLeaves />
    </>
  );
}
