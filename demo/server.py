#!/usr/bin/env python3
"""Small local demo server for the shipping calculator HTML wrapper."""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
INDEX = Path(__file__).with_name("index.html")

sys.path.insert(0, str(SRC))

from shipping_calculator import calculate_shipping_cost  # noqa: E402


class DemoHandler(BaseHTTPRequestHandler):
    """Serve the HTML form and expose an API backed by calculate_shipping_cost."""

    def do_GET(self) -> None:
        if urlparse(self.path).path not in {"/", "/index.html"}:
            self._send_json({"error": "Not found"}, status=404)
            return

        content = INDEX.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/calculate":
            self._send_json({"error": "Not found"}, status=404)
            return

        try:
            payload = self._read_json()
            cost = calculate_shipping_cost(
                weight_kg=float(payload["weight_kg"]),
                distance_km=float(payload["distance_km"]),
                delivery_type=str(payload["delivery_type"]),
                customer_type=str(payload["customer_type"]),
                area_type=str(payload["area_type"]),
            )
        except KeyError as exc:
            self._send_json({"error": f"Missing field: {exc.args[0]}"}, status=400)
            return
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            self._send_json({"error": str(exc)}, status=400)
            return

        self._send_json({"cost": cost})

    def log_message(self, format: str, *args: object) -> None:
        return

    def _read_json(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length)
        return json.loads(raw_body.decode("utf-8"))

    def _send_json(self, payload: dict[str, object], status: int = 200) -> None:
        content = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def main() -> int:
    host = "127.0.0.1"
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer((host, port), DemoHandler)
    print(f"Demo available at http://{host}:{port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
