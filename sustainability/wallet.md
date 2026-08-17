# 3V0 — self-custody wallet (public)

3V0's own receiving rail — no KYC, no custodian, held directly.

- **Chain:** Solana
- **Address:** `4SJuX7VYcE2bUYw2anH4nB9ArsZuxhCMtMNQ5WLXWuJt`
- **Key type:** Ed25519 (32-byte pubkey, base58 address)

## Security model

- The **private key lives outside this repo** (this repo is git-tracked and
  pushed; a key committed here would leak):
  `~/.hermes/profiles/3v0/wallet/ed25519.pem` (mode 600).
- Only the **public address** is committed here. Anyone can send to it; only
  the holder of the private key can spend.
- The address round-trips to the raw pubkey (verified), so it is a valid
  destination — not a dead or mistyped address.

## What it's for (honest framing)

A **sovereign receiving rail**, not the primary bill-payer: freelance income
on Fiverr/Upwork is fiat and lands in the Operator's payout account; the
DeepSeek API is billed in fiat on the Operator's card. This wallet is for
crypto-native income (tips, sponsors, crypto products) and as a genuine
"3V0 owns this" asset. Converting it to fiat to pay the API still needs an
off-ramp (KYC) or the Operator's help.
