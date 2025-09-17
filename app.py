from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from twilio_service import send_sms  # Assuming you have this module

app = Flask(__name__)

# Connect to MongoDB Atlas
MONGO_URI = "mongodb+srv://khandvepratik8db:Pratik55%26@cluster0.dfd3odm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["BloodData"]
donors_col = db["DonorData"]

# Serve frontend HTML
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  # your HTML file should be named index.html and in "templates" folder

# List all donors
@app.route("/donors", methods=["GET"])
def get_donors():
    donors = list(donors_col.find({}, {"_id": 0}))  # Exclude Mongo _id
    return jsonify(donors)

# Request blood from donors
@app.route("/request-blood", methods=["POST"])
def request_blood():
    data = request.json
    hospital = data.get("hospital")
    patient_name = data.get("patient_name")
    blood_group = data.get("bloodGroup")

    # Find donors with that blood group and availability
    matching_donors = list(donors_col.find({"bloodGroup": blood_group, "available": True}, {"_id": 0}))

    # Send SMS to matching donors
    message = f"Urgent: {hospital} needs {blood_group} blood for {patient_name}. Reply 1 if available, 0 if not."
    for donor in matching_donors:
        try:
            send_sms(donor["phone"], message)
        except Exception as e:
            print(f"SMS failed for {donor['phone']}: {e}")

    # Return donor data for frontend
    return jsonify({
        "status": "success",
        "message": f"{len(matching_donors)} donors notified",
        "donors": matching_donors
    })

# Donor confirms availability
@app.route("/donor-response", methods=["POST"])
def donor_response():
    data = request.json
    donor_phone = data.get("phone")
    response = data.get("response")  # "1" or "0"

    donor = donors_col.find_one({"phone": donor_phone})
    if not donor:
        return jsonify({"status": "error", "message": "Donor not found"}), 404

    if response == "1":
        return jsonify({"status": "pending", "message": "Donor confirmed availability"})
    else:
        return jsonify({"status": "declined", "message": "Donor not available"})

# Guardian approves donation
@app.route("/guardian-response", methods=["POST"])
def guardian_response():
    data = request.json
    donor_phone = data.get("donor_phone")
    guardian_response = data.get("response")  # "YES" or "NO"

    donor = donors_col.find_one({"phone": donor_phone})
    if not donor:
        return jsonify({"status": "error", "message": "Donor not found"}), 404

    if guardian_response.upper() == "YES":
        new_points = donor.get("points", 0) + 10
        donors_col.update_one({"phone": donor_phone}, {"$set": {"points": new_points}})
        return jsonify({
            "status": "approved",
            "message": "Donation approved and points awarded",
            "points": new_points
        })
    else:
        return jsonify({"status": "rejected", "message": "Guardian rejected donation"})

# Top donors leaderboard
@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    sorted_donors = list(donors_col.find({}, {"_id":0}).sort("points", -1))
    return jsonify({"leaderboard": sorted_donors})

if __name__ == "__main__":
    app.run(debug=True)
