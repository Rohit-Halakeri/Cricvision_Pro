<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
<img src="https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" />
<img src="https://img.shields.io/badge/LangChain-NLP-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />

<br /><br />

# 🏏 CricVision Pro

### AI-Powered Cricket Franchise Analytics Suite

*Simulate. Scout. Dominate.*

A full-stack sports intelligence platform integrating **Random Forest ML**, **LangChain NLP**, and **live ETL pipelines** — built for the modern franchise manager.

[Getting Started](#-quick-start) · [Features](#-features) · [Architecture](#-project-architecture) · [Roadmap](#-roadmap)

</div>

---

## 🎯 What is CricVision Pro?

CricVision Pro is a full-stack, AI-driven analytics platform that brings the power of a professional cricket franchise war room to your desktop. It combines real machine learning (not just heuristics), a conversational AI analyst, live data pipelines, and an interactive auction simulator — all in a zero-build React frontend.

Whether you're building your dream squad, predicting live match outcomes, or querying 10 years of ball-by-ball data in plain English, CricVision Pro has you covered.

---

## ✨ Features

### 🧠 True Machine Learning Engine
A custom-trained **scikit-learn Random Forest Regressor** predicts player impact scores using raw historical metrics. The model is trained on real Cricsheet data and persisted as a `.pkl` file — not mock scores or static lookup tables.

### 🤖 LangChain NLP Chatbot
An intelligent **conversational SQL agent** (powered by OpenAI GPT-3.5-turbo + LangChain) that translates plain-English questions into precise database queries. Includes a custom SQL fallback system for robustness.

> *"Who are the top 5 all-rounders by impact score in T20 matches since 2020?"* — just type it.

### 🏭 Automated ETL Data Pipelines
Live data hydration via **Pandas + BeautifulSoup4** — pulls ICC rankings and full ball-by-ball datasets from Cricsheet directly into the SQLite database. No manual CSV wrangling required.

### 📊 Visual Analytics Dashboard
A zero-build, highly optimised **React 18 + Tailwind CSS** frontend featuring:
- Live metric charts and player stat cards
- Conic-gradient data visualisers
- Dynamic stat generation with a crash-proof inline SVG icon engine

### ⚖️ Live IPL-Style Auction Simulator
A franchise **war room experience** where you bid against AI-driven rival franchises. Each AI opponent has a calculated max-bid limit, making every round competitive and unpredictable.

### 📈 Real-Time Win Predictor
Algorithmic live win probability based on **run-rate pressure** and **wicket-penalty heuristics** — updated ball by ball.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | FastAPI, Uvicorn |
| **Database** | SQLite3, SQLAlchemy ORM |
| **ETL / Data Engineering** | Pandas, BeautifulSoup4, Requests |
| **Machine Learning** | scikit-learn (Random Forest), Pickle |
| **AI / NLP** | LangChain, OpenAI GPT-3.5-turbo |
| **Frontend** | React 18 (CDN/Standalone) |
| **Styling** | Tailwind CSS |
| **Icons** | Custom Inline SVG Engine |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js (optional, for local tooling)
- An OpenAI API key

### 1. Clone the Repository

```bash
git clone https://github.com/Rohit-Halakeri/Cricvision_Pro.git
cd Cricvision_Pro
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

> ⚠️ Never commit your `.env` file. It is already included in `.gitignore`.

### 5. Hydrate the Database & Train the ML Model

Run these **in order** — the scraper must complete before training:

```bash
# Step 1: Pull live player data into the database
python -m app.scrapers.live_scraper

# Step 2: Train the Random Forest model on current data
python -m app.ml.train_model
```

### 6. Start the Backend Server

```bash
uvicorn app.main:app --reload
```

The API is now live at **`http://127.0.0.1:8000`**

> 📖 Visit `/docs` for the interactive Swagger UI — all endpoints are documented and testable there.

### 7. Launch the Frontend

Open `Frontend/frontend.html` directly in **Google Chrome**, **Edge**, or **Safari**. The frontend auto-connects to your local FastAPI instance — no build step needed.

---

## 📂 Project Architecture

```
Cricvision_Pro/
├── Backend/
│   └── app/
│       ├── api/            # FastAPI routers — Chat, Predictions, Players
│       ├── core/           # DB connection, config, settings
│       ├── ml/             # Random Forest training scripts & .pkl model
│       ├── models/         # SQLAlchemy ORM schemas
│       ├── scrapers/       # ETL pipelines (BeautifulSoup + Cricsheet/Pandas)
│       └── main.py         # FastAPI application entry point
│
├── Frontend/
│   └── frontend.html       # Consolidated React + Tailwind dashboard
│
├── cricvision.db           # SQLite database (auto-generated on first run)
├── requirements.txt        # Python dependencies
├── .env                    # API keys — git ignored
├── .gitignore
└── README.md
```

---

## 🔌 API Reference

Once the server is running, the full interactive API docs are available at:

| URL | Description |
|---|---|
| `http://127.0.0.1:8000/docs` | Swagger UI — interactive endpoint explorer |
| `http://127.0.0.1:8000/redoc` | ReDoc — clean API reference |

Key endpoint groups:

- **`/api/players`** — Player search, stats, ML impact scores
- **`/api/predictions`** — Match win probability, live score analysis
- **`/api/chat`** — NLP chatbot interface (LangChain SQL agent)

---

## 🔮 Roadmap

| Phase | Feature | Status |
|---|---|---|
| Phase 7 | **AI Squad Optimizer (Auto-Draft)** — Knapsack algorithm for optimal 11-player squad selection under salary cap | 🔜 Planned |
| Phase 7 | **Cloud Deployment** — Backend on Render, Frontend on Netlify | 🔜 Planned |
| Future | Advanced player comparison views | 💡 Idea |
| Future | Historical auction analytics | 💡 Idea |

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please ensure your code follows existing patterns and is tested before submitting.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built with ❤️ for the love of cricket and data engineering.

**[⭐ Star this repo](https://github.com/Rohit-Halakeri/Cricvision_Pro)** if you found it useful!

</div>