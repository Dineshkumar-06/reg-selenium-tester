import json

import pandas as pd
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from automation.src.config import DATA_JSON, DATA_DIR, REPORTS_DIR, LOGS_DIR
from automation.src.functions import single_dropdown_checker
from automation.src.selenium_driver import get_driver


def run_single_dropdown():
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    app_identifier = data['app_identifier'].strip()
    excel_file_name = data['excel_file_name'].strip()

    url = "https://staging.sifyreg.com/sanjana/"+app_identifier+"/reg_details.php"
    print(url)
    print("Entered single_dropdown.py")


    data_path = DATA_DIR / excel_file_name

    driver = get_driver()

    driver.get(url)

    # Check whether the URL is valid
    if "404" in driver.title.lower():
        raise RuntimeError("Application URL returned 404 page")

    # Extract the single dropdown data from the application
    ids = driver.find_elements(By.XPATH, '//*[@id]')

    c = 1

    select_tag_ids = []

    selects_to_skip = ["day", "mon", "yr", "disability", "religion", "nationality", "subdistypeido" ]

    for i in range(0,len(ids)):
        if ids[i].tag_name == "select":
            if ids[i].get_attribute("id") == "seldobday":
                break
            if any(key in ids[i].get_attribute("id") for key in selects_to_skip):
                continue

            select_tag_ids.append(ids[i].get_attribute("id"))
            c += 1

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

    count = 0

    for i in actual_select_dict:
        count += 1

    driver.quit() 

    with open(LOGS_DIR / "single_dropdown_app.json", "w", encoding="utf-8") as f:
        json.dump(actual_select_dict, f, indent=4)
        

    # Extract the single dropdown data from the input excel file
    data_frame = pd.read_excel(data_path, sheet_name="single_dropdown")

    # Drop empty columns
    data_frame.dropna(axis=1, how='all', inplace=True)

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

    count1 = 0
    for i in expected_select_dict:
        count1 += 1

    with open(LOGS_DIR / "single_dropdown_excel.json", "w", encoding="utf-8") as f:
        json.dump(expected_select_dict, f, indent=4)
        
    # Invoking the comparison function
    res = single_dropdown_checker(actual_select_dict, expected_select_dict, "dropdown")

    with open(REPORTS_DIR / "single_dropdown_output.txt", "w", encoding="utf-8") as file:
        for i in res:
            file.write(f"{i}\n")

    print("exiting single_dropdown.py")


if __name__ == "__main__":
    run_single_dropdown()