# QTS - AT2 - Qualidade e Testes de Software 🚀

Bem-vindo ao repositório do exercício prático de testes automatizados e Qualidade de Software! Este projeto é uma aplicação RESTful em Flask (com interface frontend básica integrada) que gerencia cadastros de usuários. 

O projeto evoluiu durante o exercício com foco rigoroso em metodologias ágeis (TDD), testes em múltiplos níveis (Pirâmide de Testes) e Integração Contínua (CI/CD).

---

## 🏗️ Arquitetura e Estrutura do Projeto

A base de código foi elaborada pensando em escalabilidade e manutenibilidade, separando perfeitamente a **Camada de Apresentação (Rotas)** da **Camada de Lógica de Negócios (Serviços)**.

Abaixo você confere o mapa completo do repositório e a responsabilidade de cada arquivo:

```text
📦 AT2
 ┣ 📂 .github/workflows      # ⚙️ Pipeline de CI/CD (GitHub Actions)
 ┃ ┗ 📜 ci.yml               # Receita dos jobs automáticos (Black, Flake8, Pytest)
 ┣ 📂 app                    # 🧠 Código-fonte principal da aplicação
 ┃ ┣ 📂 routes               # Controladores da API
 ┃ ┃ ┗ 📜 user_routes.py     # Endpoints RESTful (GET, POST, PUT, DELETE)
 ┃ ┣ 📂 services             # Regras de Negócio e Persistência
 ┃ ┃ ┗ 📜 user_services.py   # Lógica de validação (Email, Duplicatas) e array em memória
 ┃ ┣ 📂 templates            # Visualização / UI
 ┃ ┃ ┗ 📜 users.html         # Frontend HTML/JS vanilla que consome nossa própria API
 ┃ ┗ 📜 __init__.py          # Factory Pattern: instancia o Flask e registra os Blueprints
 ┣ 📂 tests                  # 🧪 Suítes de testes rigorosamente divididas
 ┃ ┣ 📂 e2e                  # Selenium: Interações reais automatizadas no Chrome
 ┃ ┣ 📂 functional           # Validação de fluxos operacionais inteiros e longos
 ┃ ┣ 📂 integration          # Comunicação entre as requisições web e o motor de serviços
 ┃ ┗ 📂 unit                 # Testes microscópicos de sucesso/falha em funções puras
 ┣ 📜 run.py                 # 🚀 Ponto de entrada (Entrypoint) para subir o servidor local
 ┣ 📜 requirements.txt       # 📦 Dependências vitais e de desenvolvimento
 ┣ 📜 pyproject.toml         # 🔧 Arquivo de configuração de Linter/Testes
 ┗ 📜 README.md              # 📖 Esta documentação
```

---

## ✨ Nova Funcionalidade Implementada

Como objetivo do exercício, implementamos uma nova regra de negócio vital para a plataforma: **O Campo de E-mail Obrigatório**.

- **Validação de Negócio**: Não é mais possível cadastrar um usuário informando apenas seu nome.
- **Validação de Formato**: O sistema intercepta o payload e valida se o e-mail possui um caractere `@` utilizando um helper isolado (`is_valid_email()`).
- **Unicidade de Dados Absoluta**: Foi adicionada uma barreira que blinda o banco de dados contra duplicidades (um mesmo e-mail não pode pertencer a dois usuários e nomes não podem conflitar).
- **Frontend Atualizado**: A interface clássica (`users.html`) recebeu campos novos e as requisições assíncronas do JavaScript foram adaptadas para suportar as novidades do Backend de forma transparente ao usuário.

---

## 🛠️ O Processo TDD (Test Driven Development)

Toda a implementação do campo `email` foi criada **estritamente sob a metodologia TDD**, garantindo que o código foi 100% guiado por testes. 

O fluxo de trabalho e as evidências ocorreram nas 3 fases consagradas pela engenharia de software:

### 🔴 1. Fase RED (Teste Falhando)
Antes de alterar qualquer arquivo em `app/` para suportar e-mails, o time construiu **20 novos testes** baseados apenas nos "requisitos do cliente" da nova funcionalidade.
- Foram codificados cenários complexos tentando salvar requisições sem e-mail, e-mails incorretos, duplicados e fluxos agressivos de listagem.
- **A Evidência**: Ao executar o `pytest` de forma inicial, o motor disparou **dezenas de falhas e telas vermelhas** (erros 400 inesperados, AssertionError e KeyError), atestando perfeitamente a ausência da funcionalidade no código de produção.

