import difflib

def diff_texts_html(file1_path, file2_path, output_html="diff_output.html"):
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

# diff_texts_html(r'C:\Python files\automation_testing\test\test_excel_op.txt', r'C:\Python files\automation_testing\test\test_output.txt')


