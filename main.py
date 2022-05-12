
from narc_cluster.db.configs.arango import config as arango
# from narc_cluster.db.calculated_fields.wrat import wratCalc
from narc_cluster.db.arango_queries.wasi import wasiUpdate
from narc_cluster.db.excel_conv.dMRI import csv2db

csv2db('./narc_cluster/db/excel_conv/MORE_dMRI_database_Time2_V2.xlsx')
