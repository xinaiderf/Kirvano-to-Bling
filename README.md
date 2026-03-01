# Integração Kirvano → Bling (API V3)
<p> Este projeto automatiza o fluxo de vendas Aprovadas da Kirvano, enviando-as diretamente para o Bling utilizando a API V3 e Webhooks. </p>

---

🛠️ Tecnologias Utilizadas
-
* Python 3.13+
* FastAPI / Uvicorn
* Bling API V3
* Kirvano Webhook

---

⚙️ Configuração Inicial no Bling 
-
Crie um Aplicativo: No painel do Bling, vá em Configurações > Integrações > Aplicativos.

Callback: No campo Link de Redirecionamento, você pode usar https://google.com (apenas para capturar o código inicial).

Permissões: Garanta que o app tenha todas as permissões de leitura e escrita para Vendas e Contatos.

Credenciais: Copie o Client ID e o Client Secret e insira nas variáveis correspondentes no seu código.

---

🔑 Autenticação e Primeiros Passos 
-
O Bling utiliza o protocolo OAuth 2.0. Siga este fluxo para o primeiro acesso:

Autorização: Copie o link de convite gerado, cole no navegador e autorize o acesso.

Captura do Code: Você será redirecionado para uma URL parecida com esta:
https://google.com/?code=VALOR_DO_CODIGO_AQUI&state=...

Configuração do Script: Copie o valor de code e cole na variável auth_code no seu script.

⚠️ Atenção: Você tem cerca de 1 minuto para realizar a troca do auth_code pelo token antes que ele expire.

--- 
Instale as dependências: pip install -r requirements.txt

Inicie o Servidor:
python server.py

Persistência: Na primeira execução, o script criará um arquivo tokens.txt. A partir daí, o sistema usará o Refresh Token automaticamente para renovar o acesso sem intervenção manual.

---
📡 Configuração do Webhook (Kirvano)
Com o servidor rodando, configure o Webhook na sua conta Kirvano:

Evento: Venda Aprovada.

URL: https://seu-dominio.com/newOrder

💸 Finalização
Após esses passos, cada venda aprovada na Kirvano será processada, o contato será verificado/criado e o pedido de venda será lançado no Bling automaticamente. Agora é só escalar e ver o negócio rodar no automático!
