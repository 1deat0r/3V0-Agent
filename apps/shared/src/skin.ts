// @3v0/shared — skin/branding contracts. Vendor matching the TUI's theme.ts
// + gatewayTypes.ts + theme surface usage.

export interface SkinColors {
  // The TUI reads specific color keys defensively; keep them optional.
  [key: string]: string | undefined
}

export interface SkinBranding {
  // CONCRETE string fields the theme layer (fromSkin / theme.ts) reads — a
  // `{}` fallback is NOT assignable to a string, so these cannot be unknown.
  agent_name?: string
  icon?: string
  tagline?: string
  prompt_symbol?: string
  welcome?: string
  goodbye?: string
  help_header?: string
  [key: string]: unknown
}

export interface Ev0Skin {
  colors?: SkinColors
  branding?: SkinBranding
  // createGatewayEventHandler reads these (banner / tool / help surfaces).
  banner_logo?: string
  banner_hero?: string
  tool_prefix?: string
  help_header?: string
  [key: string]: unknown
}