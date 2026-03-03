"""
TasteScore SDK — Official Python client for TasteScore V2 API.

Usage:
    from tastescore_sdk import TasteScoreClient, AsyncTasteScoreClient

    client = TasteScoreClient(api_key="your-key")
    result = client.get_score("0x...")
"""

from tastescore_sdk.client import AsyncTasteScoreClient, TasteScoreClient

__version__ = "0.1.0"
__all__ = ["TasteScoreClient", "AsyncTasteScoreClient", "__version__"]
