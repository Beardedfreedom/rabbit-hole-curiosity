#!/bin/sh
# Install the Rabbit-Hole Curiosity skill into ~/.agents/skills/rabbit-hole-curiosity
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
DEST="$HOME/.agents/skills/rabbit-hole-curiosity"
mkdir -p "$DEST"
cp -R "$ROOT/rabbit-hole-curiosity/"* "$DEST/"
chmod +x "$DEST/scripts/rabbit_hole_engine.py"
echo "Installed Rabbit-Hole Curiosity skill to: $DEST"
echo "Try it now:"
echo "  python3 ~/.agents/skills/rabbit-hole-curiosity/scripts/rabbit_hole_engine.py explore \"Serendipity\""
