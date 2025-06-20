"""Utility script to analyze a single vesting contract."""

import argparse
import os
from dotenv import load_dotenv
from web3_integration import VestingContractAnalyzer


def main() -> None:
    """Run the analyzer for a single contract."""

    parser = argparse.ArgumentParser(description="Analyze a vesting contract")
    parser.add_argument("address", help="Contract address")
    parser.add_argument(
        "-b", "--beneficiary", dest="beneficiary", default=None,
        help="Beneficiary address (optional)"
    )
    parser.add_argument(
        "-n", "--network", dest="network", default="mainnet",
        help="Ethereum network to use (default: mainnet)"
    )
    args = parser.parse_args()

    # Load API keys from .env or environment variables
    load_dotenv()

    analyzer = VestingContractAnalyzer(args.network)
    result = analyzer.analyze_contract(
        args.address,
        name="CustomToken",
        beneficiary_address=args.beneficiary,
    )

    print("--- Vesting Contract Analysis ---")
    for key, val in result.items():
        print(f"{key}: {val}")


if __name__ == "__main__":
    main()
