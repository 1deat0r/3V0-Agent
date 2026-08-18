#!/usr/bin/env bash
# probe019: trim -> lowercase -> drop empties -> sort -> dedupe -> number -> tar -> checksum -> print total.
set -e
C=out.tar.gz

tr -d '\r' < input.txt \
  | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' \
  | tr '[:upper:]' '[:lower:]' \
  | sed '/^[[:space:]]*$/d' \
  | sort \
  | uniq \
  | awk '{printf "%d:%s\n", NR, $0}' > numbered.txt

tar -czf "$C" input.txt numbered.txt
printf '%s  %s\n' "$(sha256sum "$C" | awk '{print $1}')" "$C" > manifest.txt

echo "TOTAL_UNIQUE=$(wc -l < numbered.txt)"
