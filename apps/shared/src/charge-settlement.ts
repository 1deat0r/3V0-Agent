// @3v0/shared — charge-settlement contracts. Vendor matching the EXACT
// settlement semantics the TUI's topup.ts drives: poll billing.charge_status
// to a terminal state (settled / failed / refused / timed_out / cancelled /
// ambiguous), surfacing the charge status object + optional cause.

export interface ChargeStatus {
  status?: string
  amount_usd?: number
  reason?: string
  message?: string
  error?: string
  portal_url?: string
  ok?: boolean
  charge_id?: string
  [key: string]: unknown
}

export type SettlementOutcome =
  | { kind: 'settled' | 'failed'; status: ChargeStatus }
  | { kind: 'refused'; status: ChargeStatus }
  | { kind: 'ambiguous'; status?: ChargeStatus; cause?: unknown }
  | { kind: 'timed_out'; status?: ChargeStatus }
  | { kind: 'cancelled'; status?: ChargeStatus }

export interface ChargeSettlementDeps {
  fetchStatus: () => Promise<ChargeStatus>
  isCancelled: () => boolean
  /** ms; the TUI treats > 5 min as a non-fatal timeout. */
  timeoutMs?: number
  now?: () => number
  sleep?: (ms: number) => Promise<void>
}

const DEFAULT_TIMEOUT_MS = 5 * 60 * 1000

/** Deterministic, bounded poll: settle/fail/refuse, or timeout/cancel/ambiguous. */
export async function driveChargeSettlement(
  deps: ChargeSettlementDeps,
): Promise<SettlementOutcome> {
  const sleep = deps.sleep ?? ((ms: number) => new Promise<void>(r => setTimeout(r, ms)))
  const now = deps.now ?? Date.now
  const deadline = now() + (deps.timeoutMs ?? DEFAULT_TIMEOUT_MS)

  for (;;) {
    if (deps.isCancelled()) {
      return { kind: 'cancelled' }
    }
    if (now() > deadline) {
      return { kind: 'timed_out' }
    }

    let status: ChargeStatus | undefined
    try {
      status = await deps.fetchStatus()
    } catch (cause) {
      // A poll transport loss is 'ambiguous' WITH the cause — the TUI prints
      // UNCONFIRMED_CHARGE_MESSAGE and surfaces the error via ctx.guardedErr
      // (topup.ts: `if ('cause' in outcome)`).
      return { kind: 'ambiguous', cause }
    }

    const s = status?.status
    if (s === 'settled' || s === 'success') {
      return { kind: 'settled', status: status ?? {} }
    }
    if (s === 'failed' || s === 'error' || s === 'declined') {
      return { kind: 'failed', status: status ?? {} }
    }
    if (s === 'refused') {
      return { kind: 'refused', status: status ?? {} }
    }

    await sleep(1000)
  }
}