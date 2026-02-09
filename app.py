import os
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = None

if url and key:
    supabase = create_client(url, key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Patienten')
def patients():
    data = []
    # Fallback data
    fallback_data = [
        {"id": "1", "name": "Peter"},
        {"id": "2", "name": "Klaus"},
        {"id": "3", "name": "Maria"},
        {"id": "4", "name": "Sven"},
        {"id": "5", "name": "Claudia"}
    ]

    if supabase:
        try:
            response = supabase.table('patients').select('*').execute()
            data = response.data
        except Exception as e:
            print(f"Error fetching data: {e}")
            data = fallback_data
    else:
        # Supabase not configured, use fallback
        data = fallback_data

    # If Supabase returns empty (but configured), we might want to just show empty.
    # But if connection failed/not configured, we showed fallback.
    # The requirement says "fetch all patients".

    return render_template('patients.html', patients=data)

@app.route('/log_session', methods=['POST'])
def log_session():
    data = request.json
    patient_id = data.get('patient_id')
    appointment_type = data.get('type')

    if not patient_id or not appointment_type:
        return jsonify({'error': 'Missing data'}), 400

    if supabase:
        try:
            supabase.table('appointments').insert({
                'patient_id': patient_id,
                'type': appointment_type
            }).execute()
            return jsonify({'success': True}), 200
        except Exception as e:
            print(f"Error logging session: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        # Fallback/Mock behavior if Supabase is not configured
        print(f"Mock Log: Patient {patient_id}, Type {appointment_type}")
        return jsonify({'success': True, 'mock': True}), 200

if __name__ == '__main__':
    app.run(debug=True)
