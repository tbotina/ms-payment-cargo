import requests

# Datos de autenticación y URL de la API de ePayco
url = "https://secure.epayco.co/validation/v1/reference"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <private_key>'  # Reemplazar con tu private_key
}

# Datos de la solicitud de pago
data = {
    "public_key": "<public_key>",  # Reemplazar con tu public_key
    "card_number": "4575623182290326",  # Número de tarjeta de prueba de ePayco
    "card_exp_year": "22",  # Año de expiración (dos dígitos)
    "card_exp_month": "12",  # Mes de expiración
    "card_cvc": "123",  # Código de seguridad de la tarjeta
    "doc_type": "CC",  # Tipo de documento (CC: cédula de ciudadanía, TI: tarjeta de identidad)
    "doc_number": "123456789",  # Número de documento del pagador
    "name": "Juan Perez",  # Nombre del tarjetahabiente
    "last_name": "Lopez",  # Apellido del tarjetahabiente
    "email": "juanperez@gmail.com",  # Correo electrónico del pagador
    "invoice": "1234",  # Número de factura o referencia
    "description": "Pago de prueba",  # Descripción del pago
    "value": "10000",  # Valor del pago
    "tax": "1600",  # Impuesto si aplica
    "tax_base": "8400",  # Base imponible
    "currency": "COP",  # Moneda
    "dues": "1",  # Número de cuotas
}

# Función para realizar el pago
def realizar_pago():
    try:
        # Realizar solicitud POST a la API de ePayco
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()

        # Verificar si el pago fue exitoso
        if response_data['status'] == 'success':
            token = response_data['data']['transactionID']
            print(f"Pago realizado con éxito. Token de confirmación: {token}")
            return token
        else:
            print(f"Error en el pago: {response_data['message']}")
            return None
    except Exception as e:
        print(f"Error al realizar el pago: {e}")
        return None

# Ejecutar la función
realizar_pago()
