import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Willkommen" in response.data

def test_patients_page(client):
    """Test that the patients page loads and displays fallback data (since no DB config)."""
    response = client.get('/Patienten')
    assert response.status_code == 200
    assert b"Patientenliste" in response.data
    # Check for fallback data names
    assert b"Peter" in response.data
    assert b"Claudia" in response.data

def test_log_session_endpoint(client):
    """Test that the log_session endpoint accepts POST requests."""
    response = client.post('/log_session', json={
        'patient_id': '123',
        'type': 'Einzelstunde'
    })
    assert response.status_code == 200
    assert response.json['success'] is True
