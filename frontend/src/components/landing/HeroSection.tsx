/**
 * HeroSection.tsx
 *
 * Exact 1-to-1 conversion of the hero in template.html.
 */

import Link from "next/link";

export default function HeroSection() {

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
        className="px-[8%] py-[80px] lg:py-[120px] overflow-hidden"
      >
        <div
          className="
            mx-auto max-w-[1400px]
            grid grid-cols-1 lg:grid-cols-2
            items-center
            gap-[40px] lg:gap-[80px]
            min-h-[calc(100vh-100px)] lg:min-h-screen
            lg:text-left text-center
          "
        >
          <div className="hero-content order-2 lg:order-1 flex flex-col items-center lg:items-start">
            <div className="inline-flex items-center gap-[10px] rounded-full border border-[#22C55E]/20 bg-[#22C55E]/[0.08] px-[18px] py-[10px] text-[0.7rem] font-mono tracking-[0.15em] text-[#22C55E] uppercase mb-[28px] lg:mx-0 mx-auto w-fit">
              <span className="w-2 h-2 rounded-full bg-[#22C55E] animate-blink"></span>
              <span>AI-Powered Agriculture Platform</span>
            </div>

            <h1
              className="
                text-[clamp(2.5rem,8vw,5.5rem)]
                font-[800]
                leading-[1.1] lg:leading-[1.0]
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
                flex flex-col sm:flex-row
                gap-[16px] lg:gap-[20px]
                mt-[32px] lg:mt-[40px]
                w-full sm:w-auto
                justify-center lg:justify-start
              "
            >
              <Link
                href="/upload"
                className="
                  w-full sm:w-auto
                  px-[30px] py-[15px]
                  rounded-full
                  font-bold
                  text-white
                  border-none
                  cursor-pointer
                  transition-transform duration-300
                  hover:-translate-y-1
                  text-center
                "
                style={{
                  background: "linear-gradient(135deg, #166534, #22C55E)",
                }}
              >
                Start Scanning
              </Link>

              <button
                className="
                  w-full sm:w-auto
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

          <div className="flex justify-center items-center relative order-1 lg:order-2 w-full max-w-[500px] mx-auto aspect-square">
            <div
              className="absolute rounded-full w-full h-full max-w-[280px] max-h-[280px] sm:max-w-[400px] sm:max-h-[400px] lg:max-w-[500px] lg:max-h-[500px] will-change-transform"
              style={{
                background:
                  "radial-gradient(circle, rgba(34,197,94,0.3), transparent)",
                animation: "pulse 4s infinite",
              }}
            />

            <div
              className="text-[120px] sm:text-[180px] lg:text-[220px] relative z-[2] select-none will-change-transform"
              style={{
                animation: "floatPlant 5s ease-in-out infinite",
              }}
              aria-hidden="true"
            >
              🌿
            </div>
          </div>
        </div>



      </section>
    </>
  );
}
