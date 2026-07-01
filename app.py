from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "hospital123"

# Simple login credentials
USERNAME = "admin"
PASSWORD = "hospital@123"

# This stores all hospitals
hospitals = []
hospital_id_counter = 1

# Login page
@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            error = "Wrong username or password!"
    return render_template("login.html", error=error)

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# Add hospital
@app.route("/add", methods=["POST"])
def add_hospital():
    global hospital_id_counter
    data = request.json
    hospital = {
        "id": hospital_id_counter,
        "name": data["name"],
        "specialties": [s.strip().lower() for s in data["specialties"].split(",")],
        "location": data["location"],
        "cost": data["cost"],
        "insurance": [i.strip() for i in data["insurance"].split(",")] if data["insurance"].strip() else ["No insurance"]
    }
    hospitals.append(hospital)
    hospital_id_counter += 1
    return jsonify({"message": "Hospital added successfully!", "hospital": hospital})

# Search hospital
@app.route("/search", methods=["POST"])
def search():
    data = request.json
    problem = data.get("problem", "").lower()
    matched = []
    for hospital in hospitals:
        for keyword in hospital["specialties"]:
            if keyword in problem:
                matched.append(hospital)
                break
    return jsonify(matched)

# Get all hospitals
@app.route("/all")
def all_hospitals():
    return jsonify(hospitals)

# Delete hospital
@app.route("/delete/<int:hospital_id>", methods=["DELETE"])
def delete_hospital(hospital_id):
    global hospitals
    hospitals = [h for h in hospitals if h["id"] != hospital_id]
    return jsonify({"message": "Hospital deleted!"})

if __name__ == "__main__":
    app.run(debug=True)