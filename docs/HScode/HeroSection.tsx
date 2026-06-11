"use client";

/**
 * HeroSection.tsx
 *
 * Exact 1-to-1 conversion of the hero in template.html.
 * Every value below is traced directly from the source:
 *
 *  Layout   → .hero: grid 1fr 1fr, align-items center, gap 80px, min-height 100vh
 *  Section  → padding: 120px 8%
 *  H1       → font-size 5rem, font-weight 800, line-height 1.05
 *  Body p   → font-size 1.15rem, color #cbd5e1, margin-top 25px, line-height 1.9, max-width 650px
 *  Buttons  → padding 15px 30px, border-radius 999px, font-weight 700, transition 0.3s
 *             hover: translateY(-4px)
 *             primary: linear-gradient(135deg, #166534, #22C55E), color white
 *             secondary: background white, color black
 *  Buttons  → display flex, gap 20px, margin-top 40px, flex-wrap wrap
 *  Visual   → display flex, justify-content center, align-items center, position relative
 *  Glow     → 500×500px circle, radial-gradient(circle, rgba(34,197,94,.3), transparent)
 *             animation: pulse 4s infinite (scale 1 → 1.2 → 1)
 *  Plant    → font-size 220px, z-index 2
 *             animation: floatPlant 5s ease-in-out infinite (translateY 0 → -20px → 0)
 *  Stats    → margin-top -50px, grid repeat(4,1fr), gap 25px
 *  StatCard → .glass + padding 30px, text-align center
 *             h3: font-size 2rem, color #86efac
 *  Glass    → background rgba(255,255,255,0.08), backdrop-filter blur(24px),
 *             border 1px solid rgba(255,255,255,0.12),
 *             box-shadow 0 10px 40px rgba(0,0,0,0.25), border-radius 28px
 *  Responsive →
 *    ≤1024px: grid 1fr, text-align center, p margin auto + margin-top 25px,
 *             buttons justify-content center, stats repeat(2,1fr)
 *    ≤768px : h1 font-size 3rem, stats 1fr
 */

import { useRef } from "react";

/* ─── Types ─────────────────────────────────────── */

interface StatItem {
  value: string;
  label: string;
}

/* ─── Data (exactly as in template.html) ────────── */

const STATS: StatItem[] = [
  { value: "50K+", label: "Crop Scans" },
  { value: "96%",  label: "AI Accuracy" },
  { value: "10K+", label: "Farmers" },
  { value: "24/7", label: "AI Support" },
];

/* ─── Component ──────────────────────────────────── */

