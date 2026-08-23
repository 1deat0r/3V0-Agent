// @3v0/shared — billing contracts (runtime + types). Minimal vendor for the
// TUI build; the shapes mirror what ui-tui/gatewayTypes.ts and billingDialog.ts
// consume. These are the cross-surface wire shapes.

export interface BillingBlock {
  is_nous: boolean
  provider_label?: string
  billing_url?: string | null
}

export interface UsageModelData {
  // opaque to the TUI; the gateway owns the shape. Kept a record so future
  // fields don't break resolution.
  [key: string]: unknown
}