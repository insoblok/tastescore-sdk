/**
 * TasteScore V2 — TypeScript/JavaScript SDK (Whitepaper §8.3)
 *
 * Official TypeScript SDK for TasteScore V2 API.
 *
 * @example
 * ```ts
 * import { TasteScoreClient } from '@insoblok/tastescore-sdk';
 *
 * const client = new TasteScoreClient({
 *   apiKey: 'your-key',
 *   baseUrl: 'https://api.insoblokai.io',
 * });
 *
 * const score = await client.getScore('0x...');
 * ```
 *
 * @packageDocumentation
 */

// ─── Types ───────────────────────────────────────────────────────────────

export interface TasteScoreConfig {
  apiKey: string;
  baseUrl?: string;
  timeout?: number;
}

export interface ScoreResult {
  score: number;
  label: string;
  confidence: number;
  subScores?: {
    reputationQuality: SubScoreDetail;
    tasteCoherence: SubScoreDetail;
    influence: SubScoreDetail;
    onChainTrust: SubScoreDetail;
    trendSensitivity: SubScoreDetail;
  };
}

export interface SubScoreDetail {
  value: number;
  weight: number;
  contribution: number;
}

export interface ThresholdProof {
  proof_type: "threshold";
  threshold: number;
  above_threshold: boolean;
  commitment: string;
  proof: string;
}

export interface TierProof {
  proof_type: "tier_membership";
  allowed_tiers: string[];
  in_allowed_set: boolean;
  proof: string;
}

export interface Attestation {
  attestation_hash: string;
  input_hash: string;
  output_hash: string;
  merkle_root: string;
  score: number;
  label: string;
  model_ver: string;
}

export interface AdversarialAssessment {
  manipulation_risk: number;
  action: string;
  wash_trading: Record<string, unknown>;
  artificial_diversity: Record<string, unknown>;
  sybil_escalation: Record<string, unknown>;
}

export interface BatchResult {
  address: string;
  result?: ScoreResult;
  error?: string;
}

export interface V2Envelope<T = unknown> {
  status: string;
  version: string;
  summary: Record<string, unknown>;
  details?: T;
}

// ─── Client ──────────────────────────────────────────────────────────────

export class TasteScoreClient {
  private readonly apiKey: string;
  private readonly baseUrl: string;
  private readonly timeout: number;

  constructor(config: TasteScoreConfig) {
    this.apiKey = config.apiKey;
    this.baseUrl = (config.baseUrl || "https://api.insoblokai.io").replace(
      /\/$/,
      ""
    );
    this.timeout = config.timeout || 30_000;
  }

  // ── Internal helpers ──

