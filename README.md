# TasteScore SDK

Official SDKs for the [TasteScore V2 API](https://api.insoblokai.io) — universal wallet reputation scoring for Web3.

[![TypeScript](https://img.shields.io/npm/v/@insoblok/tastescore-sdk?label=%40insoblok%2Ftastescore-sdk&color=blue)](https://www.npmjs.com/package/@insoblok/tastescore-sdk)
[![Python](https://img.shields.io/pypi/v/tastescore-sdk?label=tastescore-sdk&color=blue)](https://pypi.org/project/tastescore-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Packages

| Package | Language | Install |
|---------|----------|---------|
| [`@insoblok/tastescore-sdk`](packages/typescript/) | TypeScript / JavaScript | `npm install @insoblok/tastescore-sdk` |
| [`tastescore-sdk`](packages/python/) | Python | `pip install tastescore-sdk` |

## Quick Start

### TypeScript

```typescript
import { TasteScoreClient } from '@insoblok/tastescore-sdk';

const client = new TasteScoreClient({ apiKey: 'your-key' });

const result = await client.getScore('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045');
console.log(result);
```

### Python

```python
from tastescore_sdk import TasteScoreClient

client = TasteScoreClient(api_key="your-key")

result = client.get_score("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
print(result)
```

## Features

- **Core Scoring** — Single wallet or batch scoring (up to 100 addresses)
- **ZK Proofs** — Threshold, tier membership & delta proofs
- **Compliance** — Sanctions screening & verifiable attestations
- **Analytics** — Timeline history, peer comparison, chain breakdown
- **Social Trust** — Cross-platform social reputation signals
- **Real-time** — WebSocket streaming for live score updates
- **GraphQL** — Full GraphQL query support
- **Multi-format** — ISO 20022, CASA, OpenRisk response formats

## API Endpoints

All SDKs wrap the TasteScore V2 REST API:

| Category | Methods |
|----------|---------|
| Scoring | `getScore`, `batchScore`, `dashboard` |
| History | `getTimeline`, `getDelta` |
| Compliance | `complianceScreen` |
| Verifiable | `createAttestation`, `thresholdProof`, `tierProof`, `deltaProof`, `explainScore` |
| Adversarial | `adversarialAssessment` |
| Analytics | `chainBreakdown`, `fingerprint`, `peerComparison` |
| Social | `socialTrust` |
| Governance | `modelVersion` |
| GraphQL | `graphqlQuery`, `graphqlScore` |
| Streaming | `subscribe` (WebSocket) |

## Response Format

All responses follow the TasteScore V2 envelope:

```json
{
  "status": "success",
  "version": "2.0",
  "summary": { ... },
  "details": { ... }
}
```

Alternative formats: append `?format=iso20022`, `?format=casa`, or `?format=openrisk`.

## Documentation

- [API Reference](https://portal.insoblokai.io/api)
- [Whitepaper](https://portal.insoblokai.io/whitepaper)
- [TasteScore Portal](https://portal.insoblokai.io)

## License

MIT — © 2025-2026 InSoBlok
