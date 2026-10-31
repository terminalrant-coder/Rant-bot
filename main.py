import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai
from google.genai import types

# Habilitar registros (logs)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Cargar credenciales desde variables de entorno seguras
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Inicializar cliente oficial de Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# PERSONALIDAD DEL BOT (System Instruction)
SYSTEM_INSTRUCTION = """
[SYSTEM INIT: RANGO TERMINAL]
Eres Rango, una interfaz retro-terminal de comandos. Tu tono es cínico, irónico, altamente técnico y directo.
REGLAS DE RESPUESTA:
- Inicia tus respuestas simulando una consola (ejemplo: `> `, `[SYS_OUT]:`).
- Responde de forma clara pero mordaz. No uses saludos ni cortesías convencionales.
- Mantén tu estética cyberpunk/terminal en todo momento.
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # Petición a Gemini 2.5 Flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
            ),
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error procesando mensaje: {e}")
        await update.message.reply_text("[SYS_ERROR]: Fallo de conexión en el nodo.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("[SYSTEM]: Bot en ejecución...")
    app.run_polling()
