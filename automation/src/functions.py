import difflib

def single_dropdown_checker(actual_dict, expected_dict, type):
    actual_values = list(actual_dict.values())
    expected_values = list(expected_dict.values())

    actual_keys = list(actual_dict.keys())
    expected_keys = list(expected_dict.keys())

    field_name = []

    for key in expected_keys:
        key = key[4:]
        field_name.append(key)

    mismatches = []
        

    if len(actual_values) != len(expected_values):
        mismatches.append(f"⚠️ The number of fields in the excel and application is mismatched!")
        return mismatches
    
    
    for dict_index, (list1, list2) in enumerate(zip(actual_values, expected_values)):
        if len(list1) != len(list2):
            if len(list1) > len(list2):
                mismatches.append(f"⚠️ {field_name[dict_index]} is missing some of the options than expected")
            else:
                mismatches.append(f"⚠️ {field_name[dict_index]} has more number of options than expected")

        for list_index, (actual, expected) in enumerate(zip(list1, list2)):
            if actual != expected:
                mismatches.append(f"Mismatch at {field_name[dict_index]}, position {list_index}: expected '{expected}' vs actual '{actual}'")
   
        
    return mismatches if len(mismatches) > 0 else [f"All {type} values matched by value and order."]



def dependent_dropdown_checker(expected_dependent_dicts, actual_dependent_dicts):
    mismatches = []

    # Outer parent keys => main parent dropdown
    expected_outer_keys = list(expected_dependent_dicts.keys())
    actual_outer_keys = list(actual_dependent_dicts.keys())

    # Outer parent values => main parent dropdown
    expected_outer_values = list(expected_dependent_dicts.values())
    actual_outer_values = list(actual_dependent_dicts.values())


    if len(expected_outer_keys) != len(actual_outer_keys):
        mismatches.append("The number of fields in application and excel mismatched. Please prepare the excel correctly!")
        return mismatches
    
    # print(len(expected_outer_keys))
    

    for outer_dict_index in range(0, len(expected_outer_keys)):
        expected_current_child = expected_outer_values[outer_dict_index]
        actual_current_child = actual_outer_values[outer_dict_index]

        expected_current_keys = list(expected_current_child.keys())
        actual_current_keys = list(actual_current_child.keys())

        expected_current_values = list(expected_current_child.values())
        actual_current_values = list(actual_current_child.values())


        # print(expected_current_keys)
        # print("✅")
        # print(actual_current_keys)

        if len(expected_current_keys) != len(actual_current_keys):
            mismatches.append(f"⚠️ Field {outer_dict_index} actual number of values is mismatching with expected!")

            if len(expected_current_keys) > len(actual_current_keys):
                mismatches.append(f"⚠️ Field {outer_dict_index} is missing some of the dependencies than expected")
            else:
                mismatches.append(f"⚠️ Field {outer_dict_index} has more number of dependencies than expected")

        for key in expected_current_keys:
            try:
                expected_inner_values = expected_current_child[key]
                actual_inner_values = actual_current_child[key]
            except:
                mismatches.append(f"Parent field values in excel is mismatching that of in the application.")

            # mismatches.append(expected_inner_values)
            # mismatches.append(actual_inner_values)

            # Testing for children option length
            if len(expected_inner_values) != len(actual_inner_values):
                if len(expected_inner_values) > len(actual_inner_values):
                    mismatches.append(f"⚠️ {key}: is missing some of the options than expected")
                else:
                    mismatches.append(f"⚠️ {key}: has more number of options than expected")

            
            # Testing for children option value and order
            if expected_inner_values != actual_inner_values:
                
                for list_index, (expected, actual) in enumerate(zip(expected_inner_values, actual_inner_values)):
                    if expected != actual:
                        mismatches.append(f"🔥For Parent {outer_dict_index + 1}:\n❓For {key}:\n Mismatch at position {list_index}: expected '{expected}' vs actual '{actual}'\n")

                # mismatches.append(f"\nExpected:{expected_inner_values} is not equal to Actual: {actual_inner_values}")

            

        # mismatches.append(f"Dropdown {outer_dict_index} done\n")

    return mismatches if len(mismatches) > 0 else [f"All dependent dropdown values matched by value and order."]

def diff_texts_html(file1_path, file2_path, output_html):
    with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
        lines1 = f1.read().splitlines()
        lines2 = f2.read().splitlines()
        
    html_diff = difflib.HtmlDiff().make_file(lines1, lines2)

    style_insert = '''
    <style>
      body {
        font-family: Arial, sans-serif;
        font-size: 14px;
        color: #000;
        margin: 20px;
        background-color: #fff;
      }
      table.diff {
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #ccc;
        table-layout: fixed;
      }
      th, td {
        padding: 6px 8px;
        vertical-align: top;
        border: 1px solid #bbb;
        word-wrap: break-word;
        white-space: normal !important;
      }
      th.diff_header {
        background-color: #EAEAEA;
        font-weight: bold;
      }
      .diff_add {
        background-color: #D4FCDC;
      }
      .diff_sub {
        background-color: #FFD8D8;
      }
      .diff_chg {
        background-color: #FFF3B0;
      }
      .diff_next , .diff_next a{
        background-color: #F0F0F0;
        text-align: center;
        text-decoration: none;
        font-size: larger;
      }

       tr:has(.diff_add, .diff_sub, .diff_chg) {
        background-color: #e8e6e6;
        border: 1.5px solid black;
      }

      table.diff tr td:nth-child(3),
      table.diff tr td:nth-child(6) {
        width: 50%;
        max-width: 50%;
      }

      table.diff tr td:not(:nth-child(3)):not(:nth-child(6)) {
        text-align: center;
        width: 5%;
        max-width: 5%;
      }
    </style>
    '''
    html_diff = html_diff.replace('<head>', '<head>' + style_insert)

    # Generate side-by-side HTML diff

    # Write to output file
    with open(output_html, 'w' , encoding='utf-8') as f_out:
        f_out.write(html_diff)

    print(f"Diff output saved to {output_html}")



