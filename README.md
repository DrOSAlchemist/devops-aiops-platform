# End-to-End DevOps + AIOps Platform

A small incident classifier API plus Kubernetes deployment and Prometheus alert rules. It turns operational signals into triage labels, a safe starting point for AIOps workflows.

## Run locally

```bash
python3 app.py
curl -X POST localhost:8080/incidents -H 'Content-Type: application/json' -d '{"latency_ms":1500,"error_rate":0.08,"cpu_pct":92}'
```

## Production path

Apply `manifests.yaml`, scrape `/metrics` with Prometheus, and route alerts through Alertmanager. Replace heuristic triage with a reviewed model only after collecting labeled incidents.
