from fastapi import FastAPI, HTTPException, Header
import uvicorn
import blingAPI
from pydantic import BaseModel
from typing import List, Optional
import os
import base64
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Address(BaseModel):
    street: str
    number: str
    complement: Optional[str] = ""
    neighborhood: str
    city: str
    state: str
    zipcode: str

class Customer(BaseModel):
    name: str
    document: str
    email: str
    phone_number: str
    address: Address

class Product(BaseModel):
    name: str
    offer_name: str

class KirvanoWebhook(BaseModel):
    sale_id: str
    total_price: str
    created_at: str
    customer: Customer
    products: List[Product]

skus = {
    "PDRN-1": "SKU1",
    "PDRN-3": "SKU2",
    "PDRN-5": "SKU3",
    "PDRN-12": "SKU4",
    "GHK-CU-1": "SKU9",
    "GHK-CU-3": "SKU6",
    "GHK-CU-5": "SKU7",
    "GHK-CU-12": "SKU8"
}

tokenBase64 = os.getenv("tokenBase64")
TOKEN = base64.b64decode(tokenBase64).decode('utf-8')


@app.post("/newOrder")
async def newOrder(data: KirvanoWebhook, Authorization: str = Header(None)):
    
    if Authorization != f"Bearer {TOKEN}":
      raise HTTPException(status_code=401, detail="Unauthorized")
    
    
    customer = data.customer
    address = customer.address

    enderecoCliente = {
        "logradouro": address.street if address else "",
        "numero": address.number if address else "",
        "complemento": address.complement if address else "",
        "bairro": address.neighborhood if address else "",
        "municipio": address.city if address else "",
        "uf": address.state if address else "",
        "cep": address.zipcode if address else ""
    }

    dadosCliente = {
        "nomeCliente": customer.name,
        "cpfCliente": customer.document,
        "emailCliente": customer.email,
        "telefoneCliente": customer.phone_number
    }

    nomeProduto = data.products[0].name.upper()
    quantidadeVendida = data.products[0].offer_name.split(" ")[0]
    
    if "PDRN" in nomeProduto:
        nomeProduto = "PDRN"
    elif "GHK-CU" in nomeProduto:
        nomeProduto = "GHK-CU"

    dadosVenda = {
        "nomeProduto": nomeProduto,
        "precoTotal": data.total_price.replace("R$ ", "").replace(".", ""),
        "codigoPedido": data.sale_id,
        "dataVenda": data.created_at.split(" ")[0],
        "quantidadeVendida": quantidadeVendida
    } 
    print(f"Processando Pedido: {dadosVenda['codigoPedido']}")

    chaveBusca = f"{nomeProduto}-{quantidadeVendida}"
    codigoSKU = skus.get(chaveBusca)
    
    tokens = blingAPI.readTokensFile()
    access_token = tokens["access_token"]

    return await blingAPI.createPedidoVenda(access_token, codigoSKU, dadosCliente, enderecoCliente, dadosVenda)

if os.path.exists("tokens.txt"):
  print("🔄 Atualizando tokens...")
  try:
    blingAPI.refreshAccessToken()
  except Exception as e:
    print(f"Erro ao atualizar: {e}")
else: 
  print("🔑 Gerando token inicial...")
  try:
    blingAPI.generateAccessToken()
  except Exception as e:
    print(f"Erro ao gerar: {e}")

if __name__ == "__main__":
  uvicorn.run("server:app", host="0.0.0.0", port=4000, reload=True)