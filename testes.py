import requests
import blingAPI
import re

dadosCliente = {
    "nomeCliente": "Beatrix Yazigi",
    "cpfCliente": "09021457890",
    "emailCliente": "byazigi@hotmail.com",
    "telefoneCliente": "11981417533",
    "celularCliente": "11981417533"
}

# Mockup para enderecoCliente
enderecoCliente = {
    "logradouro": "Rua Raimundo Simão de Souza",
    "numero": "26",
    "complemento": "252c",
    "bairro": "Vila Suzana",
    "municipio": "São Paulo",
    "uf": "SP",
    "cep": "05709040"
}

def createContato(dadosCliente, enderecoCliente):
  url = "https://api.bling.com.br/Api/v3/contatos"

  tokens = blingAPI.readTokensFile()
  access_token = tokens["access_token"]

  payload = {
  "nome": dadosCliente["nomeCliente"],
  "situacao": "A",
  "numeroDocumento": dadosCliente["cpfCliente"].replace(".", "").replace("-", "").strip(),
  "telefone": re.sub(r'[^\d]', '', dadosCliente["telefoneCliente"]),
  "celular": dadosCliente["celularCliente"],
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
    print(response.json())
  else:
    print(f"Erro {response.status_code}: {response.text}")

createContato(dadosCliente, enderecoCliente)