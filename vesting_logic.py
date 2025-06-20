import json
import time
import plotly.express as px
import pandas as pd
from web3_connector import Web3Connector

class VestingAnalyzer:
    def __init__(self, network="mainnet"):
        self.web3_conn = Web3Connector(network)
        
    def analyze_contracts(self, addresses, names=None):
        results = []
        for i, address in enumerate(addresses):
            name = names[i] if names and i < len(names) else f"Contract_{i+1}"
            try:
                contract_data = self.web3_conn.get_vesting_data(address)
                results.append({
                    "Contract": name,
                    "Address": address,
                    "Vested": contract_data['vested'],
                    "Released": contract_data['released'],
                    "Security Score": self.calculate_security_score(contract_data)
                })
            except Exception as e:
                print(f"Error analyzing {address}: {str(e)}")
                results.append({
                    "Contract": name,
                    "Address": address,
                    "Vested": 0,
                    "Released": 0,
                    "Security Score": 0
                })
        return results
    
    def calculate_security_score(self, contract_data):
        score = 0
        if 'vestedAmount' in contract_data['functions']: score += 30
        if 'releasable' in contract_data['functions']: score += 25
        if 'cliff' in contract_data['functions']: score += 20
        if 'beneficiary' in contract_data['functions']: score += 15
        if 'start' in contract_data['functions']: score += 10
        return score
    
    def generate_security_chart(self, results):
        df = pd.DataFrame(results)
        fig = px.bar(
            df,
            x='Contract',
            y='Security Score',
            color='Security Score',
            color_continuous_scale=["red", "yellow", "green"],
            title="Contract Security Scores"
        )
        fig.update_layout(yaxis_range=[0,100])
        return fig
    
    def generate_token_chart(self, results):
        df = pd.DataFrame(results)
        fig = px.pie(
            df,
            names='Contract',
            values='Vested',
            title="Token Distribution",
            hole=0.4
        )
        return fig

def analyze_vesting_contracts(contracts_text, names_text, network):
    addresses = [addr.strip() for addr in contracts_text.split('\n') if addr.strip()]
    names = [name.strip() for name in names_text.split(',')] if names_text else None
    
    analyzer = VestingAnalyzer(network.lower())
    results = analyzer.analyze_contracts(addresses, names)
    
    df = pd.DataFrame(results)
    security_plot = analyzer.generate_security_chart(results)
    token_plot = analyzer.generate_token_chart(results)
    
    return df, security_plot, token_plot
