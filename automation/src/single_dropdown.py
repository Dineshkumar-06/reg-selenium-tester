from automation.src.selenium_driver import get_driver
from automation.src.config import DATA_JSON, DATA_DIR, REPORTS_DIR, LOGS_DIR

from automation.src.functions import single_dropdown_checker

from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import *

import os
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
print("Entered single_dropdown.py")


data_path = DATA_DIR / excel_file_name


driver = get_driver()

driver.get(url)

ids = driver.find_elements(By.XPATH, '//*[@id]')

c = 1

""" Extracting select tags """ 

select_tag_ids = []

selects_to_skip = ["day", "mon", "yr", "disability", "religion", "nationality", "subdistypeido" ]

for i in range(0,len(ids)):
    if ids[i].tag_name == "select":
        if ids[i].get_attribute("id") == "seldobday":
            break
        if any(key in ids[i].get_attribute("id") for key in selects_to_skip):
            continue
        # print(c)
        # print("Tag name: "+ids[i].tag_name)
        # print("ID: "+ids[i].get_attribute("id"))
        # print("Name: "+ids[i].get_attribute("name"))
        select_tag_ids.append(ids[i].get_attribute("id"))
        c += 1

# print(select_tag_ids)

actual_select_dict = {}
expected_select_dict = {}

for i in range(0,len(select_tag_ids)):
    array_name = f"arr_{select_tag_ids[i]}"
    current_select = Select(driver.find_element("id", select_tag_ids[i]))
    current_options = current_select.options  

    current_select_options = [option.text.strip() for option in current_options]

    if len(current_select_options) < 2:
        continue

    actual_select_dict[array_name] = current_select_options

# print(select_dict) 

count = 0

for i in actual_select_dict:
    # print(i,actual_select_dict[i])
    count += 1
    # print("**********")


""" Extracting labels """

# label_ids = []

# rows = driver.find_elements(By.XPATH, "//table//tr")


driver.quit() 

with open(LOGS_DIR / "single_dropdown_app.json", "w", encoding="utf-8") as f:
    json.dump(actual_select_dict, f, indent=4)
################################################################################################
# print("#######################################################################################")

"""  Extracting data from excel """

# data_path = r"C:\Python files\automation_testing\flask\docs\'+excel_file_name+'.xlsx"

data_frame = pd.read_excel(data_path, sheet_name="single_dropdown")

# Drop empty columns
data_frame.dropna(axis=1, how='all', inplace=True)

# print(data_frame)

columns = data_frame.columns.tolist()

revised_columns = [ col.strip().lower().replace(" ","_") for col in columns]

print(columns)

expected_select_dict = {}

for i in range(0,len(columns)):
    temp = []
    array_name = f"arr_{revised_columns[i]}" 
    current_data = data_frame[columns[i]]
    last_index = current_data.last_valid_index()
    result = current_data.iloc[:last_index+1]
    for i in result:
        if pd.notna(i):
            temp.append(str(i).strip())
    temp.insert(0,"Select") 
    expected_select_dict[array_name] = temp

# print(expected_select_dict)

count1 = 0
for i in expected_select_dict:
    # print(i, expected_select_dict[i])
    count1 += 1
    # print("*")

# if count == count1:
#     print("Count matched!")
# else:
#     print(count, count1)
#     print("Mismatch!")

with open(LOGS_DIR / "single_dropdown_excel.json", "w", encoding="utf-8") as f:
    json.dump(expected_select_dict, f, indent=4)
    
res = single_dropdown_checker(actual_select_dict, expected_select_dict, "dropdown")

with open(REPORTS_DIR / "single_dropdown_output.txt", "w", encoding="utf-8") as file:
    # for key, val in expected_select_dict.items():
    #     file.write(f"{key} => {val}\n")
    # for key, val in actual_select_dict.items():
    #     file.write(f"{key} => {val}\n")
    for i in res:
        file.write(f"{i}\n")

print("exiting single_dropdown.py")


