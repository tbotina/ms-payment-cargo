import json 
from dotenv import load_dotenv
from epaycosdk.epayco import Epayco
from flask import Flask, request, jsonify
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
epayco = Epayco({
    "apiKey": os.getenv("EPAYCO_PUBLIC_KEY"),
    "privateKey": os.getenv("EPAYCO_PRIVATE_KEY"),
    "lenguage": "ES",
    "test": os.getenv("EPAYCO_TEST") == "True" 
})

def create_token(data):
    print(data)
    try:
        print("Entro al create_token")
        card_info = {
            "card[number]": data["card_number"],
            "card[exp_year]": data["exp_year"],
            "card[exp_month]": data["exp_month"],
            "card[cvc]": data["cvc"],
            "hasCvv": True
        }
        token= epayco.token.create(card_info)
        print("Token generado", token)
        return token
    except Exception as e:
        return {"error al crear token": str(e)}

def create_customer(token, data):
    customer_info = {
        "name": data["name"],
        "last_name": data["last_name"],
        "email": data["email"],
        "phone": data["phone"],
        "default": True
    }
    customer_info["token_card"] = token
    try:
        customer = epayco.customer.create(customer_info)
        return customer
    except Exception as e:
        return {"error al crear el usuario": str(e)}

def process_payment(data, customer_id, token_card):
    try:
        payment_info = {
            "token_card": token_card,
            "customer_id": customer_id,
            "doc_type": "CC",
            "doc_number": data["doc_number"],
            "name": data["name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "city": data["city"],
            "address": data["address"],
            "phone": data["phone"],
            "cell_phone": data["cell_phone"],
            "bill": data["bill"],
            "description": "Pago servicio de transporte",
            "value": data["value"],
            "tax": 0,
            "tax_base": data["value"],
            "currency": "COP"
        }
        response= epayco.charge.create(payment_info)
        return response
    except Exception as e:
        return {"error al procesar el pago": str(e)}
    
@app.route("/process-payment", methods=["POST"])
def handle_process_payment():
    data = request.json
    token_response = create_token(data)
    print("Token response", json.dumps(token_response))

    if token_response["status"] is False:
        return jsonify(token_response), 500
    token_card = token_response["id"]

    customer_response = create_customer(token_card, data)
    print("Customer response", json.dumps(customer_response))

    if "error" in customer_response:
        return jsonify(customer_response), 500

    customer_id = customer_response["data"]["customerId"]

    payment_response = process_payment(data, customer_id, token_card)
    print("Payment response", json.dumps(payment_response))

    if "error" in payment_response:
        return jsonify(payment_response), 500
    
    return jsonify(payment_response), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)