"""
chat.py - Chat interativo no terminal usando Google Gemini.

Mantém o histórico da conversa e o envia a cada turno,
permitindo respostas com contexto dos turnos anteriores.
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
    chat = model.start_chat(history=[])

    print("=== Chat com Gemini ===")
    print('Digite suas mensagens. Use "sair" ou Ctrl+C para encerrar.\n')

    while True:
        try:
            user_input = input("Você: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando chat. Até mais!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("sair", "exit", "quit"):
            print("Encerrando chat. Até mais!")
            break

        response = chat.send_message(user_input)
        print(f"\nGemini: {response.text}\n")


if __name__ == "__main__":
    main()
