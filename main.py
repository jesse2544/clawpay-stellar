import os
from flask import Flask, request, jsonify
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset
from openclaw import Agent
from anthropic import Anthropic

app = Flask(_name_)
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    user_prompt = request.json.get('prompt')
    # x402: Return 402 Payment Required if no payment header
    if not request.headers.get('X-Payment'):
        return jsonify({
            "error": "Payment Required", 
            "price": "0.01 USDC",
            "pay_to": os.getenv("STELLAR_ADDRESS"),
            "network": "testnet"
        }), 402
    
    # If paid, call Claude via OpenClaw agent
    msg = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return jsonify({"reply": msg.content[0].text})

if _name_ == '_main_':
    app.run(port=5000)