from io import BytesIO
import pandas as pd
import re

import_table_name = "city_data_table"

psg_user = 'myprojectuser'
psg_pwd = 'nitinsaini'
psg_host = '127.0.0.1'
psg_db_name = 'myproject'
psg_port = '5432'


def createDf(indexs, quotations, answers, owners, vendors_ctrl):
    df = pd.DataFrame({
        "#":indexs,
        "Quotations": quotations,
        "Answers": answers,
        "Owners":owners,
        "Corresponding Vendor Control":vendors_ctrl         
    })

    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        
        pd.io.formats.format.header_style = None
        df.to_excel(writer, sheet_name="Sheet1", index=False)

        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
    
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value)

        writer.save()

    return output


# santise table name
def sanitise_table_name(string):
    return re.sub('[^a-zA-Z0-9]', '_', string.strip().lower())

# Sanitise column name
def sanitise_column(value):
    # return value.strip().lower().replace(' ', '_').replace('(', '').replace('.', '_').replace(')', '').replace(',', '').replace('=','_').replace('-', '_').replace('#', '')
    return value.str.strip().str.lower().str.replace('[^A-Za-z\s]+', '').str.replace(' ', '_')

# def santize_column_name(value):
#     return value.str.strip().str.lower().str.replace('[^A-Za-z\s]+', '').str.replace(' ', '_')
