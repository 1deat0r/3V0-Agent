// @3v0/shared — charge-settlement contracts. Minimal vendor for the TUI's
// topup.ts: the settlement poll-loop driver and its outcome union. It mirrors
// the semantic the slash command relies on (poll billing.charge_status until
// settled/failed, collapsing to 'ambiguous' with no status on cancels).

export type SettlementOutcome =
  | { kind: 'settled'; status?: unknown }
  | { kind: 'failed'; reason?: string; status?: unknown }
  | { kind: 'ambiguous'; status?: unknown }

export interface ChargeSettlementDeps {
  fetchStatus: () => Promise<{ status: unknown }>
  isCancelled: () => boolean
  now?: () => number
  sleep?: (ms: number) => Promise<void>
}

export async function driveChargeSettlement(
  deps: ChargeSettlementDeps,
): Promise<SettlementOutcome> {
  // Deterministic, bounded poll: try up to 200 times; a cancel or throw -> ambiguous.
  const sleep = deps.sleep ?? ((ms: number) => new Promise<void>(r => setTimeout(r, ms)))
  const now = deps.now ?? Date.now
  void now
  for (let i = 0; i < 200; i++) {
    if (deps.isCancelled()) {
      return { kind: 'ambiguous', status: undefined }
    }
    let status: unknown
    try {
      const res = await deps.fetchStatus()
      status = res?.status
    } catch {
      return { kind: 'ambiguous', status: undefined }
    }
    if (status === 'settled' || status === 'success') {
      return { kind: 'settled', status }
    }
    if (status === 'failed' || status === 'error') {
      return { kind: 'failed', status }
    }
    await sleep(1000)
  }
  return { kind: 'ambiguous', status: undefined }
}