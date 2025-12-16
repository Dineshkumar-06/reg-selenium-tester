import json
import subprocess
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os 

app = Flask(__name__)
CORS(app)

path = r"C:\Python files\automation_testing\flask\docs"

json_data_file = "data.json"

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
    # print("Form keys:", request.form.keys())

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
        excel_file.save(os.path.join(path, filename))
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

    with open(json_data_file, "w") as file:
        json.dump(new_data, file, indent=4)

    print("data.json saved successfully!")
    
    if test_single_dropdown == "Y":
        try:
            subprocess.run(['python', 'single_dropdown.py'], check=True)
            print("single dropdown tested successfully!")
            messages.append("Single dropdown testing completed successfully!") 
        except Exception as e:
            messages.append(str(e)) 
            status = "error"
        
    if test_dependent_dropdown == "Y":
        try:
            subprocess.run(['python', 'dependent_dropdown.py'], check=True)
            print("Dependent dropdown tested successfully!")
            messages.append("Dependent dropdown testing completed successfully!") 
        except Exception as e:
            messages.append(str(e)) 
            status = "error"
        
    if test_label == "Y":
        try:
            subprocess.run(['python', 'label.py'], check=True)
            print("Labels tested successfully!")
            messages.append("Labels testing completed successfully!") 
        except Exception as e:
            messages.append(str(e)) 
            status = "error"
    
    return jsonify({
    "status": status,
    "message": messages
    })

    

""" @app.route('/dependent_process', methods=['POST'])
def dependent_process():
    app_identifier = request.form.get('app_identifier')
    excel_file = request.files.get('excel_file')


    messages = []

    if not app_identifier or not excel_file:
        messages.append("Upload all the required details!")
        return jsonify({
            'status': 'error',
            'message': messages 
        }), 400

    if excel_file:
        filename = excel_file.filename
        excel_file.save(os.path.join(path, filename))
        messages.append("Data saved successfully!")
    else:
        messages.append("Failed")
        return jsonify({
            'status': 'error',
            'message': messages 
        }), 400 
    
    new_data = {"app_identifier": app_identifier, "excel_file_name": filename,}

    with open(json_data_file, "w") as file:
        json.dump(new_data, file, indent=4)

    
    try:
        subprocess.run(['python', 'dependent_dropdown.py'], check=True)
        messages.append("Script executed successfully!") 
        return jsonify({
            'status': 'success',
            'message': messages 
        })
    except Exception as e:
        messages.append(str(e)) 
        return jsonify({
            'status': 'error',
            'message': messages 
        }), 500 """


if __name__ == '__main__':
    app.run(debug=True)


