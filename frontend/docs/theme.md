# AgroGuard Theme Configuration (Task 3.2)

This document outlines the design tokens, color palette, typography, animations, and glassmorphism specifications extracted from the master `template.html` for the AgroGuard frontend.

## 1. Colors & Shadcn Mapping

### Extracted Theme Colors
- **`--g` (Deep Green):** `#166534` - Darkest green for gradient start and deep accents.
- **`--g2` (Main Green):** `#22C55E` - Primary brand color, used for primary actions, buttons, rings.
- **`--g3` (Light Green):** `#4ade80` - Secondary highlights.
- **`--g4` (Lighter Green):** `#86efac` - Hover highlights.
- **`--g5` (Pale Green):** `#dcfce7` - Subtle success states.
- **`--bg` (Primary BG):** `#050d07` - The main application background color. Very dark green-tinted black.
- **`--bg2` (Secondary BG):** `#0a1a0d` - Used for cards, popovers, and elevated elements.
- **`--bg3` (Tertiary BG):** `#0f2414` - Muted secondary containers or hover states.
- **`--text` (Foreground):** `#f0fdf4` - Primary text color for high readability against dark backgrounds.
- **`--muted-text` (Muted):** `#6b7280` - Secondary text, placeholders.
- **Destructive:** `#ef4444` - Used for destructive actions/errors (standard Shadcn destructive).

### Shadcn Variables Mapping
The extracted colors are mapped directly into standard Shadcn variables within `globals.css`:
- `--background` -> `var(--bg)`
- `--foreground` -> `var(--text)`
- `--primary` -> `var(--g2)`
- `--primary-foreground` -> `#ffffff`
- `--card` / `--popover` -> `var(--bg2)`
- `--card-foreground` / `--popover-foreground` -> `var(--text)`
- `--secondary` / `--muted` / `--accent` -> `var(--bg3)`
- `--secondary-foreground` / `--accent-foreground` -> `var(--text)`
- `--muted-foreground` -> `var(--muted-text)`
- `--border` -> `rgba(255, 255, 255, 0.12)` (Contrast optimized)
- `--input` -> `var(--glass-border)`
- `--ring` -> `var(--g2)`

## 2. Typography

*Note: Custom fonts (Syne, DM Sans, Space Mono) have not been loaded into the layout yet and are deferred to a future task. Currently using Next.js default Geist fonts.*

## 3. Design Tokens

### Glassmorphism Variables
- **Glass Background (`--glass`):** `rgba(255, 255, 255, 0.04)`
- **Glass Border (`--glass-border`):** `rgba(255, 255, 255, 0.08)`
- **Glass Strong (`--glass-strong`):** `rgba(255, 255, 255, 0.09)`
- **Blur Values:** 20px for regular glass, 30px for strong glass.

### Reusable Utilities (No components)
Defined in `@layer utilities` in `globals.css`:
- `.glass-card`: Background `--glass`, backdrop blur 20px, border `--glass-border`, border-radius `--radius`.
- `.glass-card-strong`: Background `--glass-strong`, backdrop blur 30px, border `rgba(255, 255, 255, 0.12)`, border-radius `--radius`.

## 4. Animations

General animations have been extracted as `@keyframes` in `globals.css` and mapped to Tailwind v4 theme variables via `--animate-[name]`:
- `blink` (`blink 2s infinite`)
- `text-shimmer` (`textShimmer 4s linear infinite`)
- `orb-pulse` (`orbPulse 6s ease-in-out infinite`)

*Note: Landing-page specific animations (auroras, particles, floating plants, grids) are reserved for Phase 4 implementation.*

## 5. Guidelines for Future Tasks

1. **Strict Separation:** This theme is purely structural. Do not generate Button, Card, or Navbar components.
2. **Usage:** Apply Tailwind classes like `bg-background`, `text-primary`, and `animate-orb-pulse` natively.
3. **Glass UI:** Rely on the `.glass-card` utilities for containers instead of hardcoding translucent backgrounds.
