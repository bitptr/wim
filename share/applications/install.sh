#!/bin/sh

DESKTOP_DIR="${PREFIX}/share/applications"

for file in *.desktop; do
  target="$DESKTOP_DIR/$file"

  if ! [ -d "$(dirname $target)" ]; then
    mkdir -p "$(dirname target)"
  fi

  echo "Installing $(basename $file) desktop entry to $target"
  install -m 644 "$file" "$target"
done

if command -v update-desktop-database; then
  echo "update-desktop-database $DESKTOP_DIR"
  update-desktop-database "$DESKTOP_DIR"
fi
