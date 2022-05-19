from collections import Counter
from pandas import pandas as pd
import re
import json

from narc_cluster.db.calculated_fields.wasi import wasiCalc
from narc_cluster.db.dbConnect import getCollection
from narc_cluster.db.dbUpdate import updateArango


def emaQuery():
    db, collection = getCollection('MORE', 'subjects3')

    query_result = db.aql.execute(
        'FOR s IN subjects3 \
            FILTER s.assessments.ema != null \
            RETURN { narc_id: s._key, ema: s.assessments.ema, asi_drug: s.assessments.asi.drug }',
        batch_size=1
    )

    for subject in query_result:
        ema_days = subject['ema']
        # print(json.dumps(ema_days, indent=2))
        for day, questions in ema_days.items():
            if 'arm' not in day:
                day_int = int(day.split('day_')[-1])
                for question, resp in questions.items():
                    # 3. "How badly do you want to use drugs? 0-10"
                    if question == '3' and day_int > 15 and int(resp) > 7:
                        print(day, subject['narc_id'])
                        
                        # Query more data by adding condition to the AQL RETURN statement,
                        # or by sending a second query only when warranted (below)
                        for drug, drug2 in subject['asi_drug'].items():
                            try: print(drug,drug2['ao']) 
                            except: pass
                            
                        # Alternate way to retrieve data (more granular)
                        new_data = collection.find({'_key': subject['narc_id']})
                        for focus_subject in new_data:
                            asi = focus_subject['assessments']['asi']
                            for drug, drug_qs in asi['drug'].items():
                                # Use try statement to handle errors where no data exists
                                try: print(drug, drug_qs['ao'])
                                except: pass
                        # print(json.dumps(new_data, indent=2))
            
   
    
            
    