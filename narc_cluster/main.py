import json

from db.configs.arango import config
# from narc_cluster.db.configs.arango import config as arango
# from narc_cluster.db.calculated_fields.wrat import wratCalc
from db.arango_queries.group import groupQuery
from db.arango_queries.mri_data import mriData
from db.arango_queries.task_data import taskData
from db.arango_queries.ema import emaQuery
from db.mongo_queries.example import mongoTest
# from narc_cluster.db.excel_conv.mri_data import mriData
# from narc_cluster.db.excel_conv.dMRI import csv2db
from db.excel_conv.forPrediction import forPrediction
# from db.excel_conv.mri_data import mriData
# from narc_cluster.db.graphs.test import test
from db.migrations.redcap.enrollment import addEnrollments
# from db.migrations.redcap.all_records import allRecords
# from db.transformations.enrollment_group import enrollmentGroup
from db.file_server.crawl_dirs import crawlDirs
from db.utils.dbConnect import getCollection
from db.utils.narc_from_record import narcFromRecord

# db, collection = getCollection(config['db_name'], config['collection_name'])


# csv2db('./narc_cluster/db/excel_conv/MORE_dMRI_database_Time2_V2.xlsx')
# crawlDirs()
# forPrediction()
# print(json.dumps(mriData(), indent=2))
# print(json.dumps(taskData('choice'), indent=2))

# Example query data for all subjects by task
# task_data = taskData('choice')
# for i in task_data:
#     if i['group'] == 'OUD' or i['group'] == 'HUD':
#         print(i['subj'])
# addEnrollments()
# allRecords()
# mriData()
forPrediction()
# mongoTest()


# res = emaQuery()
# for i in res:
#     print('\n\n\n', i, '\nasdfasdf')
