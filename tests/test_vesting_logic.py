import pandas as pd
import vesting_logic

class DummyAnalyzer:
    def __init__(self, network):
        self.network = network
    def analyze_contracts(self, addresses, names):
        return [{
            "Contract": "Test",
            "Address": addresses[0],
            "Vested": 100,
            "Released": 10,
            "Security Score": 80
        }]
    def generate_security_chart(self, results):
        return "security_chart"
    def generate_token_chart(self, results):
        return "token_chart"

def test_analyze_vesting_contracts(monkeypatch):
    monkeypatch.setattr(vesting_logic, "VestingAnalyzer", DummyAnalyzer)
    df, security_plot, token_plot = vesting_logic.analyze_vesting_contracts(
        "0xabc", "Test", "mainnet"
    )
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["Contract"] == "Test"
    assert security_plot == "security_chart"
    assert token_plot == "token_chart"
