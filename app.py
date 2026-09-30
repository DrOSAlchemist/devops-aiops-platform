#!/usr/bin/env python3
"""Dependency-free AIOps triage service for local demos."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


def classify(signal: dict) -> dict:
    latency = signal.get("latency_ms", 0)
    errors = signal.get("error_rate", 0)
    cpu = signal.get("cpu_pct", 0)
    if errors >= 0.05:
        return {"severity": "critical", "runbook": "check-rollout-and-dependency-health"}
    if latency >= 1000 or cpu >= 90:
        return {"severity": "warning", "runbook": "inspect-capacity-and-hpa"}
    return {"severity": "info", "runbook": "continue-monitoring"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            self.send_response(200); self.end_headers()
            self.wfile.write(b"aiops_service_up 1\n")
            return
        self.send_error(404)

    def do_POST(self):
        if self.path != "/incidents":
            self.send_error(404); return
        size = int(self.headers.get("Content-Length", 0))
        result = classify(json.loads(self.rfile.read(size)))
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps(result).encode())


HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
