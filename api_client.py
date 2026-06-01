import requests

SERVER_ALERTS_URL = "http://127.0.0.1:8000/alerts"
SERVER_ANALYZE_URL = "http://127.0.0.1:8000/analyze"
"""
   שכבת הרשת: אחראית אך ורק על משלוח הקבצים לשרת וניהול התקשורת
"""
def send_files_for_analysis(files_to_send):
    try:
        response = requests.post(SERVER_ALERTS_URL, files=files_to_send)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Server error (Status {response.status_code}): {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("\n Error: Could not connect to CodeGuard server.")
        print("Make sure your FastAPI backend is running via: uvicorn main:app --reload\n")
        return None

def send_files_for_graphs(files_to_send):
    try:
        response = requests.post(SERVER_ANALYZE_URL, files=files_to_send)
        if response.status_code == 200:
            with open("codeguard_report.zip", "wb") as f:
                f.write(response.content)
            print("📊 Graphs saved to codeguard_report.zip")
        else:
            print(f"Graph error (Status {response.status_code}): {response.text}")
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to CodeGuard server.")