  private async request<T>(
    method: string,
    path: string,
    body?: unknown
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        method,
        headers: {
          "X-API-Key": this.apiKey,
          "Content-Type": "application/json",
        },
        body: body ? JSON.stringify(body) : undefined,
        signal: controller.signal,
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`HTTP ${response.status}: ${text}`);
      }

      return (await response.json()) as T;
    } finally {
      clearTimeout(timer);
    }
  }

  // ── Core Scoring ──

  /** Get TasteScore for a wallet address. */
  async getScore(
    address: string,
    includeDetails = true
  ): Promise<V2Envelope<ScoreResult>> {
    const params = new URLSearchParams({
      address,
      include_details: String(includeDetails),
    });
    return this.request("GET", `/api/tastescore/details?${params}`);
  }

  /** Score multiple wallets concurrently (max 100). */
  async batchScore(addresses: string[]): Promise<BatchResult[]> {
    const results: BatchResult[] = [];
    const chunkSize = 10;

    for (let i = 0; i < Math.min(addresses.length, 100); i += chunkSize) {
      const chunk = addresses.slice(i, i + chunkSize);
      const promises = chunk.map(async (addr): Promise<BatchResult> => {
        try {
          const result = await this.getScore(addr);
          return { address: addr, result: result as unknown as ScoreResult };
        } catch (e: unknown) {
          return {
            address: addr,
            error: e instanceof Error ? e.message : String(e),
          };
        }
      });
      results.push(...(await Promise.all(promises)));
    }

    return results;
  }

  /** Get full dashboard data in one call. */
  async dashboard(address: string): Promise<V2Envelope> {
    return this.request(
      "GET",
      `/api/tastescore/summary?address=${encodeURIComponent(address)}`
    );
  }

  // ── History & Compliance ──

  /** Get score timeline history. */
  async getTimeline(address: string, days = 90): Promise<V2Envelope> {
    return this.request(
      "GET",
      `/api/history/timeline/${address}?days=${days}`
    );
  }

  /** Get score delta (change over time). */
  async getDelta(address: string): Promise<V2Envelope> {
    return this.request("GET", `/api/history/delta/${address}`);
  }

  /** Run compliance screening on an address. */
  async complianceScreen(address: string): Promise<V2Envelope> {
    return this.request("GET", `/api/compliance/screen/${address}`);
  }

  // ── Verifiable Scores ──

  /** Create a verifiable score attestation. */
  async createAttestation(
    address: string,
    onchain = false
  ): Promise<V2Envelope<Attestation>> {
    return this.request(
      "POST",
      `/api/verifiable/attestation/${address}?onchain=${onchain}`
    );
  }

  /** Generate a ZK threshold proof. */
  async thresholdProof(
    address: string,
    threshold = 700
  ): Promise<V2Envelope<ThresholdProof>> {
    return this.request("POST", "/api/verifiable/proof/threshold", {
      address,
      threshold,
    });
  }

  /** Generate a ZK tier membership proof. */
  async tierProof(
    address: string,
    allowedTiers = ["A", "B"]
  ): Promise<V2Envelope<TierProof>> {
    return this.request("POST", "/api/verifiable/proof/tier", {
      address,
      allowed_tiers: allowedTiers,
    });
  }

  /** Generate a ZK delta proof (score improved over period). */
  async deltaProof(address: string, days = 30): Promise<V2Envelope> {
    return this.request("POST", "/api/verifiable/proof/delta", {
      address,
      days,
    });
  }

  /** Get score explainability breakdown. */
  async explainScore(address: string): Promise<V2Envelope> {
    return this.request("GET", `/api/verifiable/explain/${address}`);
  }

  // ── Adversarial ──

  /** Run adversarial robustness assessment. */
  async adversarialAssessment(
    address: string
  ): Promise<V2Envelope<AdversarialAssessment>> {
    return this.request("POST", `/api/adversarial/assess/${address}`);
  }

  // ── Chain Breakdown ──

  /** Get per-chain activity breakdown. */
  async chainBreakdown(address: string): Promise<V2Envelope> {
    const params = new URLSearchParams({
      address,
      include_details: "true",
    });
    return this.request(
      "GET",
      `/api/tastescore/chain-breakdown?${params}`
    );
  }

  // ── Behavioural ──

  /** Get behavioural fingerprint. */
  async fingerprint(address: string): Promise<V2Envelope> {
    return this.request("GET", `/api/fingerprint/${address}`);
  }

  /** Get peer percentile ranking. */
  async peerComparison(address: string, days = 30): Promise<V2Envelope> {
    return this.request(
      "GET",
      `/api/history/peers/${address}?days=${days}`
    );
  }

  // ── Social Trust ──

  /** Get social trust panel for a platform/handle. */
  async socialTrust(platform: string, handle: string): Promise<V2Envelope> {
    return this.request("POST", "/api/social-trust/panel", {
      platform,
      handle,
    });
  }

  // ── Governance ──

  /** Get current model version and weights. */
  async modelVersion(): Promise<V2Envelope> {
    return this.request("GET", "/api/governance/model/version");
  }

  // ── GraphQL ──

  /** Execute a raw GraphQL query. */
  async graphqlQuery(
    query: string,
    variables?: Record<string, unknown>
  ): Promise<V2Envelope> {
    return this.request("POST", "/api/graphql", {
      query,
      variables: variables ?? {},
    });
  }

  /** Get score via GraphQL. */
  async graphqlScore(address: string): Promise<V2Envelope> {
    const query = `
      query GetScore($address: String!) {
        tastescore(address: $address) {
          address
          score
          label
          confidence
          subScores {
            reputationQuality { value weight contribution }
            tasteCoherence { value weight contribution }
            influence { value weight contribution }
            onChainTrust { value weight contribution }
            trendSensitivity { value weight contribution }
          }
        }
      }
    `;
    return this.graphqlQuery(query, { address });
  }

  // ── WebSocket ──

  /**
   * Subscribe to real-time score updates via WebSocket.
   *
   * @returns An object with a `close()` method to stop the subscription.
   */
  subscribe(
    address: string,
    onUpdate: (data: unknown) => void,
    onError?: (error: unknown) => void
  ): { close: () => void } {
    const wsUrl = this.baseUrl
      .replace("https://", "wss://")
      .replace("http://", "ws://");
    const ws = new WebSocket(
      `${wsUrl}/api/ws/scores/${address}`
    );

    ws.onmessage = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data as string);
        if (data.type === "score_update") {
          onUpdate(data);
        }
      } catch (e) {
        onError?.(e);
      }
    };

    ws.onerror = (event: Event) => {
      onError?.(event);
    };

    return { close: () => ws.close() };
  }
}

export default TasteScoreClient;
