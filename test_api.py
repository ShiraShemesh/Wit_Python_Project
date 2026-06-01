import requests

url = "http://127.0.0.1:8000/alerts"

# אנחנו שולחים את הקבצים שכבר קיימים בתוך תיקיית backend
files = [
    ('files', ('Main.py', open('backend/Main.py', 'rb'), 'text/plain')),
    ('files', ('analyzer.py', open('backend/analyzer.py', 'rb'), 'text/plain'))
]

print("שולח בקשה לשרת עם שני קבצים במקביל...")
try:
    response = requests.post(url, files=files)
    print("\n--- תשובת השרת (JSON) ---")
    print(response.json())
except Exception as e:
    print(f"שגיאה בתקשורת: {e}")