# book-summerization-and-recommendation

# 📚 BookMan — GenAI-Powered Book Recommendation & Summarization API

BookMan is a Flask-based backend system that uses GenAI to summarize books and recommend similar titles. It features JWT authentication, Swagger documentation, and modular architecture for scalable deployment.

---

## 🚀 Features

- 🔐 JWT-based authentication
- 🧠 GenAI-powered summarization (via Ollama)
- 📖 Book recommendation engine
- 📄 Swagger UI for API exploration
- 🗃️ Modular Flask blueprint structure
- 🛠️ Async-safe LLM invocation
- 🧪 Pytest-based test suite

---

## 🧰 Tech Stack

- Python 3.10+
- Flask + Flask-RESTX
- Ollama (local LLMs like Mistral, Llama3)
- SQLite (default) or PostgreSQL
- PyJWT
- Swagger (via Flask-RESTX)

---

## 🗄️ Database Setup
install PostgreSQL locally

### 1. Create `.env` file
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt


FLASK_ENV=development
JWT_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///bookman.db'''

**Innitialize db**
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

**run the project**

py run.py


### run the test case

pytest
