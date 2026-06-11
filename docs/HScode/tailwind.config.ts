import type { Config } from "tailwindcss";

/**
 * tailwind.config.ts
 *
 * Tokens extracted directly from template.html :root variables.
 * These are not additions or interpretations — every value here
 * is present verbatim in the source template.
 */
const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // --primary: #166534
        "brand-deep": "#166534",
        // --secondary: #22C55E
        "brand-leaf": "#22C55E",
        // --soft: #DCFCE7
        "brand-soft": "#DCFCE7",
        // #86efac — used on stat card h3 values and nav hover
        "brand-accent": "#86efac",
        // --bg: #08110c — page background
        "brand-bg": "#08110c",
        // --danger / --warning / --success
        danger: "#ef4444",
        warning: "#f59e0b",
        success: "#22c55e",
        // Secondary text color used throughout template
        muted: "#cbd5e1",
      },

      fontFamily: {
        // Only font used in template: Inter
        sans: ["Inter", "sans-serif"],
      },

      borderRadius: {
        // Glass card radius: 28px
        card: "28px",
        // Logo box: 18px
        "logo-box": "18px",
        // Card icon / step number containers: 20px
        icon: "20px",
      },

      maxWidth: {
        // .container max-width: 1400px
        container: "1400px",
      },

      backgroundImage: {
        // The single gradient used across every primary surface in the template:
        // buttons, logo-box, step-numbers, card-icons, chat header, chat button
        "brand-gradient": "linear-gradient(135deg, #166534, #22C55E)",
      },

      keyframes: {
        // @keyframes pulse — hero glow orb
        // 0%,100% { transform: scale(1) }  50% { transform: scale(1.2) }
        pulse: {
          "0%, 100%": { transform: "scale(1)" },
          "50%": { transform: "scale(1.2)" },
        },
        // @keyframes floatPlant — hero emoji
        // 0%,100% { transform: translateY(0) }  50% { transform: translateY(-20px) }
        floatPlant: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-20px)" },
        },
        // @keyframes auroraOne — 120px,-100px translate + scale(1.4)
        auroraOne: {
          "0%": { transform: "translate(0,0) scale(1)" },
          "100%": { transform: "translate(120px,-100px) scale(1.4)" },
        },
        // @keyframes auroraTwo — -150px,100px translate + scale(1.5)
        auroraTwo: {
          "0%": { transform: "translate(0,0) scale(1)" },
          "100%": { transform: "translate(-150px,100px) scale(1.5)" },
        },
        // @keyframes auroraThree — 100px,-120px translate + scale(1.35)
        auroraThree: {
          "0%": { transform: "translate(0,0) scale(1)" },
          "100%": { transform: "translate(100px,-120px) scale(1.35)" },
        },
        // @keyframes particleMove — particles rise from 120vh to -20vh
        particleMove: {
          "0%": { transform: "translateY(120vh)" },
          "100%": { transform: "translateY(-20vh)" },
        },
      },

      animation: {
        // pulse 4s infinite — hero glow
        "glow-pulse": "pulse 4s infinite",
        // floatPlant 5s ease-in-out infinite — hero emoji
        "float-plant": "floatPlant 5s ease-in-out infinite",
        // aurora animations — alternate ease-in-out at different durations
        "aurora-one":   "auroraOne 20s infinite alternate ease-in-out",
        "aurora-two":   "auroraTwo 25s infinite alternate ease-in-out",
        "aurora-three": "auroraThree 30s infinite alternate ease-in-out",
        // particles — linear, per-particle duration set inline
        "particle-move": "particleMove linear infinite",
      },
    },
  },
  plugins: [],
};

export default config;
