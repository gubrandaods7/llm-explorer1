"""
basic_call.py - Chamada simples à API do Google Gemini.

Envia um único prompt e imprime a resposta.
"""

import os
import sys

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Erro: defina a variável de ambiente GEMINI_API_KEY antes de rodar.")
        sys.exit(1)

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = "Explique, em 3 frases curtas, o que é uma API REST."
    print(f"Prompt: {prompt}\n")

    response = model.generate_content(prompt)
    print(f"Resposta do Gemini:\n{response.text}")


if __name__ == "__main__":
    main()
