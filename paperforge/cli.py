from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .render import load_request, write_output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="paperforge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    render_parser = subparsers.add_parser("render", help="Render a carnet")
    render_parser.add_argument("--config", required=True, type=Path)
    render_parser.add_argument("--output", required=True, type=Path)
    render_parser.add_argument("--html-only", action="store_true")

    web_parser = subparsers.add_parser("web", help="Start the local web app")
    web_parser.add_argument("--host", default="127.0.0.1")
    web_parser.add_argument("--port", default=8765, type=int)

    args = parser.parse_args(argv)
    if args.command == "render":
        request = load_request(args.config)
        try:
            write_output(request, args.output, html_only=args.html_only)
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        return 0
    if args.command == "web":
        from .web import serve

        serve(host=args.host, port=args.port)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
