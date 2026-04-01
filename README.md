# Smart Office Assistant (SOMS)

A powerful, AI-driven office automation tool designed to streamline meeting summaries, document queries (RAG), scheduling, and translation tasks.

## 🌟 Features

-   **Meeting Summarization**: Automatically generate concise summaries and action items from meeting transcripts.
-   **RAG-based Document Query**: Upload or paste documents and ask questions to get context-aware answers using Retrieval-Augmented Generation.
-   **Smart Scheduling**: Extract structured schedule information from natural language descriptions.
-   **Translation Services**: Professional-grade translation for office documents and communication.
-   **Modern UI**: Built with Vue 3 and Tailwind CSS v4, featuring a sleek dark mode and responsive design.

## 🚀 Tech Stack

-   **Backend**: [FastAPI](https://fastapi.tiangolo.com/), Python 3.13, [ChromaDB](https://www.trychroma.com/) (Vector Store)
-   **Frontend**: [Vue.js 3](https://vuejs.org/), [Vite](https://vitejs.dev/), [Tailwind CSS v4](https://tailwindcss.com/)
-   **AI Engines**: Integration with DashScope (Qwen) and Doubao (Ark) LLMs

## 🛠️ Getting Started

### Prerequisites

-   Python 3.13+
-   Node.js 18+
-   API keys for DashScope or Doubao

### Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure environment variables:
    ```bash
    cp .env.example .env
    # Edit .env and add your API keys
    ```
5.  Run the server:
    ```bash
    python app/main.py
    ```

### Frontend Setup

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```

## 📂 Project Structure

-   `backend/`: FastAPI application, services, and API endpoints.
-   `frontend/`: Vue 3 source code, components, and assets.
-   `package.json`: Root configuration for the workspace.

## 📝 License

MIT License

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>