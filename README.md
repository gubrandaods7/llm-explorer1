# llm-explorer

Interface web de chat com o Google Gemini usando Python e Streamlit. Permite conversar com diferentes modelos Gemini direto no navegador.

## Estrutura do projeto

```
llm-explorer/
├── .env               # Sua API key (não vai para o git)
├── .gitignore          # Ignora .env, .venv/ e __pycache__/
├── requirements.txt    # Dependências do projeto
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

## Como rodar

```bash
streamlit run app.py

# Caso o comando acima não seja reconhecido:
python -m streamlit run app.py
```

O navegador abre automaticamente em `http://localhost:8501`.

## Funcionalidades

- **Seleção de modelo** na barra lateral: `gemini-2.5-flash`, `gemini-2.5-flash-lite`, `gemini-2.0-flash-lite`, `gemini-2.5-pro`
- **Histórico de conversa** mantido via `st.session_state`
- **Troca de modelo** em tempo real (limpa o histórico ao trocar)
- **Tratamento de erros** de cota da API (`ResourceExhausted`)
