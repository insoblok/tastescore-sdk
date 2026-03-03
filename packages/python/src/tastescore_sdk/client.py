"""
TasteScore V2 — Python SDK Client (Whitepaper §8.3)

Official Python SDK for TasteScore V2 API.
Supports REST, GraphQL, WebSocket, and batch operations.

Usage:
    from tastescore_sdk import TasteScoreClient

    client = TasteScoreClient(api_key="your-key", base_url="https://api.insoblokai.io")

    # Single score
    result = client.get_score("0x...")

    # Batch scores
    results = client.batch_score(["0x...", "0x..."])

    # Threshold proof
    proof = client.threshold_proof("0x...", threshold=700)

    # WebSocket streaming
    async for score in client.subscribe("0x..."):
        print(score)
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TasteScoreClient:
    """
    TasteScore V2 Python SDK — synchronous client.

    Wraps REST and GraphQL API endpoints for easy integration.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.insoblokai.io",
        timeout: int = 30,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = None

    def _get_session(self):
        if self._session is None:
            import requests

            self._session = requests.Session()
            self._session.headers.update(
                {
                    "X-API-Key": self.api_key,
                    "Content-Type": "application/json",
                }
            )
        return self._session

    def _get(self, path: str, params: Optional[dict] = None) -> dict:
        """Make a GET request."""
        session = self._get_session()
        resp = session.get(
            f"{self.base_url}{path}",
            params=params,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, data: Optional[dict] = None) -> dict:
        """Make a POST request."""
        session = self._get_session()
        resp = session.post(
            f"{self.base_url}{path}",
            json=data or {},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()

    # ----- Core Scoring -----

    def get_score(self, address: str, include_details: bool = True) -> dict:
        """
        Get TasteScore for a wallet address.

        Args:
            address: Wallet address (EVM / BTC / SOL / TRX / TON)
            include_details: Include detailed sub-scores

        Returns:
            Score result with score, label, confidence, sub-scores
        """
        return self._get(
            "/api/tastescore/details",
            params={
                "address": address,
                "include_details": str(include_details).lower(),
            },
        )

    def batch_score(
        self, addresses: List[str], max_concurrent: int = 10
    ) -> List[dict]:
        """
        Get TasteScores for multiple addresses.

        Args:
            addresses: List of wallet addresses (max 100)
            max_concurrent: Max concurrent requests

        Returns:
            List of score results
        """
        results = []
        for addr in addresses[:100]:
            try:
                result = self.get_score(addr)
                results.append({"address": addr, "result": result, "error": None})
            except Exception as e:
                results.append({"address": addr, "result": None, "error": str(e)})
        return results

    # ----- Dashboard -----

    def dashboard(self, address: str) -> dict:
        """Get full dashboard data in one call."""
        return self._get(
            "/api/tastescore/summary",
            params={"address": address},
        )

    # ----- History & Compliance -----

    def get_timeline(self, address: str, days: int = 90) -> dict:
        """Get score timeline history."""
        return self._get(
            f"/api/history/timeline/{address}",
            params={"days": days},
        )

    def get_delta(self, address: str) -> dict:
        """Get score delta (change over time)."""
        return self._get(f"/api/history/delta/{address}")

    def compliance_screen(self, address: str) -> dict:
        """Run compliance screening on an address."""
        return self._get(f"/api/compliance/screen/{address}")

    # ----- Verifiable Scores -----

    def create_attestation(self, address: str, onchain: bool = False) -> dict:
        """Create a verifiable score attestation."""
        return self._post(
            f"/api/verifiable/attestation/{address}",
            data={"onchain": onchain},
        )

    def threshold_proof(self, address: str, threshold: int = 700) -> dict:
        """Generate a ZK threshold proof."""
        return self._post(
            "/api/verifiable/proof/threshold",
            data={"address": address, "threshold": threshold},
        )

    def tier_proof(
        self, address: str, allowed_tiers: Optional[List[str]] = None
    ) -> dict:
        """Generate a ZK tier membership proof."""
        return self._post(
            "/api/verifiable/proof/tier",
            data={
                "address": address,
                "allowed_tiers": allowed_tiers or ["A", "B"],
            },
        )

    def delta_proof(self, address: str, days: int = 30) -> dict:
        """Generate a ZK delta proof (score improved over period)."""
        return self._post(
            "/api/verifiable/proof/delta",
            data={"address": address, "days": days},
        )

    def explain_score(self, address: str) -> dict:
        """Get score explainability breakdown."""
        return self._get(f"/api/verifiable/explain/{address}")

    # ----- Adversarial -----

    def adversarial_assessment(self, address: str) -> dict:
        """Run adversarial robustness assessment."""
        return self._post(f"/api/adversarial/assess/{address}")

    # ----- Chain Breakdown -----

    def chain_breakdown(self, address: str) -> dict:
        """Get per-chain activity breakdown."""
        return self._get(
            "/api/tastescore/chain-breakdown",
            params={"address": address, "include_details": "true"},
        )

    # ----- Behavioural -----

    def fingerprint(self, address: str) -> dict:
        """Get behavioural fingerprint."""
        return self._get(f"/api/fingerprint/{address}")

    def peer_comparison(self, address: str, days: int = 30) -> dict:
        """Get peer percentile ranking."""
        return self._get(
            f"/api/history/peers/{address}",
            params={"days": days},
        )

    # ----- Social Trust -----

    def social_trust(self, platform: str, handle: str) -> dict:
        """Get social trust panel for a platform/handle."""
        return self._post(
            "/api/social-trust/panel",
            data={"platform": platform, "handle": handle},
        )

    # ----- Governance -----

    def model_version(self) -> dict:
        """Get current model version and weights."""
        return self._get("/api/governance/model/version")

    def close(self):
        """Close the HTTP session."""
        if self._session:
            self._session.close()
            self._session = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    # ----- GraphQL -----

    def graphql_query(
        self, query: str, variables: Optional[dict] = None
    ) -> dict:
        """Execute a raw GraphQL query."""
        return self._post(
            "/api/graphql",
            data={"query": query, "variables": variables or {}},
        )

    def graphql_score(self, address: str) -> dict:
        """Get score via GraphQL."""
        query = """
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
        """
        return self.graphql_query(query, {"address": address})


class AsyncTasteScoreClient:
    """
    TasteScore V2 Python SDK — async client.

    Same API as TasteScoreClient but uses aiohttp for async operations.
    Requires ``pip install tastescore-sdk[async]``.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.insoblokai.io",
        timeout: int = 30,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = None

    async def _get_session(self):
        if self._session is None:
            try:
                import aiohttp

                self._session = aiohttp.ClientSession(
                    headers={
                        "X-API-Key": self.api_key,
                        "Content-Type": "application/json",
                    },
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                )
            except ImportError:
                raise ImportError(
                    "aiohttp required for async client: "
                    "pip install tastescore-sdk[async]"
                )
        return self._session

    async def _get(self, path: str, params: Optional[dict] = None) -> dict:
        session = await self._get_session()
        async with session.get(
            f"{self.base_url}{path}", params=params
        ) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def _post(self, path: str, data: Optional[dict] = None) -> dict:
        session = await self._get_session()
        async with session.post(
            f"{self.base_url}{path}", json=data or {}
        ) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def get_score(self, address: str) -> dict:
        """Get TasteScore for a wallet address."""
        return await self._get(
            "/api/tastescore/details",
            params={"address": address},
        )

    async def batch_score(self, addresses: List[str]) -> List[dict]:
        """Score multiple wallets concurrently."""
        tasks = [self.get_score(addr) for addr in addresses[:100]]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [
            {
                "address": addr,
                "result": r if not isinstance(r, Exception) else None,
                "error": str(r) if isinstance(r, Exception) else None,
            }
            for addr, r in zip(addresses, results)
        ]

    async def subscribe(self, address: str):
        """
        Subscribe to real-time score updates via WebSocket.

        Yields score update dicts as they arrive.
        Requires ``pip install tastescore-sdk[websocket]``.
        """
        try:
            import websockets
        except ImportError:
            raise ImportError(
                "websockets required: pip install tastescore-sdk[websocket]"
            )

        ws_url = self.base_url.replace("https://", "wss://").replace(
            "http://", "ws://"
        )
        async with websockets.connect(
            f"{ws_url}/api/ws/scores/{address}",
            extra_headers={"X-API-Key": self.api_key},
        ) as ws:
            async for message in ws:
                data = json.loads(message)
                if data.get("type") == "score_update":
                    yield data

    async def close(self):
        """Close the HTTP session."""
        if self._session:
            await self._session.close()
            self._session = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
