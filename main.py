
# from narc_cluster.db.configs.arango import config as arango
# from narc_cluster.db.calculated_fields.wrat import wratCalc
from narc_cluster.db.arango_queries.enrollment_group import enrollmentGroup
from narc_cluster.db.arango_queries.mri_data import mriData
from narc_cluster.db.excel_conv.mri_data import mriData

# from narc_cluster.db.excel_conv.dMRI import csv2db
from narc_cluster.db.excel_conv.forPrediction import forPrediction
# from narc_cluster.db.graphs.test import test
# from narc_cluster.db.transformations.enrollment_group import enrollmentGroup
from narc_cluster.db.file_server.crawl_dirs import crawlDirs

# csv2db('./narc_cluster/db/excel_conv/MORE_dMRI_database_Time2_V2.xlsx')
# crawlDirs()
# forPrediction()
mriData()