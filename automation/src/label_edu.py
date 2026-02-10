import json

import pandas as pd
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By

from automation.src.config import DATA_JSON, DATA_DIR, REPORTS_DIR, LOGS_DIR
from automation.src.functions import diff_texts_html
from automation.src.selenium_driver import get_driver


def run_label():
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    app_identifier = data['app_identifier'].strip()
    excel_file_name = data['excel_file_name'].strip()

    # url = "https://staging.sifyreg.com/sanjana/"+app_identifier+"/reg_details.php"
    url = "https://staging.sifyreg.com/dinesh/bpscoct25/registration_print.php?q=MmNmMTE3YWMwNjJmMDk4MGE5YWJjZmY2MzRmZDgwNjV8NzQxMDAwMDA4&w=MXxhY3BuaW1kYXxNREV5TlRFeE1qVXhNakU1TXpRNFlXUm1ZV0l3TXpKaE0yUm1PREZpTURGaVpEYzVPRGRtTjJZMk9ERmhZdz09&admin_id="
    print(url)
    print("Entered label.py")

    data_path = DATA_DIR / excel_file_name

    output_html = REPORTS_DIR / "label_edu_output.html"


    driver = get_driver()

    driver.get(url)

    # Check whether the URL is valid
    if "404" in driver.title.lower():
        raise RuntimeError("Application URL returned 404 page")

    """ fields = driver.find_elements(By.TAG_NAME, "div")

    exception_list = []

    label_contents = []

    # Extract the label contents from the application
    for field in fields:
        try:
            label_text = field.text
            label_text = label_text.replace(" ", "")
            label_contents.append(label_text)
        except:
            exception_list.append(f"Not able to find for {field}") """
    
    label_contents = []
    
    
    # 1. Get ALL table rows (td elements)
    rows = driver.find_elements(By.TAG_NAME, "td")

    # 2. Process in pairs: Label (left td) + Value (right td)
    table_data = {}
    i = 0
    while i < len(rows) - 1:
        label = rows[i].text.strip()
        value = rows[i+2].text.strip()

        if label != "" and value != "":

            print(label, value)
            
            if label and ':' in label:  # Label format ends with ":"
                clean_label = label.replace(':', '').strip()
                table_data[clean_label] = value
        i += 3

    print("###########################################################")

    # 3. Print structured data
    for key, value in table_data.items():
        print(f"{key}: {value}")

    driver.quit()

    c = 1

    with open(LOGS_DIR / "label_edu_app.txt", "w", encoding="utf-8") as file:
        for i in table_data:
            file.write(f"{i}\n") 
            c += 1
        file.write(f"{c}\n")

    exit()


    # Extract the label contents from the input excel file
    data_frame = pd.read_excel(data_path, sheet_name="QualifiExperLang")
    data_frame.dropna(axis=1, how='all', inplace=True)

    processed_labels = []

    for idx, row in data_frame.iterrows():
        label = row['Label Name']
        mandatory = row['Mandatory ?']

        # Check if label is not missing or empty
        if (pd.notna(label) and str(label).strip() != "") and (pd.notna(mandatory) and str(mandatory).strip() != ""):
            label_str = str(label).strip().replace(" ", "")
            mandatory_str = str(mandatory).strip().lower() if pd.notna(mandatory) else ""
            if mandatory_str == 'yes':
                label_str += '*'

            if label_str not in processed_labels:
                processed_labels.append(label_str)

    ce = 1
    with open(LOGS_DIR / "label_edu_excel.txt", "w", encoding="utf-8") as file:
        for i in processed_labels:
            file.write(f"{i}\n") 
            ce += 1
        file.write(f"{ce}\n")

    # Invoking the report generation function
    diff_texts_html(LOGS_DIR / "label_edu_excel.txt", LOGS_DIR / "label_edu_app.txt", output_html)

if __name__ == "__main__":
    run_label()