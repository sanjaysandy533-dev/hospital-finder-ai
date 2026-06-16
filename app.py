from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# This stores all hospitals
hospitals = []
hospital_id_counter = 1

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
        "insurance": [i.strip() for i in data["insurance"].split(",")]
    }
    hospitals.append(hospital)
    hospital_id_counter += 1
    return jsonify({"message": "Hospital added!", "hospital": hospital})

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

# Home page
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    # Delete hospital
@app.route("/delete/<int:hospital_id>", methods=["DELETE"])
def delete_hospital(hospital_id):
    global hospitals
    hospitals = [h for h in hospitals if h["id"] != hospital_id]
    return jsonify({"message": "Hospital deleted!"})