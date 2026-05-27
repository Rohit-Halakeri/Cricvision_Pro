import sys
import os
import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle

def train_impact_model():
    print("📊 Loading player data from SQLite database...")
    # Find the database path
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = os.path.join(base_dir, "cricvision.db")
    
    # Load data into a Pandas DataFrame
    conn = sqlite3.connect(db_path)
    query = """
        SELECT matches, runs, batting_average, strike_rate, 
               wickets, bowling_economy, impact_score 
        FROM players
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if len(df) < 50:
        print("⚠️ Not enough data! Please run the massive_roster.py script first.")
        return

    # Define our Features (X) and our Target (y)
    X = df[['matches', 'runs', 'batting_average', 'strike_rate', 'wickets', 'bowling_economy']]
    y = df['impact_score']

    # Split into 80% training data and 20% testing data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("🧠 Training Random Forest AI Model...")
    # Initialize and train the ML model
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # Test the model's accuracy
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"✅ Model trained successfully! Mean Squared Error: {mse:.2f}")

    # Save the trained model as a .pkl file so FastAPI can use it later
    ml_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(ml_dir, exist_ok=True)
    model_path = os.path.join(ml_dir, "impact_model.pkl")
    
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    
    print(f"💾 Trained model saved to: {model_path}")
    print("Your backend is now ready to make real AI inferences!")

if __name__ == "__main__":
    train_impact_model()
'''
### Your Instructions:
1. In VS Code, create a new folder inside `Backend/app/` called **`ml`**.
2. Inside that `ml` folder, create a file named **`train_model.py`**.
3. Paste the code from the Canvas above into it and save.
4. Open your terminal (stop the server with `Ctrl + C` if it is running) and run this exact command:
   ```powershell
   python -m app.ml.train_model

'''

