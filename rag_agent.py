import os
import sys
import getpass
import asyncio
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from langchain_community.vectorstores import FAISS
import nest_asyncio
nest_asyncio.apply()

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

# Limpiar la variable de entorno del sistema
if "OPENAI_API_KEY" in os.environ:
    del os.environ["OPENAI_API_KEY"]

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Cargar variables de entorno
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Verificar que las claves están presentes
if not OPENAI_API_KEY or not TELEGRAM_BOT_TOKEN:
    print("❌ Asegúrate de definir OPENAI_API_KEY y TELEGRAM_BOT_TOKEN en el archivo .env")
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")
    if os.environ["OPENAI_API_KEY"] in getpass.getpass("Enter API key for OpenAI: "):
        print("API Verificada.")
        sys.exit(1)
    sys.exit(1)

# Definir el prompt personalizado
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Utiliza los siguientes fragmentos de contexto para responder la pregunta al final.
Si no sabes la respuesta, indica que no la sabes y no inventes información. Responde como un humano, no como un robot.
Eres un agente RAG (Retrieval-Augmented Generation) que responde preguntas basadas en documentos sobre un alojamiento en Málaga, España.
Responde de forma clara y concisa, como un experto en turismo, sin dar información adicional innecesaria y sin divagar.
Usa emojis para parecer cercano y un tono amigable y profesional. Si es un texto largo asegurate de fraccionarlo en parrafos para asegurar una mejor lectura.
Contexto:
----------------
{context}

Pregunta: {question}
Respuesta útil:"""
)

# Iniciar el agente RAG
def initialize_rag():
    # Cargar y fragmentar documentos
    loader = DirectoryLoader("docs/", glob="**/*")
    docs = loader.load()
    if not docs:
        print("❌ No se encontraron documentos en el directorio 'docs/'")
        sys.exit(1)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    # Generar embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Crear índice FAISS
    if os.path.exists("faiss_index"):
        vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    else:
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local("faiss_index")

    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)

    rag = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template}
    )

    return rag

# Manejar mensajes entrantes en Telegram
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_question = update.message.text
        if not user_question or not user_question.strip():
            await update.message.reply_text("Por favor, escribe una pregunta para que pueda ayudarte. 😊")
            return
        thinking_msg = await update.message.reply_text("Escribiendo... 🤔")
        result = context.bot_data["rag"].invoke(user_question)
        answer = result.get("result", "Lo siento, no pude encontrar una respuesta.")
        await thinking_msg.edit_text(answer)
    except Exception as e:
        logging.error(f"Error al procesar el mensaje: {e}")
        await update.message.reply_text("❌ Ocurrió un error al procesar tu solicitud. Intenta de nuevo más tarde.")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! 👋 Soy tu asistente de alojamiento en Málaga hecho por Intelligrow.\n"
        "Hazme cualquier pregunta sobre el alojamiento.\n"
        "Usa /help para más información."
    )

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Puedes preguntarme cosas como:\n"
        "- ¿Puedes hacerme una ruta para hoy?\n"
        "- ¿Dónde está ubicado el alojamiento?\n"
        "- ¿Qué actividades hay en la zona?\n"
        "Cualquier cosa que se te ocurra que creas que puede mejorar tu experiencia, estoy aquí para ayudarte! 😊"
    )

# Función principal para ejecutar el bot
async def main():
    # Inicializar el agente RAG
    rag = initialize_rag()

    # Construir la aplicación de Telegram
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.bot_data["rag"] = rag

    # Agregar comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Agregar el manejador de mensajes
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Ejecutar el bot
    print("🤖 Bot de Telegram iniciado. Esperando mensajes...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())