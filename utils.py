import os
import csv
import decimal
import re
from shutil import copyfile
from datetime import datetime

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def transpose_list_of_list(mat):
    '''Transpose a list of list
    '''
    return map(list, zip(*mat))


def underscore_to_camelcase(val):
    '''Convert underscore based naming format to camel case based, with the first letter 
    capitalised, with first char capitalised
    '''
    list_val = list(val)
    list_val[0] = list_val[0].upper()
    while '_' in list_val:
        ind = list_val.index('_')
        list_val[ind+1] = list_val[ind+1].upper()
        list_val[ind] = ''

    res = ''.join(list_val)
    return res

def is_number(s):
    '''decided whether a string is number
    '''
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def read_csv_to_list(file_name):
    '''Read csv file to list of list
    '''
    with open(file_name, 'rU') as f:
        reader = csv.reader(f)
        data = list(list(rec) for rec in csv.reader(f, delimiter=','))
    
    return data

def write_list_to_csv(list_of_col, file_name):
    '''Write list of col to file as csv
    '''
    text = ""
    for item in list_of_col:
        line = ','.join(item)
        text += line + '\n'
    
    text = text[:-1]
    
    f = open(file_name, 'w+')
    f.write(text)
    f.close()


def reduce_to_decimals(value, decimals=8):
    '''Reduce a float number to (default 8) decimals
    '''
    format_str = "{{0:.{decimals}f}}".format(decimals=decimals)
    return float(format_str.format(float(value)))

def scientific_to_normal(val, prec=8):
    '''
    Convert the given float to a string,
    without resorting to scientific notation
    '''
    ctx = decimal.Context()
    ctx.prec = prec
    d1 = ctx.create_decimal(repr(float(val)))
    return format(d1, 'f')

def get_list_of_fields_from_ddl(ddl):
    '''Get all column names as list from ddl
    depends on column names to be between `` and line separated
    '''
    lines = ddl.split("\n")
    results = []
    for line in lines:
        result = re.search('`(.*)`', line)
        if result:
            results.append(result.group(1))
    return results

def append_header_to_csv(csv_file, headers):
    '''Append header (in a list) to csv file
    '''
    with open(csv_file, newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
    with open(csv_file, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(data)

def append_to_file_name_in_folder_with_extensions(folder, extension, addon):
    '''
    something.csv to somethingaddon.csv
    '''
    for file in os.listdir(folder):
        if file.endswith(extension):
            newname = file.replace(extension, addon + extension)
            os.rename(os.path.join(folder, file), os.path.join(folder, newname))

def create_folder_in_folder_from_list(folder, folder_list):
    '''Create all folders in the list in the folder given
    '''
    for item in folder_list:
        full_path = os.path.join(folder, item)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

def copy_file_from_list_to_corresponding_folder(src_dir, dst_dir, ext):
    '''Copy files from src dir to corresponding folder in dst_dir, by name
    /src_dir/something_123456.csv -> /dst_dir/something/something_123456.csv
    '''
    for file in os.listdir(src_dir):
        if file.endswith(ext):
            file_full_path = os.path.join(src_dir, file)
            for folder in os.listdir(dst_dir):
                if folder in file:
                    copyfile(file_full_path, os.path.join(dst_dir, folder, file))

def add_date_to_csv_from_filename(src_dir):
    for folder in os.listdir(src_dir):
        regex_pattern = folder + "_(\d{8}).*.csv"
        for file in os.listdir(os.path.join(src_dir, folder)):
            result = re.search(regex_pattern, file)
            src_date_raw = result.group(1)
            src_date = datetime.strptime(src_date_raw, "%Y%m%d")
            src_date_formatted = src_date.strftime("%Y-%m-%d")
            file_full_path = os.path.join(src_dir, folder, file)
            csv_data = read_csv_to_list(file_full_path)
            if "src_date" not in csv_data[0]:
                count = 0
                for row in csv_data:
                    if count == 0:
                        row.append("src_date")
                    else:
                        row.append(src_date_formatted)
                    count += 1
                
                write_list_to_csv(csv_data, file_full_path)


def get_field_from_create_table_statement(stmt):
    '''Get fields from sql create table statement
    WIP: this is buggy: does not work if there is Decimal(xxx,xxx) within fields
    '''
    pattern = r'\(((.|\n)*?)\)'
    fields = re.search(pattern, stmt).group(1)
    rows = [item.strip() for item in fields.replace("\n", "").replace("`", "").split(',')]
    field_names = [row.split()[0] for row in rows]
    return field_names

if __name__ == "__main__":
    pass