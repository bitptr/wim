#!/bin/sh

MAN_PREFIX="${PREFIX}/man"
if [ ! -d "$MAN_PREFIX" ]; then
  MAN_PREFIX="${PREFIX}/share/man"
fi

for section in man*; do
  target="$MAN_PREFIX/$section"

  if ! [ -d "$target" ]; then
    mkdir -p "$target"
  fi

  for page in ./"$section"/*.?; do
    echo "Installing $(basename $page) manpage to $target"
    install -m 444 "$page" "$target"
  done
done
