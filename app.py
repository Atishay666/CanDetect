print("App Started")

from flask import Flask, render_template, request, send_file, redirect, session
import sqlite3
import pandas as pd
import os
from utils.gemini import generate_summary
from utils.predictor import predict_dataset
from utils.pdf_generator import generate_pdf

app = Flask(__name__)
app.secret_key = "candetect_secret_key"
def init_db():

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            email TEXT UNIQUE,

            password TEXT

        )
    """)

    conn.commit()

    conn.close()


init_db()

# ==========================
# Home Page
# ==========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":

        return render_template("register.html")

    name = request.form["name"]

    email = request.form["email"]

    password = request.form["password"]

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    try:

        cursor.execute(

            "INSERT INTO users(name,email,password) VALUES(?,?,?)",

            (name, email, password)

        )

        conn.commit()

    except:

        conn.close()

        return "Email already exists."

    conn.close()

    return redirect("/")
@app.route("/")
def home():

    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]

    password = request.form["password"]

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE email=? AND password=?",

        (email, password)

    )

    user = cursor.fetchone()

    conn.close()

    if user:

        session["user"] = user[1]

        return redirect("/prediction")

    return render_template(
    "login.html",
    error="Invalid Email or Password"
)
# ==========================
# Dashboard Page
# ==========================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ==========================
# Prediction Page
# ==========================

@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    # Check if user is logged in
    if "user" not in session:
        return redirect("/")

    # First time opening the page
    if request.method == "GET":
      return render_template(
    "prediction.html",
    total=None,
    fraud=None,
    genuine=None,
    fraud_rate=None,
    results=None,
    username=session["user"]
)
    # File uploaded
    file = request.files.get("csvfile")

    if file is None or file.filename == "":
        return render_template(
            "prediction.html",
            total=None,
            fraud=None,
            genuine=None,
            fraud_rate=None,
            results=None
        )

    print("=" * 50)
    print("CSV Received:", file.filename)

    # Read CSV
    df = pd.read_csv(file)

    print(df.head())
    print()
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("=" * 50)

    # AI Prediction
    (
        total,
        fraud,
        genuine,
        fraud_rate,
        result_df
    ) = predict_dataset(df)
    # Generate AI summary
    summary = generate_summary(
       total,
       fraud,
       genuine,
       fraud_rate
    )
    print("=" * 50)
    print("AI SUMMARY")
    print(summary)
    print("=" * 50)
    print(result_df[["Prediction", "Fraud Probability"]].head(20))
    # Save complete results for download
    os.makedirs("downloads", exist_ok=True)

    download_path = os.path.join(
        "downloads",
        "fraud_analysis_results.csv"
    )

    result_df.to_csv(download_path, index=False)

    print("=" * 50)
    print("Prediction Summary")
    print("Total Transactions :", total)
    print("Fraud Transactions :", fraud)
    print("Genuine Transactions :", genuine)
    print("Fraud Rate :", fraud_rate, "%")
    print("=" * 50)

    # Top 20 Highest Risk Transactions
    top20 = result_df.sort_values(
        by="Fraud Probability",
        ascending=False
    ).head(20)

    generate_pdf(
    "downloads/Fraud_Report.pdf",
    total,
    fraud,
    genuine,
    fraud_rate,
    summary,
    top20.to_dict(orient="records")
)

    return render_template(
    "prediction.html",
    total=total,
    fraud=fraud,
    genuine=genuine,
    fraud_rate=fraud_rate,
    results=top20.to_dict(orient="records"),
    summary=summary,
    username=session["user"]
)

# ==========================
# Download Results
# ==========================

@app.route("/download")
def download():

    return send_file(
        "downloads/Fraud_Report.pdf",
        as_attachment=True
    )


# ==========================
# Run App
# ==========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)