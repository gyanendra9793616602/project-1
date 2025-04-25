from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.rest import Client
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Twilio credentials
import os

account_sid = os.environ.get("AC4e21d2f4648c34f989c57a39c53b794d")
auth_token = os.environ.get("715689fc8fc98f9ea06b91297312e8a2")

account_sid = 'AC4e21d2f4648c34f989c57a39c53b794d'
auth_token = '715689fc8fc98f9ea06b91297312e8a2'
verify_sid = 'VA541c3116afafb4553cd5831421dd0e0b'  # Replace with your Twilio Verify Service SID

client = Client(account_sid, auth_token)

SEEKER_FILE = 'seeker.xlsx'
RECRUITER_FILE = 'recruiter.xlsx'

def save_to_excel(file_name, data):
    df_new = pd.DataFrame([data])
    if os.path.exists(file_name):
        df_existing = pd.read_excel(file_name)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_excel(file_name, index=False)

@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    phone = data.get('phone')

    try:
        verification = client.verify.v2.services(verify_sid).verifications.create(to=phone, channel='sms')
        return jsonify({'success': verification.status == 'pending'})
    except Exception as e:
        print("Error sending OTP:", e)
        return jsonify({'success': False})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    phone = data.get('phone')
    otp = data.get('otp')

    try:
        verification_check = client.verify.v2.services(verify_sid).verification_checks.create(to=phone, code=otp)
        return jsonify({'verified': verification_check.status == 'approved'})
    except Exception as e:
        print("Error verifying OTP:", e)
        return jsonify({'verified': False})

@app.route('/save-details', methods=['POST'])
def save_details():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role')

    if not all([name, email, phone, role]):
        return jsonify({"success": False, "error": "Missing fields"}), 400

    try:
        file_name = SEEKER_FILE if role == 'seeker' else RECRUITER_FILE
        save_to_excel(file_name, {
            'Name': name,
            'Email': email,
            'Phone': phone,
            'Role': role.capitalize()
        })
        return jsonify({"success": True})
    except Exception as e:
        print("Error saving to Excel:", e)
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
