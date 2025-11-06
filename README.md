# Projeto: Sistema de Corretora de Valores com POO em Python

## 📖 Sobre o Projeto

Este projeto é o back-end de um sistema de corretora de valores. O objetivo principal é aplicar os 4 pilares da POO (Encapsulamento, Abstração, Herança e Polimorfismo) em um cenário prático e realista.

**O projeto foi desenvolvido em 3 Níveis:**
* **Nível 1:** Design de Classes e implementação dos 4 pilares de POO.
* **Nível 2:** Criação de uma interface de menu interativa no terminal (CLI).
* **Nível 3:** Integração com um banco de dados **MySQL** para persistência de dados, com lógica de carregamento e salvamento de todas as operações.

---

##  UML - Diagrama de Classes

A arquitetura do sistema foi planejada utilizando o seguinte diagrama de classes UML.

![Diagrama de Classes](docs/uml_finalizado.png)

---

## 🚀 Funcionalidades

-   **Design de POO:** Aplicação clara dos 4 pilares da POO.
-   **Persistência de Dados:** Todas as informações de clientes, contas e carteiras são salvas e carregadas de um banco de dados **MySQL**.
-   **Segurança:** A conexão com o banco de dados é feita de forma segura, usando `python-dotenv` para gerenciar credenciais, que não são enviadas para o GitHub.
-   **Interface de Terminal:** Um menu de usuário (CLI) completo para interagir com o sistema.
-   **Operações de Corretora:**
    -   Gerenciamento de Clientes e Contas.
    -   Operações Financeiras: Métodos seguros para `Depositar` e `Sacar`.
    -   Home Broker: Funcionalidades para `Comprar` e `Vender` ativos, com atualização persistente da carteira.
---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **MySQL (Banco de dados)**
- **mysql-connector-python** (Biblioteca de integração Python-MySQL)
- **python-dotenv** (Para gerenciamento seguro de credenciais)
- **Git & GitHub** (Para versionamento de código)

---

## 🏃 Como Executar

1. Clone o repositório:
   ```bash
   git clone [https://github.com/seu-usuario/corretora-poo-python.git](https://github.com/seu-usuario/corretora-poo-python.git)

2. **Instale as dependências Python:**
    ```bash
    pip install mysql-connector-python python-dotenv
    ```
    *(Ou `py -m pip install ...` se você usar o lançador do Windows, foi o que funcionou para mim)*

3.  **Configure o Banco de Dados:**
    * Um servidor MySQL rodando.
    * Execute o script SQL ( em `docs/schema.sql` - *você pode criar esse arquivo e colar seu script SQL lá*) para criar o banco `corretora_db` e as tabelas.
    * *Opcional: Insira os dados de exemplo manualmente no MySQL Workbench.(foi o que utilizei)*

4.  **Configure as Variáveis de Ambiente:**
    * Crie um arquivo chamado `.env`.
    * Adicione suas credenciais do banco de dados nele:
        ```dotenv
        DB_HOST=localhost
        DB_USER=root
        DB_PASSWORD=sua_senha_aqui
        DB_NAME=corretora_db
        ```

5.  **Execute o Programa:**
    ```bash
    python main.py
    ```