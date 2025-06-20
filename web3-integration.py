# Web3 Integration pentru Verificarea Contractelor de Vesting Ethereum
from web3 import Web3
import requests
import json
import time
from typing import Dict, List, Optional, Any
import os
from datetime import datetime
import asyncio

class VestingContractAnalyzer:
    """Analizor complet pentru contractele de vesting Ethereum"""
    
    def __init__(self):
        """Inițializează analizorul cu configurația API"""
        self.infura_url = f"https://mainnet.infura.io/v3/{os.getenv('INFURA_PROJECT_ID')}"
        self.etherscan_key = os.getenv("ETHERSCAN_API_KEY") 
        self.etherscan_url = "https://api.etherscan.io/api"
        
        # Inițializează Web3
        try:
            self.w3 = Web3(Web3.HTTPProvider(self.infura_url))
            if not self.w3.is_connected():
                raise ConnectionError("Nu s-a putut conecta la rețeaua Ethereum")
        except Exception as e:
            print(f"Eroare la conectarea Web3: {e}")
            self.w3 = None
    
    def fetch_contract_abi(self, address: str) -> Optional[Dict]:
        """Obține ABI-ul contractului de pe Etherscan"""
        try:
            params = {
                "module": "contract",
                "action": "getabi", 
                "address": address,
                "apikey": self.etherscan_key
            }
            
            response = requests.get(self.etherscan_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data["status"] == "1":
                return json.loads(data["result"])
            else:
                print(f"Eroare Etherscan: {data.get('message', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"Eroare la obținerea ABI: {e}")
            return None
    
    def get_contract_functions(self, abi: List[Dict]) -> List[str]:
        """Extrage funcțiile din ABI-ul contractului"""
        if not abi:
            return []
        
        functions = []
        for item in abi:
            if item.get("type") == "function":
                functions.append(item.get("name", ""))
        
        return [f for f in functions if f]  # Remove empty strings
    
    def check_vesting_functions(self, functions: List[str]) -> Dict[str, bool]:
        """Verifică prezența funcțiilor standard de vesting"""
        vesting_functions = {
            "vestedAmount": False,
            "releasable": False, 
            "release": False,
            "released": False,
            "cliff": False,
            "duration": False,
            "start": False,
            "beneficiary": False,
            "owner": False,
            "token": False
        }
        
        for func in functions:
            func_lower = func.lower()
            for vesting_func in vesting_functions.keys():
                if vesting_func.lower() in func_lower:
                    vesting_functions[vesting_func] = True
        
        return vesting_functions
    
    def calculate_security_score(self, vesting_functions: Dict[str, bool], 
                                contract_verified: bool = True) -> int:
        """Calculează scorul de securitate pe baza funcțiilor găsite"""
        score = 0
        
        # Funcții critice (20 puncte fiecare)
        critical_functions = ["vestedAmount", "releasable", "release"]
        for func in critical_functions:
            if vesting_functions.get(func, False):
                score += 20
        
        # Funcții importante (10 puncte fiecare)  
        important_functions = ["released", "cliff", "duration", "start"]
        for func in important_functions:
            if vesting_functions.get(func, False):
                score += 10
        
        # Funcții auxiliare (5 puncte fiecare)
        auxiliary_functions = ["beneficiary", "owner", "token"]
        for func in auxiliary_functions:
            if vesting_functions.get(func, False):
                score += 5
        
        # Bonus pentru contract verificat
        if contract_verified:
            score += 5
        
        return min(score, 100)  # Cap la 100
    
    def determine_risk_level(self, score: int) -> str:
        """Determină nivelul de risc pe baza scorului"""
        if score >= 80:
            return "LOW"
        elif score >= 40:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def call_contract_function(self, contract, function_name: str, 
                              beneficiary_address: str = None) -> Any:
        """Apelează o funcție din contract cu gestionarea erorilor"""
        try:
            if not hasattr(contract.functions, function_name):
                return None
            
            func = getattr(contract.functions, function_name)
            
            # Încearcă cu adresa beneficiarului dacă este furnizată
            if beneficiary_address:
                try:
                    return func(beneficiary_address).call()
                except:
                    pass
            
            # Încearcă fără parametri
            try:
                return func().call()
            except Exception as e:
                print(f"Eroare la apelarea {function_name}: {e}")
                return None
                
        except Exception as e:
            print(f"Eroare la apelarea funcției {function_name}: {e}")
            return None
    
    def get_token_amounts(self, contract, address: str) -> Dict[str, float]:
        """Obține cantitățile de token-uri vested și released"""
        amounts = {
            "vested_amount": 0.0,
            "released_amount": 0.0,
            "releasable_amount": 0.0,
            "total_supply": 0.0
        }
        
        try:
            # Încearcă să obțină cantitatea vested
            vested = self.call_contract_function(contract, "vestedAmount", address)
            if vested is not None:
                amounts["vested_amount"] = float(vested) / 1e18  # Convert from wei
            
            # Încearcă să obțină cantitatea released  
            released = self.call_contract_function(contract, "released", address)
            if released is not None:
                amounts["released_amount"] = float(released) / 1e18
            
            # Încearcă să obțină cantitatea releasable
            releasable = self.call_contract_function(contract, "releasable", address)
            if releasable is not None:
                amounts["releasable_amount"] = float(releasable) / 1e18
            
            # Încearcă să obțină total supply din contractul token
            total_supply = self.call_contract_function(contract, "totalSupply")
            if total_supply is not None:
                amounts["total_supply"] = float(total_supply) / 1e18
            
        except Exception as e:
            print(f"Eroare la obținerea cantităților: {e}")
        
        return amounts
    
    def check_contract_verification(self, address: str) -> bool:
        """Verifică dacă contractul este verificat pe Etherscan"""
        try:
            params = {
                "module": "contract",
                "action": "getsourcecode",
                "address": address,
                "apikey": self.etherscan_key
            }
            
            response = requests.get(self.etherscan_url, params=params)
            data = response.json()
            
            if data["status"] == "1" and data["result"]:
                source_code = data["result"][0].get("SourceCode", "")
                return len(source_code) > 0
            
            return False
            
        except Exception as e:
            print(f"Eroare la verificarea contractului: {e}")
            return False
    
    def get_contract_creation_info(self, address: str) -> Dict[str, Any]:
        """Obține informații despre crearea contractului"""
        try:
            params = {
                "module": "contract",
                "action": "getcontractcreation", 
                "contractaddresses": address,
                "apikey": self.etherscan_key
            }
            
            response = requests.get(self.etherscan_url, params=params)
            data = response.json()
            
            if data["status"] == "1" and data["result"]:
                return data["result"][0]
            
            return {}
            
        except Exception as e:
            print(f"Eroare la obținerea info creație: {e}")
            return {}
    
    def analyze_contract(self, address: str, name: str = "", 
                        beneficiary_address: str = None) -> Dict[str, Any]:
        """Analizează complet un contract de vesting"""
        result = {
            "name": name or f"Contract_{address[:8]}",
            "address": address,
            "status": "error",
            "error": None,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            if not self.w3 or not self.w3.is_connected():
                raise ConnectionError("Nu există conexiune la blockchain")
            
            # Verifică dacă adresa este un contract
            code = self.w3.eth.get_code(Web3.to_checksum_address(address))
            if code == b'':
                raise ValueError("Adresa nu pare să fie un contract")
            
            # Obține ABI-ul contractului
            abi = self.fetch_contract_abi(address)
            if not abi:
                raise ValueError("Nu s-a putut obține ABI-ul contractului")
            
            # Creează obiectul contract
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(address), 
                abi=abi
            )
            
            # Analizează funcțiile
            all_functions = self.get_contract_functions(abi)
            vesting_functions = self.check_vesting_functions(all_functions)
            
            # Calculează scorul de securitate
            is_verified = self.check_contract_verification(address)
            security_score = self.calculate_security_score(vesting_functions, is_verified)
            risk_level = self.determine_risk_level(security_score)
            
            # Obține cantitățile de token-uri
            token_amounts = self.get_token_amounts(contract, beneficiary_address or address)
            
            # Obține informații despre crearea contractului
            creation_info = self.get_contract_creation_info(address)
            
            # Funcțiile găsite pentru raport
            found_functions = [k for k, v in vesting_functions.items() if v]
            
            result.update({
                "status": "success",
                "security_score": security_score,
                "risk_level": risk_level,
                "vesting_functions_found": found_functions,
                "all_functions_count": len(all_functions),
                "is_verified": is_verified,
                "creation_info": creation_info,
                **token_amounts
            })
            
        except Exception as e:
            result["error"] = str(e)
            result["security_score"] = 0
            result["risk_level"] = "ERROR"
            print(f"Eroare la analiza contractului {address}: {e}")
        
        return result
    
    def analyze_multiple_contracts(self, contracts_data: List[Dict[str, str]], 
                                  progress_callback=None) -> List[Dict[str, Any]]:
        """Analizează multiple contracte cu progress tracking"""
        results = []
        total = len(contracts_data)
        
        for i, contract_data in enumerate(contracts_data):
            address = contract_data.get("address", "")
            name = contract_data.get("name", "")
            beneficiary = contract_data.get("beneficiary", None)
            
            if progress_callback:
                progress_callback(i / total, f"Analizez {name or address[:10]}...")
            
            result = self.analyze_contract(address, name, beneficiary)
            results.append(result)
            
            # Rate limiting pentru API-urile publice
            time.sleep(0.2)  # 200ms delay între cereri
        
        if progress_callback:
            progress_callback(1.0, "Analiza completă!")
        
        return results

# ── INTEGRARE CU GRADIO ──────────────────────────────────────────────────────────

def create_analyzer_instance():
    """Creează o instanță a analizorului cu verificarea configurației"""
    try:
        analyzer = VestingContractAnalyzer()
        
        # Testează conexiunea
        if analyzer.w3 and analyzer.w3.is_connected():
            latest_block = analyzer.w3.eth.block_number
            print(f"✅ Conectat la Ethereum. Ultimul bloc: {latest_block}")
            return analyzer
        else:
            print("❌ Nu s-a putut conecta la rețeaua Ethereum")
            return None
            
    except Exception as e:
        print(f"❌ Eroare la inițializarea analizorului: {e}")
        return None

def real_analyze_contracts(addresses_text: str, names_text: str = "", 
                          network: str = "Mainnet", progress=None) -> tuple:
    """Funcție de analiză reală pentru integrarea cu Gradio"""
    
    # Creează analizorul
    analyzer = create_analyzer_instance()
    if not analyzer:
        return ("❌ Nu s-a putut inițializa analizorul. Verifică cheile API.", 
                None, None, None, None)
    
    if not addresses_text.strip():
        return ("⚠️ Vă rugăm să introduceți cel puțin o adresă de contract.", 
                None, None, None, None)
    
    # Parsează datele de intrare
    addresses = [addr.strip() for addr in addresses_text.strip().split('\n') if addr.strip()]
    names = [name.strip() for name in names_text.strip().split('\n') if name.strip()] if names_text else []
    
    # Validează adresele Ethereum
    invalid_addresses = []
    for addr in addresses:
        try:
            Web3.to_checksum_address(addr)
        except:
            invalid_addresses.append(addr)
    
    if invalid_addresses:
        return (f"❌ Adrese invalide: {', '.join(invalid_addresses[:3])}", 
                None, None, None, None)
    
    # Pregătește datele pentru analiză
    contracts_data = []
    for i, address in enumerate(addresses):
        contracts_data.append({
            "address": address,
            "name": names[i] if i < len(names) else f"Contract_{i+1}"
        })
    
    # Funcție de callback pentru progress
    def progress_callback(progress_val, desc):
        if progress:
            progress(progress_val, desc=desc)
    
    # Efectuează analiza
    try:
        results = analyzer.analyze_multiple_contracts(contracts_data, progress_callback)
        
        # Importă funcțiile de generare din modulul principal
        from gradio_vesting_app import (
            generate_summary_report, 
            create_security_scores_chart,
            create_token_distribution_chart, 
            create_risk_distribution_chart,
            create_detailed_table
        )
        
        # Generează outputurile
        summary = generate_summary_report(results)
        security_chart = create_security_scores_chart(results)
        distribution_chart = create_token_distribution_chart(results)
        risk_chart = create_risk_distribution_chart(results)
        details_table = create_detailed_table(results)
        
        return summary, security_chart, distribution_chart, risk_chart, details_table
        
    except Exception as e:
        return (f"❌ Eroare în timpul analizei: {str(e)}", 
                None, None, None, None)

# ── TESTARE ȘI DEBUGGING ─────────────────────────────────────────────────────────

def test_analyzer():
    """Testează funcționalitatea analizorului"""
    print("🧪 Testez analizorul de contracte vesting...")
    
    analyzer = create_analyzer_instance()
    if not analyzer:
        print("❌ Testul a eșuat - nu s-a putut crea analizorul")
        return False
    
    # Testează cu o adresă cunoscută
    test_address = "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"  # UNI Token
    print(f"📋 Testez cu adresa: {test_address}")
    
    try:
        result = analyzer.analyze_contract(test_address, "UNI_Test")
        print(f"✅ Test reușit!")
        print(f"   Status: {result['status']}")
        print(f"   Scor securitate: {result.get('security_score', 'N/A')}")
        print(f"   Nivel risc: {result.get('risk_level', 'N/A')}")
        print(f"   Funcții găsite: {len(result.get('vesting_functions_found', []))}")
        return True
        
    except Exception as e:
        print(f"❌ Test eșuat: {e}")
        return False

if __name__ == "__main__":
    # Rulează testul dacă scriptul este executat direct
    test_analyzer()