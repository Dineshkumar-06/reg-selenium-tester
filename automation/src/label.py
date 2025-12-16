
from automation.src.selenium_driver import get_driver
from automation.src.config import DATA_JSON, DATA_DIR, REPORTS_DIR, LOGS_DIR

from automation.src.functions import diff_texts_html

from selenium.webdriver.common.by import By

from selenium.common.exceptions import *

import json

import pandas as pd

with open(DATA_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

app_identifier = data['app_identifier'].strip()
excel_file_name = data['excel_file_name'].strip()

# url = "https://regdemo.sifyitest.com/"+app_identifier+"/reg_details.php"
# url = "https://demo.sifyitest.com/prithivi/"+app_identifier+"/reg_details.php"
url = "https://staging.sifyreg.com/sanjana/"+app_identifier+"/reg_details.php"
print(url)
print("Entered label.py")

data_path = DATA_DIR / excel_file_name

output_html = REPORTS_DIR / "label_output.html"


driver = get_driver()
# driver.maximize_window()

driver.get(url)

fields = driver.find_elements(By.CLASS_NAME, "form-group")

exception_list = []

label_contents = []

html_ele_contents = []

for field in fields:
    # print(field)
    # print()
    try:
        label_element = field.find_element(By.TAG_NAME, "label")
        if label_element.is_displayed():
            label_text = label_element.text
            label_text = label_text.replace(" ", "")
            label_contents.append(label_text)
            # print(label_text)
            # print(label_element.get_attribute('outerHTML'))
    except:
        exception_list.append(f"Not able to find for {field}")
     
# print(label_contents)

c = 1
hc = 1

with open(LOGS_DIR / "label_app.txt", "w", encoding="utf-8") as file:
    for i in label_contents:
        file.write(f"{i}\n") 
        c += 1
    file.write(f"{c}\n")




# for i in exception_list:
#     print(i)

# ----------------------------------------------------------------------------------------------------------------------------

data_frame = pd.read_excel(data_path, sheet_name="Basic Details")
data_frame.dropna(axis=1, how='all', inplace=True)

# Prepare an empty list for processed labels
processed_labels = []

# Loop through each row and process
for idx, row in data_frame.iterrows():
    label = row['Label Name']
    mandatory = row['Mandatory ?']

    # Check if label is not missing or empty
    if (pd.notna(label) and str(label).strip() != "") and (pd.notna(mandatory) and str(mandatory).strip() != ""):
        label_str = str(label).strip().replace(" ", "")
        mandatory_str = str(mandatory).strip().lower() if pd.notna(mandatory) else ""
        if mandatory_str == 'yes':
            label_str += '*'
        
        processed_labels.append(label_str)

# Print or return
# print(processed_labels)

ce = 1
with open(LOGS_DIR / "label_excel.txt", "w", encoding="utf-8") as file:
    for i in processed_labels:
        file.write(f"{i}\n") 
        ce += 1
    file.write(f"{ce}\n")

diff_texts_html(LOGS_DIR / "label_excel.txt", LOGS_DIR / "label_app.txt", output_html)

# input("Press enter to quit the window...")
driver.quit()