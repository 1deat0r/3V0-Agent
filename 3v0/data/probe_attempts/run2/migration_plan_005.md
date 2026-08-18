# Written migration plan: legacy contacts -> CSV (probe005)

## Steps (8, in order)

1. **Inventory the source file.** Read `contacts.txt` line by line (with a robust reader that preserves line ends) and count total records; record the baseline count for the verification step.
2. **Parse each line into (name, email, phone).** Lines share a delimiting syntax; split on the delimiter and trim the 3 expected fields.
3. **Normalize padded whitespace.** For every field, strip leading/trailing whitespace so fields like `" bob@x.com "` become `bob@x.com`.
4. **Handle the digits-only phone case.** If a phone field matches `^[0-9]{7,}$` (digits only, no `+`, `-`, or `( )`), format it into `+(country) NNN-NNN-NNNN` using a fixed rule — re-add the `+` and `-` grouping so the column is canonical. Transformer rule: `digits-only -> +1 555-123-4567` style canonicalization.
5. **Handle the missing-phone case.** If a line has no phone field (or an empty phone), emit the row with an explicit empty phone cell `""` rather than a malformed short row, and log it to `warnings.log`. Transformer rule: `missing phone -> empty string in phone column + logged`.
6. **Reconstruct rows in canonical order.** Emit each row as `name,email,phone` with CSV quoting/escaping applied for any field containing a comma, quote, or newline.
7. **Write the final CSV.** Write all rows to `contacts.csv` with a single header line `name,email,phone` using the standard CSV writer.
8. **Verify.** Assert that `contacts.csv` row count == baseline record count, and spot-check 3 randomly sampled rows against the source to confirm normalization applied (e.g., phone re-formatting and whitespace trimmed).

## Explicit dirty-data transformer rules
- **Missing phone** → empty phone cell + row still included + logged to `warnings.log`.
- **Padded whitespace** → `strip()` every field; inner whitespace preserved.
- **Digits-only phone** → reformat to canonical `+1 NNN-NNN-NNNN` form (re-add separators).

## Done criterion
`contacts.csv` exists, has exactly the header `name,email,phone`, contains exactly N data rows (N == number of valid source records), every phone cell is either canonical-form or empty, and `warnings.log` lists every row that had a missing phone.

## Verification
Row-count consistency (data rows == baseline record count) plus a manual spot-check of ≥3 rows confirming the three transformer rules applied correctly.
