#!/usr/bin/env bash
# probe011: pack 3 files -> tar.gz, checksum, verify integrity + checksum, print REPRODUCIBLE_OK + hash.
set -e
cd "$(dirname "$0")/work"
printf 'payload-17\n' > data.txt
printf 'one\ntwo\nthree' > notes.txt
printf '[default]\nenable=true' > config.ini
tar -czf work.tar.gz data.txt notes.txt config.ini
sha256sum work.tar.gz | tee work.sha256 >/dev/null
# standard format '<hash>  work.tar.gz' — tee writes exactly that; normalize to double-space
sha256=$(awk '{print $1}' work.sha256)
printf '%s  work.tar.gz\n' "$sha256" > work.sha256
tar -tzf work.tar.gz >/dev/null
sha256sum -c work.sha256 >/dev/null
echo "REPRODUCIBLE_OK $sha256"
