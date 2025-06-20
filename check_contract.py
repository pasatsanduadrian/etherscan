import os
from dotenv import load_dotenv
from web3_integration import VestingContractAnalyzer


def main():
    # Load API keys from .env or environment variables
    load_dotenv()

    contract_address = "0xefc814a4c676a7314a13954e283de6cef597e6b2"
    beneficiary_address = "0xd725eb7ff3f1962675109e6fc24f2060133d949a"

    # Change network if needed (mainnet by default)
    analyzer = VestingContractAnalyzer("mainnet")

    result = analyzer.analyze_contract(contract_address,
                                       name="CustomToken",
                                       beneficiary_address=beneficiary_address)

    print("--- Vesting Contract Analysis ---")
    for key, val in result.items():
        print(f"{key}: {val}")


if __name__ == "__main__":
    main()
