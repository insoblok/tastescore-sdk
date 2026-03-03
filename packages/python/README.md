# TasteScore Python SDK

Official Python SDK for the [TasteScore V2 API](https://api.insoblokai.io) — crypto wallet reputation scoring.

## Installation

```bash
pip install tastescore-sdk
```

With async support:
```bash
pip install tastescore-sdk[async]
```

With WebSocket streaming:
```bash
pip install tastescore-sdk[all]
```

## Quick Start

```python
from tastescore_sdk import TasteScoreClient

client = TasteScoreClient(api_key="your-api-key")

# Get a wallet's TasteScore
result = client.get_score("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
print(result)

# Batch scoring
results = client.batch_score([
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
])

# ZK threshold proof
proof = client.threshold_proof("0x...", threshold=700)

# Compliance screening
screen = client.compliance_screen("0x...")
```

## Async Client

```python
import asyncio
from tastescore_sdk import AsyncTasteScoreClient

async def main():
    client = AsyncTasteScoreClient(api_key="your-api-key")

    score = await client.get_score("0x...")

    # Real-time WebSocket streaming
    async for update in client.subscribe("0x..."):
        print(update)

    await client.close()

asyncio.run(main())
```

## API Reference

### `TasteScoreClient` (synchronous)

| Method | Description |
|--------|-------------|
| `get_score(address)` | Get TasteScore for a wallet |
| `batch_score(addresses)` | Score multiple wallets |
| `dashboard(address)` | Full dashboard data |
| `get_timeline(address, days)` | Score history timeline |
| `get_delta(address)` | Score change over time |
| `compliance_screen(address)` | Sanctions & compliance check |
| `create_attestation(address)` | Verifiable score attestation |
| `threshold_proof(address, threshold)` | ZK threshold proof |
| `tier_proof(address, tiers)` | ZK tier membership proof |
| `delta_proof(address, days)` | ZK delta proof |
| `explain_score(address)` | Score explainability breakdown |
| `adversarial_assessment(address)` | Adversarial robustness check |
| `chain_breakdown(address)` | Per-chain activity breakdown |
| `fingerprint(address)` | Behavioural fingerprint |
| `peer_comparison(address, days)` | Peer percentile ranking |
| `social_trust(platform, handle)` | Social trust panel |
| `model_version()` | Current model version & weights |
| `graphql_query(query, variables)` | Raw GraphQL query |
| `graphql_score(address)` | Score via GraphQL |

### `AsyncTasteScoreClient`

Same API as above, plus:

| Method | Description |
|--------|-------------|
| `subscribe(address)` | WebSocket score streaming (async generator) |

## Requirements

- Python 3.9+
- `requests` (sync client)
- `aiohttp` (async client, optional)
- `websockets` (streaming, optional)

## License

MIT — © 2025-2026 InSoBlok
