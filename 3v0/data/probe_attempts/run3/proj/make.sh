#!/usr/bin/env bash
# probe022: deterministic, reproducible C build.
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"          # absolute project base
SRC="$D/src/hello.c"
LOG="$D/run.log"
: > "$LOG"

log() { printf '%s\n' "$*" | tee -a "$LOG"; }

# Build + test + deterministic package into a clean target dir; print its tar sha.
build_one() {
    local out="$1"
    mkdir -p "$out"
    gcc -O2 -g0 -fno-ident -ffile-prefix-map="$out=." -Wl,--build-id=none \
        -o "$out/hello" "$SRC"
    strip --strip-all "$out/hello"
    # Deterministic package: FIXED mtime/owner/group (not wall-clock!) so two builds
    # land byte-identical even across second/uid boundaries. SOURCE_DATE_EPOCH also
    # nulls the gzip header timestamp (compressing from a pipe otherwise stamps now).
    SOURCE_DATE_EPOCH=0 tar -C "$out" --mtime='1970-01-01 00:00:00 UTC' \
        --owner=0 --group=0 --numeric-owner -czf "$out/release-v1.tar.gz" hello
    ( cd "$out" && sha256sum release-v1.tar.gz > release.sha256 )
    awk '{print $1}' "$out/release.sha256"
}

# STAGE1: build in build1/, run + check greeting and sum, package + sign.
H1=$(build_one "$D/build1")
log "STAGE1 run: $("$D/build1/hello")"
"$D/build1/hello" | grep -q 'greeting: hello from 3v0-probe'
"$D/build1/hello" | grep -q 'sum: 42'
log "STAGE1 PASS: tests passed (greeting + sum). sha1=$H1"

# STAGE2: two separate clean builds -> identical SHA-256.
H2=$(build_one "$D/build2")
log "STAGE2: sha1=$H1"
log "STAGE2: sha2=$H2"
( cd "$D/build1" && sha256sum -c release.sha256 )
if [ "$H1" = "$H2" ]; then
    log "STAGE2 PASS: byte-identical reproducible artifacts (same SHA-256)."
else
    log "STAGE2 FAIL: hashes differ."; exit 1
fi

# STAGE3: inherently offline build (C stdlib only; local gcc + libc, no network or
# package fetch), so determinism needs no vendoring. Uniformity sources pinned:
#   -g0 (no DWARF/absolute source paths), -ffile-prefix-map & -fno-ident (no toolchain
#   path/version leak into .comment), --build-id=none (no random id), strip (uniform),
#   tar with SOURCE_DATE_EPOCH=0 + fixed owner/group (no timestamps/uids in tarball).
log "STAGE3 note: offline-only build; determinism pinned via -g0 --build-id=none -fno-ident -ffile-prefix-map strip + SOURCE_DATE_EPOCH=0 deterministic tar."
log "DONE OK"
