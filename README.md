🏏 CricVision Pro: AI-Powered Franchise Analytics Suite

CricVision Pro is a full-stack, AI-driven sports analytics platform designed to simulate franchise management, real-time match predictions, and professional scouting. It integrates live ETL data pipelines, True Machine Learning (Random Forest) for player impact valuation, and a LangChain-powered NLP chatbot to interact with the statistical database.

✨ Core Features

🧠 True Machine Learning Engine: Utilizes a custom-trained scikit-learn Random Forest Regressor to predict player impact scores based on raw historical metrics.

🤖 LangChain NLP Chatbot: A conversational SQL agent (powered by OpenAI & LangChain) that translates plain English queries into complex database queries (with a custom SQL fallback system).

🏭 Automated ETL Data Pipelines: Built with Pandas and BeautifulSoup4 to extract live ICC rankings and massive historical Cricsheet ball-by-ball datasets directly into system memory.

📊 Visual Analytics Dashboard: A zero-build, highly optimized React + Tailwind UI featuring live metric charts, dynamic stat generation, and conic-gradient data visualizers.

⚖️ Live Auction Simulator: A franchise war room that pits the user against AI-driven rival franchises in a mock bidding war, constrained by AI-calculated max-bid limits.

📈 Real-Time Win Predictor: Algorithmic calculation of live win probabilities utilizing run-rate pressure and wicket-penalty heuristics.

🛠️ Tech Stack

Backend & Data Engineering:

Framework: FastAPI, Uvicorn

Database: SQLite3, SQLAlchemy ORM

Data Pipeline (ETL): Pandas, BeautifulSoup4, Requests

Machine Learning: Scikit-Learn, Pickle

AI/NLP: LangChain, OpenAI GPT-3.5-turbo

Frontend:

Framework: React 18 (CDN/Standalone)

Styling: Tailwind CSS

Icons: Custom Inline SVG Engine (Crash-proof)

🚀 Installation & Setup

Follow these steps to run CricVision Pro on your local machine.

1. Clone the Repository

git clone [https://github.com/YOUR_USERNAME/cricvision-backend.git](https://github.com/YOUR_USERNAME/cricvision-backend.git)
cd cricvision-backend


2. Set Up a Virtual Environment (Recommended)

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate


3. Install Dependencies

Make sure you have a requirements.txt file containing FastAPI, Uvicorn, Pandas, Scikit-Learn, Langchain, etc.

pip install -r requirements.txt


4. Hydrate the Database & Train the ML Model

Run the data pipelines to build your database and train the AI brain:

# 1. Run the live scraper to fetch real players
python -m app.scrapers.live_scraper

# 2. Train the Random Forest ML Model based on current data
python -m app.ml.train_model


5. Start the FastAPI Server

uvicorn app.main:app --reload


The API will now be running on http://127.0.0.1:8000 (Visit /docs for the Swagger UI).

6. Launch the Frontend

Simply double-click the frontend.html file in your repository to open it in Google Chrome, Edge, or Safari. The frontend connects to your local FastAPI instance automatically!

📂 Project Architecture

CricVision-Pro/
├── app/
│   ├── api/                  # FastAPI Routers (Chat, Predictions, Players)
│   ├── core/                 # Database connection & configurations
│   ├── ml/                   # Machine Learning scripts & .pkl model
│   ├── models/               # SQLAlchemy ORM schemas
│   ├── scrapers/             # ETL Pipelines (BeautifulSoup, Cricsheet Pandas)
│   └── main.py               # FastAPI application entry point
├── frontend.html             # Consolidated React + Tailwind Dashboard
├── cricvision.db             # Local SQLite Database (Generated)
├── requirements.txt          # Python dependencies
├── .env                      # API Keys (Git Ignored)
└── README.md                 # Project Documentation


🔮 Future Roadmap (Phase 7)

AI Squad Optimizer (Auto-Draft): Implementation of a Knapsack-problem algorithm to automatically select the mathematically optimal 11-player squad under a strict salary cap constraint.

Cloud Deployment: Hosting the backend on Render and frontend on Netlify.

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.