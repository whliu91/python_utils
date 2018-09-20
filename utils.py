import os
import csv
import decimal

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

if __name__ == "__main__":
    # testing
    res = read_csv_to_list("C:\\Users\\d891834\\projects\\harmony\\ingestion_curation\\datasource-properties\\src\\test\\resources\\sources\\expectedoutput\\r\\c\\edevil\\w_headroom_nodeb\\w_Headroom_NodeB_20180907.csv")
    new_list_of_list = []
    for column in res:
        new_list = []
        for val in column:
            if is_number(val) and float(val) > 0.000001:
                val = str(reduce_to_decimals(val))
                if 'E' in val.upper():
                    power = -int(val.upper().split('E')[1])
                    val = scientific_to_normal(val, 9-power)
                if len(val) < 10:
                    for i in range(10 - len(val)):
                        val += "0"

            new_list.append(val)
        
        new_list_of_list.append(new_list)
    
    print(new_list_of_list)
    write_list_to_csv(new_list_of_list, "C:\\Users\\d891834\\projects\\harmony\\ingestion_curation\\datasource-properties\\src\\test\\resources\\sources\\expectedoutput\\r\\c\\edevil\\w_headroom_nodeb\\w_Headroom_NodeB_20180907.csv")


