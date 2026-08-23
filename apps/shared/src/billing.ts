// @3v0/shared — billing contracts (runtime + types). Vendor matching the
// exact shapes the TUI's billing/subscription slash commands + billing overlay
// consume (billingOverlay.tsx, topup.ts, subscription.ts).
//
// Upstream did not ship this package in this body, so it's a faithful vendor
// of the wire contract the client reads. Fields the TUI reads are concrete;
// the rest are optional so the RPC generics stay permissive.

export interface BillingCardInfo {
  brand?: string
  last4?: string
  exp_month?: number
  exp_year?: number
  name?: string
  display?: string
  kind?: string
  // subscriptionOverlay reads these (charge-card resolution display).
  resolved_via?: 'subPin' | 'customerDefault' | string
  masked?: string
}

export interface BillingAutoReload {
  enabled?: boolean
  // The gateway sends these as display strings ("$5.00"); the overlay coerces
  // with Number(...). So type them as strings.
  threshold_usd?: string
  threshold_display?: string
  reload_amount_usd?: string
  reload_to_usd?: string
  reload_to_display?: string
  billing_url?: string | null
  card?: BillingCardInfo
}

export interface BillingMonthlyCap {
  enabled?: boolean
  max_usd?: number
  is_default_ceiling?: boolean
  limit_usd?: number
  spent_display?: string
  limit_display?: string
}

export interface UsageBarData {
  label?: string
  value?: number
  model?: string
}

export interface UsageModelData {
  // subscriptionOverlay reads usage status / spendable balance; the usage-bars
  // widget reads plan_bar + topup_bar.
  status?: 'low' | 'ok' | string
  total_spendable_display?: string
  remaining_display?: string
  total_display?: string
  has_topup?: boolean
  available?: boolean
  plan_name?: string
  plan_bar?: {
    // The usage-bars widget treats these as always present.
    fill_fraction: number
    pct_used: number
    remaining_display: string
    total_display: string
  }
  topup_bar?: {
    remaining_display?: string
    total_display?: string
  }
  [key: string]: unknown
}

export interface BillingBlock {
  is_nous: boolean
  provider_label?: string
  billing_url?: string | null
  message?: string
  model?: string
  provider?: string
}

export interface BillingErrorPayload {
  code?: string
  message?: string
  error?: string
  remainingUsd?: number
}

export interface BillingChargeResponse {
  ok?: boolean
  charge_id?: string
  url?: string
  amount_usd?: number
  error?: string
}

export interface BillingChargeStatusResponse {
  status?: string | 'settled' | 'failed' | 'pending'
  charge_id?: string
  error?: string
  message?: string
  reason?: string
  amount_usd?: number
  [key: string]: unknown
}

export interface BillingMutationResponse {
  ok?: boolean
  // Step-up / remote-spending mutations also carry `granted` + `message`.
  granted?: boolean
  message?: string
  error?: string
  [key: string]: unknown
}

export interface BillingStateResponse {
  // Read by billingOverlay / topup / subscription.
  balance_display?: string
  is_admin?: boolean
  role?: string
  org_name?: string
  portal_url?: string
  auto_reload?: BillingAutoReload
  monthly_cap?: BillingMonthlyCap
  card?: BillingCardInfo
  usage?: UsageModelData
  charge_presets: string[]
  charge_presets_display: string[]
  reload_to_usd?: number
  reload_to_display?: string
  cli_billing_enabled?: boolean
  logged_in?: boolean
  org_id?: string
  subscription?: unknown
  [key: string]: unknown
}

export interface SubscriptionTierOption {
  id?: string
  name?: string
  price_usd?: number
  billing_interval?: string
  // subscriptionOverlay treats these as present (reads tier_order, name,
  // dollars_per_month_display directly without guards).
  tier_id: string
  tier_name: string
  tier_order: number
  is_current?: boolean
  is_enabled?: boolean
  // NB: may be a bare decimal string ("1,000") per the overlay, so allow both.
  monthly_credits?: number | string
  dollars_per_month_display: string
  cycle_ends_at?: string
  // pending change / cancellation bookkeeping (subscriptionOverlay reads).
  cancel_at_period_end?: boolean
  cancellation_effective_display?: string
  cancellation_effective_at?: string
  pending_downgrade_tier_name?: string
  pending_downgrade_display?: string
  pending_downgrade_at?: string
  [key: string]: unknown
}

export interface SubscriptionStateResponse {
  active?: boolean
  tier?: SubscriptionTierOption
  // subscriptionOverlay treats the plan list + current plan + usage as present.
  tiers: SubscriptionTierOption[]
  current: SubscriptionTierOption
  tier_id?: string
  tier_name?: string
  renewal_date?: string
  cycle_ends_at?: string
  cancel_at?: string
  portal_url?: string
  status?: string
  monthly_credits?: number
  can_change_plan: boolean
  usage: UsageModelData
  org_id?: string
  [key: string]: unknown
}

export interface SubscriptionPreviewResponse {
  tier?: SubscriptionTierOption
  prorated_usd?: number
  next_charge_usd?: number
  error?: string
  // subscriptionOverlay reads these for the change/cancel preview.
  amount_due_now_cents?: number
  target_tier_name?: string
  target_tier_id?: string
  tier_id?: string
  tier_name?: string
  cycle_ends_at?: string
  monthly_credits_delta?: number
  effective_at?: string
  [key: string]: unknown
}

export interface SubscriptionUpgradeResponse {
  ok?: boolean
  url?: string
  error?: string
  recovery_url?: string
  status?: string
  [key: string]: unknown
}