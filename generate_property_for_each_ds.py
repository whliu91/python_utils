import os

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "datasource-properties")

json_template = '''        "{data_set}": {{
            "spark_properties": {{
                "targetPartition": "src_date",
                "recordDelimiter": "",
                "fieldDelimiter": "",
                "readerOptions": "sep=;",
                "readerFormat": "csv",
                "cleanseChar": "",
                "srcFormats": "src_date=yyyyMMdd",
                "srcToTgtColMap": "",
                "errorThresholdPercent": "",
                "writeMode": "append",
                "fileBasedTagPattern": "{data_set}_(\\\\d{{8}}).*.csv$",
                "fileBasedTagColumns": "src_date"
            }},
            "oozie_properties": {{
                "source_files_pattern": "{data_set}_*.csv"
            }},
            "test_properties":{{
                "expected_rows": "10"
            }}
        }},
'''

ds_property_json = ""

for file in os.listdir(os.path.join(PROJECT_ROOT, "src\\main\\sources\\headspin\\hive")):
    if file.endswith(".hql"):
        ds_property = json_template.format(data_set=file[:-4])
        ds_property_json += ds_property

vscode_dir = os.path.join(PROJECT_ROOT, "..", ".vscode")
if not os.path.exists(vscode_dir):
    os.makedirs(vscode_dir)

# write to specific location
f = open(os.path.join(vscode_dir, "temp.json"), 'w+')
f.write(ds_property_json[:-2])
f.close()