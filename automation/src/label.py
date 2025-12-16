
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.common.exceptions import *

import os
import math, json

import pandas as pd

from difflib_report import *

json_file = open('data.json')
data = json.load(json_file)

app_identifier = data['app_identifier'].strip()
excel_file_name = data['excel_file_name'].strip()

# url = "https://regdemo.sifyitest.com/"+app_identifier+"/reg_details.php"
# url = "https://demo.sifyitest.com/prithivi/"+app_identifier+"/reg_details.php"
url = "https://staging.sifyreg.com/sakthi/"+app_identifier+"/reg_details.php"
print(url)
print("Entered label.py")


folder_path = r"C:\Python files\automation_testing\flask\docs"
data_path = os.path.join(folder_path, excel_file_name)

service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)

chrome_options = Options()

chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=service, options=chrome_options)

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

with open("test_output.txt", "w", encoding="utf-8") as file:
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
with open("test_excel_op.txt", "w", encoding="utf-8") as file:
    for i in processed_labels:
        file.write(f"{i}\n") 
        ce += 1
    file.write(f"{ce}\n")

diff_texts_html('test_excel_op.txt', 'test_output.txt')

# input("Press enter to quit the window...")
driver.quit()