#!/bin/bash
# https://superuser.com/a/386209
declare -A arr
shopt -s globstar

for file in **; do
  [[ -f "$file" ]] || continue

  read cksm _ < <(md5sum "$file")
  if ((arr[$cksm]++)); then
    rm "$file"
  fi
done
