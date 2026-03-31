# llm-explorer

Projeto de aprendizado para chamadas diretas à API do Google Gemini usando Python. O objetivo é explorar, de forma progressiva, como integrar um LLM em aplicações — desde uma chamada simples até uma interface visual de chat.

## Estrutura do projeto

```
llm-explorer/
├── .env               # Sua API key (não vai para o git)
├── .gitignore          # Ignora .env, .venv/ e __pycache__/
├── requirements.txt    # Dependências do projeto
├── basic_call.py       # Chamada única à API (ponto de partida)
├── chat.py             # Chat interativo no terminal
└── app.py              # Interface web com Streamlit
```

## Pré-requisitos

- Python 3.10+
- Uma API key do Google Gemini (gratuita)

## Obtendo a API Key

1. Acesse [Google AI Studio](https://aistudio.google.com/apikey)
2. Clique em **Create API Key**
3. Copie a chave gerada

## Instalação

```bash
cd llm-explorer
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

### Dependências

| Pacote | Para quê serve |
|---|---|
| `google-generativeai` | SDK oficial do Google para acessar os modelos Gemini |
| `python-dotenv` | Carrega variáveis de ambiente do arquivo `.env` |
| `streamlit` | Framework para criar interfaces web interativas em Python |

## Configurando a API Key

Crie/edite o arquivo `.env` na raiz do projeto e cole sua chave:

```
GEMINI_API_KEY=sua-chave-aqui
```

O arquivo `.env` já está no `.gitignore`, então sua chave não será commitada por acidente.

---

## Scripts

O projeto possui 3 scripts, cada um mostrando um nível diferente de complexidade na integração com o Gemini.

---

### 1. `basic_call.py` — Chamada única à API

O script mais simples. Envia **um único prompt** ao modelo e imprime a resposta. Sem histórico, sem loop — apenas uma ida e volta para validar que a API key funciona e entender a estrutura básica.

```bash
python basic_call.py
```

**Como funciona:**

1. Carrega a API key do `.env` com `load_dotenv()`
2. Configura o SDK com `genai.configure(api_key=...)`
3. Cria uma instância do modelo com `genai.GenerativeModel("gemini-2.5-flash")`
4. Envia o prompt com `model.generate_content(prompt)` e imprime `response.text`

**Conceitos aprendidos:**
- Autenticação via API key
- Método `generate_content()` — chamada stateless (sem memória de turnos anteriores)

---

### 2. `chat.py` — Chat interativo no terminal

Evolui o `basic_call.py` para uma **conversa contínua**. O modelo recebe o histórico completo a cada turno, permitindo respostas contextuais (ele "lembra" o que você disse antes).

```bash
python chat.py
```

Digite suas mensagens e o modelo responderá com contexto. Digite `sair` ou pressione `Ctrl+C` para encerrar.

**Como funciona:**

1. Mesma configuração de API key e modelo
2. Inicia uma sessão de chat com `model.start_chat(history=[])` — isso cria um objeto `ChatSession` que acumula o histórico automaticamente
3. Dentro de um loop `while True`, lê a entrada do usuário e envia com `chat.send_message(user_input)`
4. O SDK gerencia o histórico internamente — cada chamada envia todas as mensagens anteriores junto

**Diferença chave em relação ao `basic_call.py`:**

| | `basic_call.py` | `chat.py` |
|---|---|---|
| Método | `generate_content()` | `chat.send_message()` |
| Histórico | Nenhum (stateless) | Acumulado automaticamente |
| Interação | Uma pergunta/resposta | Loop contínuo |

**Conceitos aprendidos:**
- `ChatSession` e gerenciamento de histórico pelo SDK
- Loop de input/output no terminal
- Tratamento de interrupção (`Ctrl+C` / `EOFError`)

---

### 3. `app.py` — Interface web com Streamlit

Versão visual do chat, rodando no navegador. Adiciona seleção de modelo, tratamento de erros de cota e uma UI completa de chat.

```bash
streamlit run app.py

# Caso o comando acima não seja reconhecido:
python -m streamlit run app.py
```

O navegador abre automaticamente em `http://localhost:8501`.

**Como funciona:**

1. Configura a página com `st.set_page_config()` e exibe título/subtítulo
2. Na barra lateral, oferece um seletor com 3 modelos: `gemini-2.5-flash`, `gemini-2.0-flash-lite`, `gemini-2.5-pro`
3. Usa `st.session_state` para manter o histórico entre re-renders do Streamlit:
   - `st.session_state.chat` — objeto `ChatSession` do SDK
   - `st.session_state.messages` — lista de dicts `{"role": ..., "content": ...}` para renderizar na tela
   - `st.session_state.current_model` — modelo selecionado (trocar o modelo limpa o histórico)
4. O input do usuário é capturado com `st.chat_input()`, e as mensagens são exibidas com `st.chat_message()`
5. Trata o erro `ResourceExhausted` (cota da API atingida) com uma mensagem amigável

**Conceitos aprendidos:**
- Streamlit: `session_state`, `chat_input`, `chat_message`, `sidebar`, `spinner`
- Re-renderização do Streamlit — por que precisamos de `session_state` para manter estado
- Troca dinâmica de modelos em tempo de execução
- Tratamento de erros específicos da API (`ResourceExhausted`)

---

## Fluxo de aprendizado recomendado

```
basic_call.py  →  chat.py  →  app.py
(uma chamada)    (loop+histórico)  (UI web+múltiplos modelos)
```

Cada script adiciona uma camada de complexidade sobre o anterior, facilitando o entendimento gradual da API.
