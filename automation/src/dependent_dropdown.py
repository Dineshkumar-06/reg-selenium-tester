from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import *

import time
import json 
import os 

import pandas as pd

from functions import *

import math, json

json_file = open('data.json')
data = json.load(json_file)

app_identifier = data['app_identifier'].strip()
excel_file_name = data['excel_file_name'].strip()

# url = "https://regdemo.sifyitest.com/"+app_identifier+"/reg_details.php"
# url = "https://staging.sifyreg.com/pavithra/licnov25/reg_details.php?q=NjNlYzZhZGIwZTQxOTJjYzRkMDU5NDFkYWIxNTE1MjF8NzQ0MDAwMDAy"
url = "https://staging.sifyreg.com/dinesha/"+app_identifier+"/reg_details.php"

print(url)
folder_path = r"C:\Python files\automation_testing\flask\docs"
data_path = os.path.join(folder_path, excel_file_name)

service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)

chrome_options = Options()

chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=service, options=chrome_options)

# driver.get('https://demo.sifyitest.com/kathirvelu/niclaomay25/reg_details.php') 
driver.get(url)

driver.maximize_window()


selects_to_skip = ["day", "mon", "yr", "disability", "religion", "nationality"]

select_elements = driver.find_elements(By.TAG_NAME, "select")
select_ids = [sel.get_attribute('id') for sel in select_elements]

dependency_dict = {}


for i, parent_id in enumerate(select_ids):
    temp = []

    print(f"\n📌 Checking parent dropdown: {parent_id}")

    parent_element = driver.find_element(By.ID, parent_id)
    parent_select = Select(parent_element)

    if parent_id == "seldobday":
        print("Ending the process...")
        break 

    if (len(parent_select.options) < 2) or (any(key in parent_id for key in selects_to_skip)):
        print("Skipping this select!")
        continue
    
    # print(f"\nTesting parent: {parent_id}")

    for parent_option_index in range(1, 2):
        try:
            current_select_elements = driver.find_elements(By.TAG_NAME, "select")
            current_select_ids = [sel.get_attribute('id') for sel in current_select_elements]

            for j, child_id in enumerate(current_select_ids):
                
                if child_id == "seldobday":
                    # print("dob found breaking here😒")
                    break 
        
                if (i == j) or (any(key in child_id for key in selects_to_skip)):
                    continue  

                try:
                    child_element = driver.find_element(By.ID, child_id)
                    child_select = Select(child_element)
                    child_options_before = [opt.text for opt in child_select.options]
                except:
                    continue

                try:
                    parent_select.select_by_index(parent_option_index)
                except:
                    pass
                # print("Selected: ",parent_select.first_selected_option.text)
                time.sleep(1)
                
                # try:
                #     WebDriverWait(driver, 1).until(EC.alert_is_present())
                #     alert = driver.switch_to.alert
                #     alert.accept()
                # except Exception as e:
                #     pass 

                try:
                    child_element = driver.find_element(By.ID, child_id)
                    child_select = Select(child_element)
                    child_options_after = [opt.text for opt in child_select.options]
                except:
                    continue

                # print(*child_options_before, "=>", *child_options_after)

                if child_options_before != child_options_after:
                    print(f"✅ DEPENDENCY FOUND: '{parent_id}' ➔ '{child_id}'")
                    temp.append(child_id)
                    dependency_dict[parent_id] = temp
                else:
                    print(f"❌ No dependency: '{parent_id}' ➔ '{child_id}'")
                    pass
                
                
                parent_select.select_by_index(0)
                # print("Select option is selected")
                # print("Selected: ",parent_select.first_selected_option.text)
                    


        # except Exception as e:
        #     print(f"⚠️ Error handling {parent_id} ➔ {str(e)}")
        except StaleElementReferenceException:
            print("❓❓❓❓StaleElementReferenceException occurred on element id:", parent_id, child_id)

print(dependency_dict)

# driver.refresh()

try:
    driver.refresh()
except InvalidSessionIdException:
    print("Session expired, reinitializing driver...")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://demo.sifyitest.com/kathirvelu/niclaomay25/reg_details.php')

print("###################################################################################")

actual_dependent_dicts = {}

index = 0

for parent_key, item in dependency_dict.items():
    parent_element = driver.find_element(By.ID, parent_key)
    parent_select = Select(parent_element)
    parent_options = [opt.text for opt in parent_select.options]

    # parent_options = parent_options[1:]

    # print(parent_options)

    for i, id in enumerate(item):
        # print(i, id)
        temp_dependent_dict = {}
        child_element = driver.find_element(By.ID, id)
        child_select = Select(child_element)

        for parent_option_index in range(1, len(parent_options)):
            parent_select.select_by_index(parent_option_index)
            
            selected_option = parent_select.first_selected_option.text
            print("Selected option:", selected_option)

            child_element = driver.find_element(By.ID, id)
            child_select = Select(child_element)

            child_options = [opt.text for opt in child_select.options]

            child_options = child_options[1:]

            temp_dependent_dict[selected_option] = child_options

            print(selected_option, " => ", child_options)
        
        actual_dependent_dicts[id] = temp_dependent_dict


        print(id, " is done")

print(actual_dependent_dicts) 

driver.quit()
print("app dependency extracted!") 

# with open('dependency_mappings_app.json', 'w', encoding='utf-8') as f:
#     json.dump(actual_dependent_dicts, f, indent=4, ensure_ascii=False)

# exit()

##########################################################################################################

print("###################################################################################")

import pandas as pd


# data_path = r"C:\Python files\automation_testing\docs\sample_test_data.xlsx"

data_frame = pd.read_excel(data_path, sheet_name="dependent_dropdown")

# Drop empty columns
data_frame.dropna(axis=1, how='all', inplace=True)

expected_dependent_dicts = {}

columns = data_frame.columns.tolist()

revised_columns = [ col.strip().lower().replace(" ","_") for col in columns]

# print(revised_columns)

for i in range(0, len(data_frame.columns) - 1, 2):
    parent_col = data_frame.columns[i]
    child_col = data_frame.columns[i + 1]

    # Fill merged cells with the previous value 
    try:
        # data_frame[parent_col].fillna(method='ffill', inplace=True)
        data_frame[parent_col] = data_frame[parent_col].ffill()
    except:
        pass

    # Group into a dictionary based on the parent
    # dependency_map = data_frame.groupby(parent_col)[child_col].apply(lambda x: x.dropna().tolist()).to_dict()

    dependency_map = data_frame.groupby(parent_col, sort=False)[child_col].apply(
    lambda x: [
        item.strip() 
        for val in x.dropna() 
        for item in val.split(',') if item.strip()
    ]
    ).to_dict()

    cleaned_dependency_map = {
        key.strip(): value for key, value in dependency_map.items()
    }
    
    expected_dependent_dicts[f"{parent_col}_{i // 2}"] = cleaned_dependency_map

print("excel dependency extracted!") 


with open('dependency_mappings_excel.json', 'w', encoding='utf-8') as f:
    json.dump(expected_dependent_dicts, f, indent=4, ensure_ascii=False)

with open('dependency_mappings_app.json', 'w', encoding='utf-8') as f:
    json.dump(actual_dependent_dicts, f, indent=4, ensure_ascii=False)


res = dependent_dropdown_checker(expected_dependent_dicts, actual_dependent_dicts)

with open("dependent_dropdown_output.txt", "w", encoding="utf-8") as file:
    for i in res:
        file.write(f"{i}\n") 
    