### 🟢 2. Fase GREEN (Teste Passando)
Com as falhas devidamente diagnosticadas, o código "mínimo viável" foi escrito para fazer o console voltar a ficar verde:
- `user_services.py` passou a ler o dicionário à caça do e-mail e rejeitar incongruências.
- `user_routes.py` blindou as camadas web, despachando `Status Code 400` precocemente.
- `users.html` permitiu o disparo dos dados.
- **A Evidência**: Re-executamos o terminal e os mesmos 20 testes alcançaram **100% de sucesso (`PASSED`)**.

### 🔵 3. Fase REFACTOR (Melhoria Contínua)
Com o sistema operante, partimos para a lapidação de arquitetura.
Identificamos uma duplicação na verificação crua `if "@" not in email` e a extraímos para uma micro-função `is_valid_email(email)`, aplicada em múltiplos lugares, reduzindo complexidade ciclomática e repetitividade.

---

## 📊 Profundidade da Cobertura de Testes

Para garantir o requisito do exercício, a suíte conta agora com os seguintes incrementos táticos:

1. **Unitários (`tests/unit/`) - 10 Novos Testes**: Isolam o comportamento atômico das lógicas de serviço. Verificam persistência em memória e tratamentos absurdos para usuários inexistentes.
2. **Integração (`tests/integration/`) - 5 Novos Testes**: Cuidam do acoplamento garantindo que o despachante de Rotas consegue injetar na camada de Serviços.
3. **Funcionais (`tests/functional/`) - 3 Novos Testes**: Comparam comportamentos macro simulando uma jornada de apagar usuários um-por-um e conferir listagens.
4. **End-to-End E2E (`tests/e2e/`) - 2 Novos Testes**: Através do **Selenium Chrome WebDriver**, eles assumem o papel de um humano, digitam ativamente e-mails na tela de interface e caçam pop-ups de erro sem delays mágicos, usando estritamente o `WebDriverWait`.

---

## 💎 Qualidade de Código e Integração Contínua (CI/CD)

Não deixamos o aspecto organizacional de lado. O código sofreu intervenções profundas dos principais guardiões do mundo Python:
* **Black Code Formatter**: Todo o repositório passou pelo `black .`, adequando-o estritamente aos padrões de formatação limpa (PEP8).
* **Flake8 Linter**: Executado para expurgar variáveis flutuantes ou módulos importados não utilizados no `__init__.py` e nos arquivos de teste.

### 🤖 Pipeline Automatizada (GitHub Actions)
Uma pipeline de CI robótica (Integração Contínua) foi perfeitamente programada em `.github/workflows/ci.yml`.
Ao realizar qualquer **Push** para o GitHub, os robôs entram em ação e procedem:
1. Instanciamento de contêineres e download das dependências.
2. Análise estética rigorosa (`flake8 .` e `black --check .`).
3. Deploy e start do servidor Flask `run.py` em segundo plano.
4. Acionamento do gatilho do `pytest` rodando todo o cardápio em modo silencioso (Headless) garantindo que nenhum novo commit vai corromper a master.

---

## 💻 Guia de Execução na Máquina Local

Para avaliar ou dar continuidade ao desenvolvimento de forma local, execute os passos a seguir:

### 1. Preparando o Ambiente (Terminal)
Primeiro, crie e ative sua Virtual Environment (venv) para isolar as dependências do projeto:

**No Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**No Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Com a venv ativada, instale o cinturão de utilidades e dependências:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install black flake8 pytest pytest-flask selenium
```

### 2. Ligando a Aplicação
Suba o servidor e acesse via navegador em `http://localhost:5000`:
```bash
python run.py
```

### 3. Rodando o Escudo Protetor (Testes)
Na raiz do diretório `AT2`, acione a suite completa e veja as dezenas de testes atuando em milissegundos:
```bash
pytest
```
*(Nota: Certifique-se de que o run.py **não está em execução** caso haja colisão de estado nos testes, ou caso o E2E dependa da inicialização do servidor paralelo).*

### 4. Avaliando a Pureza do Código
Passe as ferramentas de auditoria e confirme a ausência de violações:
```bash
black --check .
flake8 .
```