export default function HeroSection() {
  const fileInputRef = useRef<HTMLInputElement>(null);

  return (
    <>
      {/*
       * Keyframes live here as a <style> tag so they are scoped to this
       * component and do not require changes to globals.css or
       * tailwind.config.ts.  These are the exact @keyframes from the
       * template — pulse and floatPlant — with identical values.
       */}
      <style>{`
        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50%       { transform: scale(1.2); }
        }
        @keyframes floatPlant {
          0%, 100% { transform: translateY(0); }
          50%       { transform: translateY(-20px); }
        }
      `}</style>

      {/*
       * <section id="home">
       * padding: 120px 8%  →  py-[120px] px-[8%]
       */}
      <section
        id="home"
        className="px-[8%] py-[120px]"
      >

        {/*
         * .container.hero
         * max-width: 1400px, margin: auto
         * display: grid, grid-template-columns: 1fr 1fr
         * align-items: center, gap: 80px, min-height: 100vh
         *
         * Responsive ≤1024px: single column, text-align center
         */}
        <div
          className="
            mx-auto max-w-[1400px]
            grid grid-cols-1 lg:grid-cols-2
            items-center
            gap-[80px]
            min-h-screen
            lg:text-left text-center
          "
        >

          {/* ── Left column: hero-content ── */}
          <div className="hero-content">

            {/*
             * h1
             * font-size: 5rem → text-[5rem]
             * font-weight: 800 → font-extrabold
             * line-height: 1.05 → leading-[1.05]
             * Responsive ≤768px: font-size 3rem → sm:text-[5rem] text-[3rem]
             */}
            <h1
              className="
                text-[3rem] sm:text-[5rem]
                font-extrabold
                leading-[1.05]
                text-white
              "
            >
              AI-Powered Crop Disease Detection &amp; Agricultural Intelligence
            </h1>

            {/*
             * p
             * font-size: 1.15rem → text-[1.15rem]
             * color: #cbd5e1 → text-[#cbd5e1]
             * margin-top: 25px → mt-[25px]
             * line-height: 1.9 → leading-[1.9]
             * max-width: 650px → max-w-[650px]
             * Responsive ≤1024px: margin auto + margin-top 25px
             */}
            <p
              className="
                text-[1.15rem]
                text-[#cbd5e1]
                mt-[25px]
                leading-[1.9]
                max-w-[650px]
                lg:mx-0 mx-auto
              "
            >
              Protect your harvest with next-generation AI. Detect diseases
              instantly, receive treatment recommendations, generate reports, and
              make smarter farming decisions.
            </p>

            {/*
             * .hero-buttons
             * display: flex, gap: 20px, margin-top: 40px, flex-wrap: wrap
             * Responsive ≤1024px: justify-content center
             */}
            <div
              className="
                flex flex-wrap
                gap-[20px]
                mt-[40px]
                lg:justify-start justify-center
              "
            >
              {/*
               * .btn.btn-primary
               * padding: 15px 30px, border-radius: 999px, font-weight: 700
               * background: linear-gradient(135deg, #166534, #22C55E)
               * color: white
               * transition: 0.3s
               * hover: translateY(-4px)
               */}
              <button
                className="
                  px-[30px] py-[15px]
                  rounded-full
                  font-bold
                  text-white
                  border-none
                  cursor-pointer
                  transition-transform duration-300
                  hover:-translate-y-1
                "
                style={{
                  background: "linear-gradient(135deg, #166534, #22C55E)",
                }}
              >
                Start Scanning
              </button>

              {/*
               * .btn.btn-secondary
               * padding: 15px 30px, border-radius: 999px, font-weight: 700
               * background: white, color: black
               * transition: 0.3s
               * hover: translateY(-4px)
               */}
              <button
                className="
                  px-[30px] py-[15px]
                  rounded-full
                  font-bold
                  bg-white text-black
                  border-none
                  cursor-pointer
                  transition-transform duration-300
                  hover:-translate-y-1
                "
              >
                Watch Demo
              </button>
            </div>
          </div>

          {/* ── Right column: hero-visual ── */}
          {/*
           * .hero-visual
           * display: flex, justify-content: center, align-items: center
           * position: relative
           */}
          <div className="flex justify-center items-center relative">

            {/*
             * .glow
             * position: absolute, width: 500px, height: 500px
             * border-radius: 50%
             * background: radial-gradient(circle, rgba(34,197,94,.3), transparent)
             * animation: pulse 4s infinite
             */}
            <div
              className="absolute rounded-full w-[500px] h-[500px]"
              style={{
                background:
                  "radial-gradient(circle, rgba(34,197,94,0.3), transparent)",
                animation: "pulse 4s infinite",
              }}
            />

            {/*
             * .hero-plant
             * font-size: 220px → text-[220px] (sm), text-[150px] (mobile — from responsive rule)
             * animation: floatPlant 5s ease-in-out infinite
             * z-index: 2
             */}
            <div
              className="text-[150px] sm:text-[220px] relative z-[2] select-none"
              style={{
                animation: "floatPlant 5s ease-in-out infinite",
              }}
              aria-hidden="true"
            >
              🌿
            </div>
          </div>
        </div>

        {/*
         * .container.stats
         * margin-top: -50px → -mt-[50px]
         * display: grid, grid-template-columns: repeat(4,1fr)
         * gap: 25px
         * Responsive ≤1024px: repeat(2,1fr)
         * Responsive ≤768px:  1fr
         */}
        <div
          className="
            mx-auto max-w-[1400px]
            grid
            grid-cols-1 sm:grid-cols-2 lg:grid-cols-4
            gap-[25px]
            -mt-[50px]
          "
        >
          {STATS.map((stat) => (
            /*
             * .glass.stat-card
             * Glass: background rgba(255,255,255,0.08), backdrop-filter blur(24px)
             *        border 1px solid rgba(255,255,255,0.12)
             *        box-shadow: 0 10px 40px rgba(0,0,0,0.25)
             *        border-radius: 28px
             * StatCard: padding 30px, text-align center
             */
            <div
              key={stat.label}
              className="rounded-[28px] p-[30px] text-center"
              style={{
                background: "rgba(255,255,255,0.08)",
                backdropFilter: "blur(24px)",
                WebkitBackdropFilter: "blur(24px)",
                border: "1px solid rgba(255,255,255,0.12)",
                boxShadow: "0 10px 40px rgba(0,0,0,0.25)",
              }}
            >
              {/*
               * stat-card h3
               * font-size: 2rem, color: #86efac
               */}
              <h3 className="text-[2rem] font-bold text-[#86efac]">
                {stat.value}
              </h3>
              <p className="text-white mt-1">{stat.label}</p>
            </div>
          ))}
        </div>

        {/* Hidden file input — wired to "Start Scanning" in real implementation */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          className="hidden"
          aria-hidden="true"
        />
      </section>
    </>
  );
}
