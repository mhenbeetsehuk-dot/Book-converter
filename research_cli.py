"""CLI for read-only capability discovery; no auto-installation."""
import argparse
import json
from learning.discovery import discover

def main():
    parser = argparse.ArgumentParser(description="Search GitHub and OpenAlex for free film-making techniques")
    parser.add_argument("query", help="Capability to research, e.g. 'Blender procedural character animation'")
    args = parser.parse_args()
    print(json.dumps(discover(args.query), indent=2))

if __name__ == "__main__":
    main()
