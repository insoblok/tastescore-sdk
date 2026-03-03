"""
Basic TasteScore SDK usage examples.

Run: python examples/python/basic.py
"""

import os
from tastescore_sdk import TasteScoreClient

API_KEY = os.environ.get("TASTESCORE_API_KEY", "your-api-key")


def main():
    client = TasteScoreClient(
        api_key=API_KEY,
        base_url="https://api.insoblokai.io",
    )

    # 1. Single wallet score
    print("--- Single Score ---")
    score = client.get_score("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
    print(score)

    # 2. Batch scoring
    print("\n--- Batch Score ---")
    batch = client.batch_score([
        "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
        "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
    ])
    print(batch)

    # 3. ZK Threshold proof
    print("\n--- Threshold Proof ---")
    proof = client.threshold_proof(
        "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
        threshold=700,
    )
    print(proof)

    # 4. Compliance screening
    print("\n--- Compliance Screen ---")
    compliance = client.compliance_screen(
        "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    )
    print(compliance)

    # 5. Score explanation
    print("\n--- Explain Score ---")
    explain = client.explain_score(
        "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    )
    print(explain)


if __name__ == "__main__":
    main()
