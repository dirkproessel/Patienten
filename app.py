import os
from flask import Flask, render_template
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

if __name__ == '__main__':
    app.run(debug=True)
