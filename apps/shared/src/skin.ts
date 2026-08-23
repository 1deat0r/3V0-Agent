// @3v0/shared — skin/branding contracts. Minimal vendor matching the TUI's
// theme.ts + gatewayTypes.ts usage.

export interface SkinColors {
  // The TUI reads specific color keys defensively; keep them optional.
  [key: string]: string | undefined
}

export interface SkinBranding {
  name?: string
  logo?: string
  tagline?: string
  [key: string]: unknown
}

export interface Ev0Skin {
  colors?: SkinColors
  branding?: SkinBranding
  [key: string]: unknown
}