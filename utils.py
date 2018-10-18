import os
import csv
import decimal
import re

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

if __name__ == "__main__":
    # testing
    ddl = '''CREATE DATABASE IF NOT EXISTS c_nsbu_headspin;
CREATE EXTERNAL TABLE IF NOT EXISTS c_nsbu_headspin.device_loc
(  `iteration_number` bigint,
`location` string,
`machine_name` string,
`device_id` string,
`device_type` string,
`latitude` float,
`longitude` float,
`lat_lon` string)
STORED AS ORC
LOCATION '/data/c/nsbu/headspin/device_loc';
    '''

    print(get_list_of_fields_from_ddl(ddl))