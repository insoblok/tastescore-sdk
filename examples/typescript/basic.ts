import { TasteScoreClient } from '@insoblok/tastescore-sdk';

/**
 * Basic TasteScore SDK usage examples.
 *
 * Run: npx tsx examples/typescript/basic.ts
 */

const API_KEY = process.env.TASTESCORE_API_KEY || 'your-api-key';

async function main() {
  const client = new TasteScoreClient({
    apiKey: API_KEY,
    baseUrl: 'https://api.insoblokai.io',
  });

  // 1. Single wallet score
  console.log('--- Single Score ---');
  const score = await client.getScore('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045');
  console.log(JSON.stringify(score, null, 2));

  // 2. Batch scoring
  console.log('\n--- Batch Score ---');
  const batch = await client.batchScore([
    '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
    '0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B',
  ]);
  console.log(JSON.stringify(batch, null, 2));

  // 3. ZK Threshold proof
  console.log('\n--- Threshold Proof ---');
  const proof = await client.thresholdProof('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045', 700);
  console.log(JSON.stringify(proof, null, 2));

  // 4. Compliance screening
  console.log('\n--- Compliance Screen ---');
  const compliance = await client.complianceScreen('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045');
  console.log(JSON.stringify(compliance, null, 2));

  // 5. Score explanation
  console.log('\n--- Explain Score ---');
  const explain = await client.explainScore('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045');
  console.log(JSON.stringify(explain, null, 2));

  // 6. WebSocket streaming (subscribe for 10 seconds)
  console.log('\n--- WebSocket Stream (10s) ---');
  const sub = client.subscribe(
    '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
    (data) => console.log('Update:', data),
    (err) => console.error('Error:', err),
  );
  setTimeout(() => {
    sub.close();
    console.log('Stream closed.');
  }, 10_000);
}

main().catch(console.error);
