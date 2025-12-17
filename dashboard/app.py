import json
import subprocess
from pathlib import Path

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os 

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
AUTOMATION_DATA_DIR = PROJECT_ROOT / "automation" / "data"
AUTOMATION_DATA_DIR.mkdir(parents=True, exist_ok=True)

DATA_JSON = AUTOMATION_DATA_DIR / "data.json"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['GET','POST'])
def process():  
    app_identifier = request.form.get('app_identifier')
    excel_file = request.files.get('excel_file')
    test_single_dropdown = request.form.get('test_single_dropdown')
    test_dependent_dropdown = request.form.get('test_dependent_dropdown')
    test_label = request.form.get('test_label')

    messages = []
    status = "success"

    if not app_identifier or not excel_file or not test_single_dropdown or not test_dependent_dropdown or not test_label:
        messages.append("Upload all the required details!")
        return jsonify({
            'status': 'error',
            'message': messages 
        }), 400


    if excel_file:
        filename = excel_file.filename
        excel_path = AUTOMATION_DATA_DIR / filename
        excel_file.save(excel_path)
        messages.append("Data saved successfully!")
    else:
        messages.append("Failed")
        return jsonify({
            'status': 'error',
            'message': messages 
        }), 400 
    
    print("Data saved successfully!")
    
    new_data = {
        "app_identifier": app_identifier, 
        "excel_file_name": filename,
        "test_single_dropdown": test_single_dropdown,
        "test_dependent_dropdown": test_dependent_dropdown,
        "test_label": test_label,
    }

    with open(DATA_JSON, "w") as file:
        json.dump(new_data, file, indent=4)

    print("data.json saved successfully!")

    try:
        subprocess.run(
            ["python", "-m", "automation.src.main"],
            cwd=PROJECT_ROOT,
            check=True
        )
        messages.append("Automation testing completed successfully!")
    except subprocess.CalledProcessError as e:
        messages.append(f"Automation failed! {e}")
        status = "error"
    
    return jsonify({
    "status": status,
    "message": messages
    })

if __name__ == '__main__':
    app.run(debug=True)


