import json
import time

import pandas as pd
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from automation.src.config import DATA_JSON, DATA_DIR, REPORTS_DIR, LOGS_DIR
from automation.src.functions import dependent_dropdown_checker
from automation.src.selenium_driver import get_driver


def run_dependent_dropdown():
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    app_identifier = data['app_identifier'].strip()
    excel_file_name = data['excel_file_name'].strip()

    url = "https://staging.sifyreg.com/sanjana/"+app_identifier+"/reg_details.php"

    print(url)

    data_path = DATA_DIR / excel_file_name


    driver = get_driver()

    driver.get(url)


    # Extract the dependent dropdown data from the application
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

        for parent_option_index in range(1, 2):
            try:
                current_select_elements = driver.find_elements(By.TAG_NAME, "select")
                current_select_ids = [sel.get_attribute('id') for sel in current_select_elements]

                for j, child_id in enumerate(current_select_ids):
                    
                    if child_id == "seldobday":
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

                    time.sleep(1)

                    try:
                        child_element = driver.find_element(By.ID, child_id)
                        child_select = Select(child_element)
                        child_options_after = [opt.text for opt in child_select.options]
                    except:
                        continue

                    if child_options_before != child_options_after:
                        print(f"✅ DEPENDENCY FOUND: '{parent_id}' ➔ '{child_id}'")
                        temp.append(child_id)
                        dependency_dict[parent_id] = temp
                    else:
                        print(f"❌ No dependency: '{parent_id}' ➔ '{child_id}'")
                        pass
                    
                    
                    parent_select.select_by_index(0)
                        

            except StaleElementReferenceException:
                print("❓❓❓❓StaleElementReferenceException occurred on element id:", parent_id, child_id)

    print(dependency_dict)


    try:
        driver.refresh()
    except InvalidSessionIdException:
        print("Session expired, reinitializing driver...")
        driver = get_driver()
        driver.get(url)


    actual_dependent_dicts = {}

    index = 0

    for parent_key, item in dependency_dict.items():
        parent_element = driver.find_element(By.ID, parent_key)
        parent_select = Select(parent_element)
        parent_options = [opt.text for opt in parent_select.options]

        for i, id in enumerate(item):
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

    with open(LOGS_DIR / "dependency_dropdown_excel.json", "w", encoding="utf-8") as f:
        json.dump(expected_dependent_dicts, f, indent=4, ensure_ascii=False)


    # Extract the dependent dropdown data from the input excel file
    data_frame = pd.read_excel(data_path, sheet_name="dependent_dropdown")

    # Drop empty columns
    data_frame.dropna(axis=1, how='all', inplace=True)

    expected_dependent_dicts = {}

    columns = data_frame.columns.tolist()

    revised_columns = [ col.strip().lower().replace(" ","_") for col in columns]

    for i in range(0, len(data_frame.columns) - 1, 2):
        parent_col = data_frame.columns[i]
        child_col = data_frame.columns[i + 1]

        # Fill merged cells with the previous value 
        try:
            data_frame[parent_col] = data_frame[parent_col].ffill()
        except:
            pass

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

    with open(LOGS_DIR / "dependency_dropdown_app.json", "w", encoding="utf-8") as f:
        json.dump(actual_dependent_dicts, f, indent=4, ensure_ascii=False)

    # Invoking the comparison function
    res = dependent_dropdown_checker(expected_dependent_dicts, actual_dependent_dicts)

    with open(REPORTS_DIR / "dependent_dropdown_output.txt", "w", encoding="utf-8") as f:
        for i in res:
            f.write(f"{i}\n") 
        
if __name__ == "__main__":
    run_dependent_dropdown()