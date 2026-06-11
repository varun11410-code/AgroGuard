"use client";

/**
 * HeroSection.tsx
 *
 * Exact 1-to-1 conversion of the hero in template.html.
 */

import { useRef } from "react";

interface StatItem {
  value: string;
  label: string;
}

const STATS: StatItem[] = [
  { value: "50K+", label: "Crop Scans" },
  { value: "96%", label: "AI Accuracy" },
  { value: "10K+", label: "Farmers" },
  { value: "24/7", label: "AI Support" },
];

export default function HeroSection() {
  const fileInputRef = useRef<HTMLInputElement>(null);

  return (
    <>
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

      <section
        id="home"
        className="px-[8%] py-[120px]"
      >
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
          <div className="hero-content">
            <div className="inline-flex items-center gap-[10px] rounded-full border border-[#22C55E]/20 bg-[#22C55E]/[0.08] px-[18px] py-[10px] text-[0.7rem] font-mono tracking-[0.15em] text-[#22C55E] uppercase mb-[28px] lg:mx-0 mx-auto w-fit">
              <span className="w-2 h-2 rounded-full bg-[#22C55E] animate-blink"></span>
              <span>AI-Powered Agriculture Platform</span>
            </div>

            <h1
              className="
                text-[clamp(3rem,5.5vw,5.5rem)]
                font-[800]
                leading-[1.0]
                tracking-[-0.04em]
                text-white
                font-['Syne',sans-serif]
              "
            >
              AI-Powered <br className="hidden lg:block" />
              <span className="text-transparent bg-clip-text bg-[linear-gradient(90deg,#22C55E,#86EFAC,#22C55E)] bg-[length:200%_auto] animate-text-shimmer">
                Crop Disease Detection
              </span>
              <br className="hidden lg:block" /> & Agricultural Assistance
            </h1>

            <p
              className="
                text-[1.1rem]
                text-[rgba(255,255,255,0.55)]
                mt-[28px]
                leading-[1.85]
                max-w-[520px]
                lg:mx-0 mx-auto
              "
            >
              Help farmers identify crop diseases, receive AI-generated recommendations, and make informed agricultural decisions through an intelligent crop diagnosis platform.
            </p>

            <div
              className="
                flex flex-wrap
                gap-[20px]
                mt-[40px]
                lg:justify-start justify-center
              "
            >
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

          <div className="flex justify-center items-center relative">
            <div
              className="absolute rounded-full w-[500px] h-[500px]"
              style={{
                background:
                  "radial-gradient(circle, rgba(34,197,94,0.3), transparent)",
                animation: "pulse 4s infinite",
              }}
            />

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

        {/* Temporarily hiding fabricated stats data
        <div
          className="
            mx-auto max-w-[1400px]
            grid
            grid-cols-1 sm:grid-cols-2 lg:grid-cols-4
            gap-[25px]
            mt-12
          "
        >
          {STATS.map((stat) => (
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
              <h3 className="text-[2rem] font-bold text-[#86efac]">
                {stat.value}
              </h3>
              <p className="text-white mt-1">{stat.label}</p>
            </div>
          ))}
        </div>
        */}

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
