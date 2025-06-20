import gradio as gr
from vesting_logic import analyze_vesting_contracts
import os
from dotenv import load_dotenv

load_dotenv()

def create_interface():
    with gr.Blocks(theme=gr.themes.Soft(), title="Vesting Analyzer") as app:
        gr.Markdown("## 🔍 Ethereum Vesting Contract Analyzer")
        
        with gr.Row():
            contracts_input = gr.Textbox(
                label="Contract Addresses",
                placeholder="Enter one address per line",
                lines=5
            )
            names_input = gr.Textbox(
                label="Contract Names (Optional)",
                placeholder="Enter names separated by commas",
                lines=5
            )
        
        network_dropdown = gr.Dropdown(
            label="Network",
            choices=["Mainnet", "Goerli", "Polygon"],
            value="Mainnet"
        )
        
        analyze_btn = gr.Button("Analyze Contracts", variant="primary")
        
        with gr.Tab("Results"):
            results_output = gr.Dataframe(
                headers=["Contract", "Address", "Vested", "Released", "Security Score"],
                datatype=["str", "str", "number", "number", "number"]
            )
        
        with gr.Tab("Charts"):
            security_plot = gr.Plot()
            token_distribution = gr.Plot()
        
        analyze_btn.click(
            fn=analyze_vesting_contracts,
            inputs=[contracts_input, names_input, network_dropdown],
            outputs=[results_output, security_plot, token_distribution]
        )
    
    return app

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(server_name="0.0.0.0", server_port=7860, share=True)
