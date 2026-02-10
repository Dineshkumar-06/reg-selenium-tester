import json
import subprocess
from pathlib import Path

from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
AUTOMATION_DATA_DIR = PROJECT_ROOT / "automation" / "data"
AUTOMATION_DATA_DIR.mkdir(parents=True, exist_ok=True)

DATA_JSON = AUTOMATION_DATA_DIR / "data.json"

# Reports directory (serve generated reports from here)
REPORTS_DIR = PROJECT_ROOT / "automation" / "outputs" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reports/<path:filename>')
def download_report(filename):
    return send_from_directory(str(REPORTS_DIR), filename, as_attachment=True)

@app.route('/process', methods=['GET','POST'])
def process():  
    app_identifier = request.form.get('app_identifier')
    dev_name = request.form.get('dev_name')
    excel_file = request.files.get('excel_file')
    test_single_dropdown = request.form.get('test_single_dropdown')
    test_dependent_dropdown = request.form.get('test_dependent_dropdown')
    test_label = request.form.get('test_label')

    response = {
        "status": "started",
        "messages": []
    }
    
    if not app_identifier or not dev_name or not excel_file or not test_single_dropdown or not test_dependent_dropdown or not test_label:
        response["status"] = "error"
        response["messages"].append("Upload all the required details!")
        return jsonify(response), 200

    if excel_file:
        filename = excel_file.filename
        excel_path = AUTOMATION_DATA_DIR / filename
        excel_file.save(excel_path)
        response["messages"].append("Data saved successfully!")
    else:
        response["messages"].append("Failed to save the excel file!")
        response["status"] = "error"
        return jsonify(response), 200
    
    print("Data saved successfully!")
    
    new_data = {
        "app_identifier": app_identifier, 
        "dev_name": dev_name, 
        "excel_file_name": filename,
        "test_single_dropdown": test_single_dropdown,
        "test_dependent_dropdown": test_dependent_dropdown,
        "test_label": test_label,
    }

    with open(DATA_JSON, "w") as file:
        json.dump(new_data, file, indent=4)

    print("data.json saved successfully!")

    try:
        result = subprocess.run(
            ["python", "-m", "automation.src.main"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            response["status"] = "success"
            response["messages"].append("Automation completed successfully")
            # Attempt to locate the most recent HTML report and return its URL
            try:
                reports = sorted(REPORTS_DIR.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
                if reports:
                    latest = reports[0]
                    response["report_url"] = url_for('download_report', filename=latest.name)
            except Exception:
                pass
        else:
            response["status"] = "error"
            response["messages"].append("Automation testing failed")

            if result.stderr:
                last_line = result.stderr.strip().splitlines()[-1]
                response["messages"].append(last_line)
            else:
                response["messages"].append("Unknown error occurred")

    except Exception as e:
        response["status"] = "error"
        response["messages"].append("Unexpected server error")
        response["messages"].append(str(e))

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)


