# @insoblok/tastescore-sdk

Official TypeScript/JavaScript SDK for the [TasteScore V2 API](https://api.insoblokai.io) — crypto wallet reputation scoring.

## Installation

```bash
npm install @insoblok/tastescore-sdk
# or
yarn add @insoblok/tastescore-sdk
# or
pnpm add @insoblok/tastescore-sdk
```

## Quick Start

```typescript
import { TasteScoreClient } from '@insoblok/tastescore-sdk';

const client = new TasteScoreClient({
  apiKey: 'your-api-key',
});

// Get a wallet's TasteScore
const result = await client.getScore('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045');
console.log(result);

// Batch scoring (up to 100 addresses, 10 concurrent)
const results = await client.batchScore([
  '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
  '0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B',
]);

// ZK threshold proof
const proof = await client.thresholdProof('0x...', 700);

// Compliance screening
const screen = await client.complianceScreen('0x...');
```

## WebSocket Streaming

```typescript
const sub = client.subscribe(
  '0x...',
  (update) => console.log('Score update:', update),
  (error) => console.error('Error:', error),
);

// Later: stop streaming
sub.close();
```

## API Reference

### Constructor

```typescript
const client = new TasteScoreClient({
  apiKey: 'your-key',                       // required
  baseUrl: 'https://api.insoblokai.io',     // optional (default)
  timeout: 30000,                           // optional, ms (default: 30s)
});
```

### Methods

| Method | Description |
|--------|-------------|
| `getScore(address, includeDetails?)` | Get TasteScore for a wallet |
| `batchScore(addresses)` | Score multiple wallets concurrently |
| `dashboard(address)` | Full dashboard data in one call |
| `getTimeline(address, days?)` | Score history timeline |
| `getDelta(address)` | Score change over time |
| `complianceScreen(address)` | Sanctions & compliance check |
| `createAttestation(address, onchain?)` | Verifiable score attestation |
| `thresholdProof(address, threshold?)` | ZK threshold proof |
| `tierProof(address, allowedTiers?)` | ZK tier membership proof |
| `deltaProof(address, days?)` | ZK delta proof |
| `explainScore(address)` | Score explainability breakdown |
| `adversarialAssessment(address)` | Adversarial robustness check |
| `chainBreakdown(address)` | Per-chain activity breakdown |
| `fingerprint(address)` | Behavioural fingerprint |
| `peerComparison(address, days?)` | Peer percentile ranking |
| `socialTrust(platform, handle)` | Social trust panel |
| `modelVersion()` | Current model version & weights |
| `graphqlQuery(query, variables?)` | Raw GraphQL query |
| `graphqlScore(address)` | Score via GraphQL |
| `subscribe(address, onUpdate, onError?)` | WebSocket score streaming |

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

Alternative formats: `?format=iso20022`, `?format=casa`, `?format=openrisk`.

## Requirements

- Node.js 18+ (uses native `fetch` and `WebSocket`)
- Works in modern browsers, Deno, Bun, and Cloudflare Workers

## License

MIT — © 2025-2026 InSoBlok
