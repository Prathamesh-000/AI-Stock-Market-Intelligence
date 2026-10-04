# 📈 Quant AI Terminal

![Quant AI Terminal UI](https://img.shields.io/badge/UI-React_%7C_Tailwind-blue?style=for-the-badge&logo=react)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)
![Machine Learning](https://img.shields.io/badge/ML-XGBoost-orange?style=for-the-badge)
![NLP](https://img.shields.io/badge/NLP-OpenAI_%7C_FinBERT-green?style=for-the-badge)

An institutional-grade, real-time stock market intelligence platform that combines **Large Language Models (LLMs)** with **Quantitative Machine Learning (XGBoost)** to predict short-term stock movements from breaking news.

Instead of just summarising news, this system acts as an autonomous quantitative analyst. It ingests a headline, parses the fundamental event, fetches similar historical precedents from a Vector Database, evaluates the sentiment, and passes the feature vector to a calibrated XGBoost model to generate a strict, mathematically defensible trading signal.

---

## ✨ Key Features

* **🧠 Live NLP Pipeline (OpenAI + FinBERT)**: Instantly parses unstructured news headlines, identifies the exact event structure (e.g., "Product Launch", "Earnings Miss"), and calculates a highly accurate sentiment polarity score.
* **📈 XGBoost Quantitative Engine**: A heavily trained machine learning classifier (calibrated via Platt Scaling) that calculates the exact probability of a positive/negative price reaction. It applies strict risk-management, issuing a `SKIP (Uncertain)` signal if the confidence drops below the required threshold.
* **🌊 Sector Ripple Engine**: Uses multi-output regression models to mathematically predict how a catalyst for a primary stock (e.g., NVDA) will cascade across its sector competitors (AMD, TSM, INTC).
* **📚 Historical Precedents (RAG)**: Powered by an OpenAI Embeddings Vector Database, the system instantly matches incoming breaking news against a database of historical events, calculating cosine similarity to find out how the market reacted the last time a similar event occurred.
* **🖥️ Bloomberg-Style React Dashboard**: A stunning, fully interactive frontend powered by WebSockets. It features real-time simulated intraday charts, interactive watchlists, and a transparent breakdown of the AI's reasoning (removing the "black box" of AI).
* **🎯 Model Performance Tracking**: Automatically logs predictions to an SQLite database and tracks the AI's directional accuracy against actual historical market returns.

---

## 🏗️ System Architecture

The pipeline executes in milliseconds via background tasks to ensure non-blocking WebSocket streams:

1. **Ingestion**: The user submits a ticker (e.g., NVDA) and a breaking rumor/headline via the React UI.
2. **Retrieval (RAG)**: The backend queries the Vector Database to fetch similar historical events.
3. **NLP Analysis**: The LLM analyzes the text, assigns an impact score (0-100), extracts the event type, and generates the fundamental reasoning.
4. **Feature Engineering**: The pipeline constructs a live mathematical feature vector combining the NLP scores, historical volatility (simulated 5-day variance), and similar-event scores.
5. **Inference**: The XGBoost model calculates the raw log-odds, which are converted to a strict probability via the Logistic Calibrator.
6. **Broadcasting**: The final payload is saved to the SQLite database and broadcasted globally via WebSockets to all connected React clients.

---

## 🛠️ Tech Stack

### Frontend
* **React 18** (Vite)
* **TypeScript**
* **Tailwind CSS** (Styling & Animations)
* **Recharts** (Data Visualization & Intraday Price AreaCharts)
* **Lucide React** (Icons)

### Backend
* **Python 3.10+**
* **FastAPI** (REST Endpoints & WebSockets)
* **SQLite & SQLAlchemy** (Relational Database / ORM)
* **Pydantic** (Data Validation)

### Machine Learning & AI
* **XGBoost** (Gradient Boosted Trees for Directional & Ripple predictions)
* **Scikit-Learn** (Platt Scaling Calibration)
* **Pandas & NumPy** (Data processing)
* **OpenAI API** (GPT-4o for event extraction, `text-embedding-3-small` for Vector DB)
* **FinBERT** (Financial Sentiment NLP)

---

## 🚀 Getting Started

### 1. Backend Setup
Navigate to the project root and activate your virtual environment:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

Install backend dependencies:
```bash
pip install -r requirements.txt
```

Set up your `.env` file:
```env
OPENAI_API_KEY=your_api_key_here
```

Start the FastAPI server:
```bash
python src/api/main.py
```
*(The backend runs on `http://localhost:8000`)*

### 2. Frontend Setup
Open a second terminal, navigate to the frontend directory, and start the Vite dev server:
```bash
cd frontend
npm install
npm run dev
```
*(The frontend runs on `http://localhost:3000`)*

---

## 📊 Using the Dashboard

1. **Select a Ticker**: Click on a stock (e.g., NVDA, AMD, AAPL) from the Watchlist panel on the left.
2. **Submit a Headline**: Paste a breaking news headline (e.g., *"Apple rumored to delay iPhone 17 production due to supply chain constraints"*) into the Feed News input.
3. **Execute AI**: Click the button. The UI will stream the prediction, revealing the live intraday chart, the expected 1-hour return, the explicit FinBERT sentiment breakdown, and the historical matches.

---

## 📝 License
This project was built as an advanced portfolio demonstration of AI-driven Quantitative Finance.
