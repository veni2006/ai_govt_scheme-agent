from flask import Flask, render_template, request, jsonify
import json
from collections import Counter

app = Flask(__name__)

# Load scheme data
with open("schemes.json", "r") as f:
    schemes = json.load(f)

with open("fraud_schemes.json", "r") as f:
    fraud_keywords = json.load(f)

users_data = []


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/find_schemes", methods=["POST"])
def find_schemes():
    data = request.json

    age = int(data["age"])
    income = int(data["income"])
    category = data["category"].strip().lower()
    community = data["community"].strip().lower()
    state = data["state"].strip().lower()

    eligible = []
    missed_amount = 0

    for scheme in schemes:
        score = 0

        # Age
        if age >= scheme["min_age"]:
            score += 20

        # Income
        if income <= scheme["max_income"]:
            score += 30
        else:
            score += 10   # partial score even if income higher

        # Category
        if category == scheme["category"].lower():
            score += 20

        # Community
        if scheme["community"].lower() == "all" or community in scheme["community"].lower():
            score += 15

        # State
        if scheme["state"].lower() == "all" or state == scheme["state"].lower():
            score += 15

        # ✅ SHOW ALL SCHEMES WITH SCORE >= 20
        if score >= 20:
            scheme_copy = scheme.copy()
            scheme_copy["eligibility_score"] = score
            eligible.append(scheme_copy)

            if income <= scheme["max_income"]:
                missed_amount += scheme["benefit"]

    # Sort highest score first
    eligible = sorted(eligible, key=lambda x: x["eligibility_score"], reverse=True)

    users_data.append({
        "age": age,
        "income": income,
        "category": category,
        "community": community,
        "state": state
    })

    return jsonify({
        "eligible_schemes": eligible,
        "missed_benefit": missed_amount
    })

@app.route("/fraud_check", methods=["POST"])
def fraud_check():
    message = request.json["message"].lower()

    suspicious_patterns = [
        "pay", "processing fee", "click here",
        "urgent", "lottery", "guaranteed",
        "transfer money", "bank otp",
        "limited time", "registration fee"
    ]

    fraud_score = 0

    for word in suspicious_patterns:
        if word in message:
            fraud_score += 1

    if "http://" in message or "bit.ly" in message:
        fraud_score += 2

    return jsonify({
        "fraud": fraud_score <= 1,
        "fraud_score": fraud_score
    })


@app.route("/admin_data")
def admin_data():
    total_users = len(users_data)
    categories = [u["category"] for u in users_data]
    most_common_category = Counter(categories).most_common(1)

    return jsonify({
        "total_users": total_users,
        "most_common_category": most_common_category
    })


@app.route("/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(debug=True)