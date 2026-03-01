import requests
import base64
import re
from dotenv import load_dotenv
import os

load_dotenv()  

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
auth_code = os.getenv("auth_code")

url = "https://api.bling.com.br/Api/v3/oauth/token?"

credentials = f"{client_id}:{client_secret}"
base_64 = base64.b64encode(credentials.encode()).decode()

def readTokensFile():
  with open("tokens.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    access_token = lines[0].split("Access Token: ")[1].strip()
    refresh_token = lines[1].split("Refresh Token: ")[1].strip()

    saida = { "access_token": access_token, "refresh_token": refresh_token }
    return saida

def writeTokensFile(access_token, refresh_token):
  with open("tokens.txt", "w", encoding="utf-8") as file:
    file.write(f"Access Token: {access_token}\n")
    file.write(f"Refresh Token: {refresh_token}")
    print(f"----- Access Token ----- \n \n {access_token} \n")
    print(f"----- Refresh Token ----- \n \n {refresh_token} \n\n")


def generateAccessToken():
  headers = {
    "Authorization": f"Basic {base_64}",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "1.0",
    "enable-jwt": "1"
  }

  payload = {
    "grant_type": "authorization_code",
    "code": auth_code
  }

  try:
    response = requests.post(url, headers=headers, data=payload)      
    if response.status_code == 200:
      writeTokensFile(response.json()['access_token'], response.json()['refresh_token'])
      
    else:
      print(f"Erro {response.status_code}")
      print(response.text)

  except Exception as e:
    print(f"Erro na conexão: {e}")

def refreshAccessToken():

  with open("tokens.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    refresh_token = lines[1].split("Refresh Token: ")[1].strip()

  headers = {
  "Authorization": f"Basic {base_64}",
  "Content-Type": "application/x-www-form-urlencoded",
  "enable-jwt": "1"
  }

  payload = {
    "grant_type": "refresh_token",
    "refresh_token": refresh_token
  }

  try:
    response = requests.post(url, headers=headers, data=payload, timeout=10)      
    if response.status_code == 200:
      writeTokensFile(response.json()['access_token'], response.json()['refresh_token'])
    else:
      print(f"Erro {response.status_code}")
            
  except Exception as e:
    print(f"Erro na conexão: {e}")


async def createPedidoVenda(access_token, codigoSKU, dadosCliente, enderecoCliente, dadosVenda):

  url = "https://api.bling.com.br/Api/v3/pedidos/vendas"


  contatoId = await getContato(access_token, dadosCliente["cpfCliente"])
  print(f"Contato ID: {contatoId}")
  if contatoId is None:
    contatoId = await createContato(access_token, dadosCliente, enderecoCliente)
    print(f"Contato criado com ID: {contatoId}")

    
  payload = {
    "data": dadosVenda["dataVenda"],
    "numeroPedidoCompra": dadosVenda["codigoPedido"],
    "contato": {
      "id": contatoId,
    },
    "observacoesInternas": f"Integração Kirvano. Venda: {dadosVenda['codigoPedido']}",
    "itens": [
      {
        "codigo": codigoSKU, 
        "descricao": f"Produto referente à venda {dadosVenda['codigoPedido']}, feita na plataforma Kirvano.",
        "quantidade": dadosVenda["quantidadeVendida"],
        "valor": dadosVenda["precoTotal"],
        "unidade": "UN"
      }
    ],
    "transporte": {
      "fretePorConta": 0, 
      "etiqueta": {
        "nome": dadosCliente["nomeCliente"],
        "endereco": enderecoCliente["logradouro"],
        "numero": enderecoCliente["numero"],
        "complemento": enderecoCliente["complemento"],
        "municipio": enderecoCliente["municipio"],
        "uf": enderecoCliente["uf"],
        "cep": enderecoCliente["cep"], 
        "bairro": enderecoCliente["bairro"],
        "nomePais": "BRASIL"
      },
      "volumes": [
      {
        "servico": "CORREIOS", 
      }
    ]
    }
  }
  

  response = requests.post(url, headers={"Authorization": f"Bearer {access_token}"}, json=payload)
  if response.status_code == 201:
    print("--- PEDIDO DE VENDA CRIADO COM SUCESSO! ---")
  else:
    print(f"Erro {response.status_code}: {response.text}")



async def createContato(access_token, dadosCliente, enderecoCliente):
 
  url = "https://api.bling.com.br/Api/v3/contatos"

  dadosCliente["telefoneCliente"] = re.sub(r'\D', '', str(dadosCliente["telefoneCliente"]))

  if dadosCliente["telefoneCliente"].startswith("55"):
    dadosCliente["telefoneCliente"] = dadosCliente["telefoneCliente"][2:]

  if len(dadosCliente["telefoneCliente"]) < 11:
    dadosCliente["telefoneCliente"] = dadosCliente["telefoneCliente"].zfill(11)
  elif len(dadosCliente["telefoneCliente"]) > 11:
    dadosCliente["telefoneCliente"] = dadosCliente["telefoneCliente"][-11:]


  payload = {
  "nome": dadosCliente["nomeCliente"],
  "situacao": "A",
  "numeroDocumento": dadosCliente["cpfCliente"].replace(".", "").replace("-", "").strip(),
  "telefone": dadosCliente["telefoneCliente"],
  "celular": dadosCliente["telefoneCliente"],
  "tipo": "F",
  "email": dadosCliente["emailCliente"],
  "emailNotaFiscal": dadosCliente["emailCliente"],
  "endereco": {
    "geral": {
      "endereco": enderecoCliente["logradouro"],
      "cep": enderecoCliente["cep"],
      "bairro": enderecoCliente["bairro"],
      "municipio": enderecoCliente["municipio"],
      "uf": enderecoCliente["uf"],
      "numero": enderecoCliente["numero"],
      "complemento": enderecoCliente["complemento"]
    },
  },
  "pais": {
    "nome": "BRASIL"
  }}

  response = requests.post(url, headers={"Authorization": f"Bearer {access_token}"}, json=payload)
  
  if response.status_code == 201:
    print("--- CONTATO CRIADO COM SUCESSO! ---")
    return
  else:
    print(f"Erro {response.status_code}: {response.text}")


async def getContato(access_token, cpf):

  url = f"https://api.bling.com.br/Api/v3/contatos?numeroDocumento={cpf}"
  response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
  if response.status_code == 200:
    dados = response.json()

    if "data" in dados and len(dados["data"]) > 0:
      print("----- CLIENTE ID ENCONTADO -----")
      return dados["data"][0]["id"]
  else:
    print("----- CLIENTE ID NÃO ENCONTRADO -----")
    return None