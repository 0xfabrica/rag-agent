# RAG Airbnb Assistant

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-10a37f?logo=openai)](https://platform.openai.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-yellow?logo=data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjRkZGIiB2aWV3Qm94PSIwIDAgMzAgMzAiIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiI+PHJlY3Qgd2lkdGg9IjMwIiBoZWlnaHQ9IjMwIiByeD0iNSIgZmlsbD0iI0ZGRDgwMCIvPjwvc3ZnPg==)](https://python.langchain.com/)
[![FAISS](https://img.shields.io/badge/FAISS-Semantic_Search-009688)](https://github.com/facebookresearch/faiss)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-2CA5E0?logo=telegram)](https://core.telegram.org/bots)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-4B0082)](https://www.trychroma.com/)
[![dotenv](https://img.shields.io/badge/dotenv-Env_Vars-4EAA25)](https://pypi.org/project/python-dotenv/)


Asistente conversacional basado en RAG (Retrieval-Augmented Generation) para responder preguntas sobre un alojamiento en Málaga, España, usando documentos propios (alojamiento ficticio) y la API de OpenAI. El bot funciona en Telegram y utiliza FAISS para la búsqueda semántica eficiente. Faiss (**Facebook AI Similarity Search**) es una biblioteca de código abierto desarrollada por Meta (antes Facebook) diseñada para realizar búsquedas de similitud eficientes y agrupamiento de vectores densos a gran escala.

## Características

- **RAG (Retrieval-Augmented Generation):** Responde preguntas usando información relevante extraída de documentos PDF.
- **Integración con Telegram:** Interactúa con los usuarios a través de un bot de Telegram.
- **Embeddings y búsqueda semántica:** Utiliza FAISS y OpenAI Embeddings para encontrar respuestas precisas.
- **Soporte para múltiples documentos:** Carga y fragmenta documentos desde la carpeta `docs/`.
- **Respuestas personalizadas:** El bot responde de manera amigable, profesional y cercana, usando emojis y fragmentando textos largos.

## Estructura del Proyecto

```
.
├── .env.example          # Variables de entorno (API keys, tokens, etc.)
├── rag_agent.py          # Código principal del bot y agente RAG
├── requirements.txt      # Dependencias del proyecto
├── docs/                 # Documentos fuente para el RAG (PDF, etc.)
├── faiss_index/          # Índice FAISS generado automáticamente
└── README.md             # Este archivo
```

## Requisitos

- Python 3.8+
- Cuenta de OpenAI y clave API
- Bot de Telegram y token

## Instalación

1. **Clona el repositorio y entra en la carpeta:**
   ```sh
   git clone https://github.com/0xfabrica/rag-agent.git
   cd rag_python
   ```

2. **Crea y activa un entorno virtual (opcional pero recomendado):**
   ```sh
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno:**
   - Renombra `.env.example` a `.env` si existe, o edita el archivo `.env` y añade tus claves:
     ```
     OPENAI_API_KEY="TU_OPENAI_API_KEY"
     TELEGRAM_BOT_TOKEN="TU_TELEGRAM_BOT_TOKEN"
     ```

5. **Coloca tus documentos en la carpeta `docs/`.**

## Uso

1. **Ejecuta el bot:**
   ```sh
   python rag_agent.py
   ```

2. **Habla con tu bot en Telegram:**  
   Busca tu bot por su nombre de usuario y envíale preguntas sobre el alojamiento.

## Personalización

- **Documentos:** Añade o reemplaza archivos PDF en la carpeta `docs/` para actualizar la base de conocimiento.
- **Prompt:** Modifica el prompt en [`rag_agent.py`](rag_agent.py) para cambiar el tono o el formato de las respuestas.
- ** Base de datos:** Añade una base de datos para guardar las conversaciones.

## Dependencias principales

- [`langchain`](https://python.langchain.com/)
- [`openai`](https://pypi.org/project/openai/)
- [`faiss-cpu`](https://github.com/facebookresearch/faiss)
- [`python-telegram-bot`](https://python-telegram-bot.org/)
- [`python-dotenv`](https://pypi.org/project/python-dotenv/)
- [`chromadb`](https://www.trychroma.com/)

## Créditos

Desarrollado por Izan Medkouri López, IntelliGrow Owner.

---

> **Nota:** No compartas tus claves API públicamente.  
> Para dudas técnicas, revisa el código en [`rag_agent.py`](rag_agent.py).