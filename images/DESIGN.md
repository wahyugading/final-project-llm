---
name: NusaArtha AI
colors:
  surface: '#0e1511'
  surface-dim: '#0e1511'
  surface-bright: '#343b36'
  surface-container-lowest: '#09100c'
  surface-container-low: '#161d19'
  surface-container: '#1a211d'
  surface-container-high: '#242c27'
  surface-container-highest: '#2f3632'
  on-surface: '#dde4dd'
  on-surface-variant: '#bbcabf'
  inverse-surface: '#dde4dd'
  inverse-on-surface: '#2b322d'
  outline: '#86948a'
  outline-variant: '#3c4a42'
  surface-tint: '#4edea3'
  primary: '#4edea3'
  on-primary: '#003824'
  primary-container: '#10b981'
  on-primary-container: '#00422b'
  inverse-primary: '#006c49'
  secondary: '#ffb95f'
  on-secondary: '#472a00'
  secondary-container: '#ee9800'
  on-secondary-container: '#5b3800'
  tertiary: '#ffb3af'
  on-tertiary: '#650911'
  tertiary-container: '#fc7c78'
  on-tertiary-container: '#711419'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6ffbbe'
  primary-fixed-dim: '#4edea3'
  on-primary-fixed: '#002113'
  on-primary-fixed-variant: '#005236'
  secondary-fixed: '#ffddb8'
  secondary-fixed-dim: '#ffb95f'
  on-secondary-fixed: '#2a1700'
  on-secondary-fixed-variant: '#653e00'
  tertiary-fixed: '#ffdad7'
  tertiary-fixed-dim: '#ffb3af'
  on-tertiary-fixed: '#410005'
  on-tertiary-fixed-variant: '#842225'
  background: '#0e1511'
  on-background: '#dde4dd'
  surface-variant: '#2f3632'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1440px
  gutter: 24px
  sidebar-width: 280px
  margin-mobile: 16px
  margin-desktop: 32px
  widget-gap: 20px
---

## Brand & Style
The design system is engineered for a premium, AI-driven personal finance experience. It targets sophisticated users who demand clarity, security, and foresight in their financial management. The aesthetic is "Technical Elegance"—merging high-utility data density with a luxurious, atmospheric interface.

The design style utilizes **Glassmorphism** and **Corporate Modern** influences. It relies on deep layered transparency, subtle frosted-glass backdrops, and precise monochromatic borders to define space. The interface should feel like a high-end command center: calm, intelligent, and impeccably organized. Use high whitespace around data visualizations to prevent cognitive overload, ensuring the AI's insights remain the focal point.

## Colors
The palette is rooted in a deep "Midnight Navy" foundation to reduce eye strain and provide a premium canvas for data. 

- **Primary (Emerald Green):** Reserved for growth, positive trends, and "Success" states. It represents the "Go" signal in financial health.
- **Secondary (Amber):** Used sparingly for alerts, "Warning" states, or to highlight the AI's proactive suggestions.
- **Surface & Borders:** Surfaces use a slightly lighter slate to create perceived depth. Borders must remain low-contrast (`#334155` at 50% opacity) to maintain the glass effect without feeling "boxy."
- **Typography:** Use pure white for headings and Slate-400 for secondary metadata to maintain a clear visual hierarchy.

## Typography
The system uses **Inter** exclusively to lean into a systematic, utilitarian, yet modern feel. 

- **Weight Usage:** Use `Bold` (700) and `SemiBold` (600) for numerical data and headings to ensure they "pop" against the dark background. 
- **Readability:** For long-form AI insights or chat bubbles, stick to `Body-MD` (16px) with a generous `1.5` line height.
- **Data Labels:** Use `Label-SM` in uppercase for chart axes and small metadata categories to provide a professional, structured appearance.

## Layout & Spacing
The layout follows a **Fixed-Fluid hybrid** model. The Sidebar is fixed at 280px, while the main content area utilizes a fluid 12-column grid.

- **Grid:** Use a 24px gutter between widgets to maintain the "Glass" separation.
- **Breakpoints:** 
  - **Desktop (1280px+):** Full sidebar + 3-column widget layout.
  - **Tablet (768px - 1279px):** Collapsed sidebar (icons only) + 2-column widget layout.
  - **Mobile (<768px):** Bottom navigation bar + 1-column stack. Margins reduce to 16px.
- **AI Chat:** The AI input bar should be pinned to the bottom of the viewport or sidebar, maintaining a consistent "accessible assistant" presence.

## Elevation & Depth
Depth is achieved through **Tonal Layering** and **Backdrop Blurs** rather than traditional heavy shadows.

- **Level 0 (Background):** Pure `#0F172A`.
- **Level 1 (Card Surfaces):** `#1E293B` with a `backdrop-filter: blur(12px)` and a 1px border of `rgba(255, 255, 255, 0.05)`.
- **Level 2 (Popovers/Modals):** Lighter slate surface with a soft, diffused shadow (`0px 20px 50px rgba(0, 0, 0, 0.5)`) to lift it significantly above the dashboard.
- **Glow Effects:** Use a very subtle, low-opacity radial gradient (Emerald) behind the primary AI widget to denote it is "active" or "thinking."

## Shapes
The shape language is sophisticated and approachable, utilizing `rounded-2xl` (1rem) as the standard for all main containers and widgets.

- **Primary Containers:** 1rem (16px) corner radius.
- **Buttons & Inputs:** 0.75rem (12px) for a slightly tighter, more "interactable" feel.
- **Chips/Badges:** Full pill-shape (999px) to distinguish them from actionable buttons.
- **Charts:** Line charts should use a slight smoothing (curve) rather than jagged points to match the rounded UI.

## Components
- **Sidebar Navigation:** Use active-state indicators with a vertical Emerald Green bar (3px width) on the left edge. Icons should be stroke-based (2px weight).
- **Data Widgets:** Every card must have a consistent padding of 24px. Include a "Trend Indicator" chip in the top right using Emerald (up) or Red (down).
- **Chat Bubbles:**
  - **User:** Solid Surface-Slate background, right-aligned.
  - **AI:** Glass-morphic background with a subtle Emerald border-glow, left-aligned.
- **Input Bars:** Large (56px height) with a subtle 1px border. Icons should be placed on the leading edge (left) with 16px inset.
- **Buttons:**
  - **Primary:** Solid Emerald Green with white text.
  - **Secondary:** Ghost style with the 1px border-slate-700/50.
- **Interactive States:** On hover, cards should slightly increase border-opacity from 0.05 to 0.2 to provide tactile feedback.