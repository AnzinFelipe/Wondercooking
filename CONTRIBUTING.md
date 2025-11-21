# 👨‍🍳 Venha ser um contribuidor de Wondercooking

👋 Olá, chef de código!
Que bom ver você por aqui! Se está pensando em contribuir com o projeto **Wondercooking**, seja muito bem-vindo à nossa cozinha digital. 👨‍🍳🔥
Aqui você encontrará tudo o que precisa para preparar, temperar e servir suas contribuições da melhor forma possível.

Vamos ao mise en place! 🍴

---

## 🥣 Pré-requisitos

Antes de colocar a mão na massa, certifique-se de ter as seguintes ferramentas instaladas:

- **Python**
- **Git**
- **Visual Studio Code (VSCode)**

---

## 🎛️ Começando a cozinhar

1. Faça um fork deste repositório.
2. Clone o projeto no seu computador:
   ```bash 
   git clone https://github.com/seu-usuario/Wondercooking.git
   
   ┌──────────────────────────────────────────────────────────────┐
   │ 📥  Etapa 1 — Clone o Repositório                            │
   └──────────────────────────────────────────────────────────────┘

    Abra seu terminal e navegue até o diretório onde deseja clonar o repositório.
    Em seguida, execute o comando:
    
    git clone https://github.com/eduaab/Wondercooking.git
    
    
    ┌──────────────────────────────────────────────────────────────┐
    │ 📂  Etapa 2 — Navegue até o Diretório do Projeto             │
    └──────────────────────────────────────────────────────────────┘
    
    Use o comando:
    
    cd Wondercooking
    
    
    ┌──────────────────────────────────────────────────────────────┐
    │ 🧪  Etapa 3 — Crie e Ative um Ambiente Virtual               │
    └──────────────────────────────────────────────────────────────┘
    
    Caso não tenha o Virtualenv instalado, execute:
    
    pip install virtualenv
    
    Agora crie o ambiente virtual:
    
    python -m venv venv
    
    Para ativar:
    
    🔹 Windows:
    venv\Scripts\activate
    
    🔹 macOS/Linux:
    source venv/bin/activate
    
    
    ┌──────────────────────────────────────────────────────────────┐
    │ 📦  Etapa 4 — Instale as Dependências                        │
    └──────────────────────────────────────────────────────────────┘
    
    Com o ambiente virtual ativado, execute:
    
    pip install -r requirements.txt
    
    
    ┌──────────────────────────────────────────────────────────────┐
    │ 🧱  Etapa 5 — Execute as Migrações                           │
    └──────────────────────────────────────────────────────────────┘
    
    Crie as migrações:
    
    python manage.py makemigrations
    
    Depois aplique:
    
    python manage.py migrate
    
    💡 *Em alguns dispositivos use "py" em vez de "python"*
    
    
    ┌──────────────────────────────────────────────────────────────┐
    │ 🔥  Etapa 6 — Inicie o Servidor de Desenvolvimento           │
    └──────────────────────────────────────────────────────────────┘
    
    Execute:
    
    python manage.py runserver
    
    Agora abra no navegador:
    
    http://localhost:8000/
    
    
    ┌──────────────────────────────────────────────────────────────┐
    │ 🛠  Etapa 7 — Contribuindo com Código                        │
    └──────────────────────────────────────────────────────────────┘
    
    Recomendamos o uso do Visual Studio Code (VSCode) para desenvolver o projeto.
    Para abrir o projeto no VSCode, siga os passos:
    
    Abra o VSCode.  
Clique em *File > Open Folder...* e selecione o diretório do projeto **Wondercooking**.  
Tenha certeza de que o ambiente virtual esteja ativado no terminal do VSCode.  

---

# 🍴 Abra um Pull Request

### 🔍 Processo de Revisão

Nossos **cozinheiros* analisarão cada Pull Request com atenção.  
Somente e apenas aqueles que estiverem alinhados com o cardápio do projeto** serão aprovados. 👨‍🍳✨

---

## 🧾 Dúvidas?

Se ouver alguma duvida, abra uma **issue** e nossa equipe de cozinha ficará feliz em ajudar. 🍽🗨️

---

## 📚 Diretrizes de Desenvolvimento 🤔

🔹 **Use boas práticas de código** em *Python, HTML e CSS*  
🔹 **Mantenha a formatação limpa e padronizada**  
🔹 **Organize os imports com elegância e ordem**

> 📌 *Código bonito é prato bonito — ninguém quer servir comida feia.*
