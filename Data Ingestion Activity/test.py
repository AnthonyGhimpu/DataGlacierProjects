import testutility as util
config_data = util.readConfigFile('file.yaml')

import pandas as pd
file_type = config_data['file_type']
source_file = './'+config_data['file_name'] + f'.{file_type}'
df = pd.read_csv(source_file,config_data['inbound_delimiter'])


util.col_header_val(df,config_data)