import pandas as pd
from redcap import Project
from config import config


URL = config['api_url']
TOKEN = config['api_token']
proj = Project(URL, TOKEN)
# print(proj.field_names, pr
# pd.set_option("display.max_columns", 3)
records = proj.export_records(format_type="df", record_type="eav")
# with open('./records.csv', 'w') as file:
#     # file.write(records.to_csv())
#     recordfile = pd.read_csv(file)

# print(records)
# print(recordfile)

print('index:', records.DataFrame.index())
print('columns:', records.DataFrame.columns())
print('axes:', records.DataFrame.axes())
print('dimensions:', records.DataFrame.ndim())
print('shape:', records.DataFrame.shape())
