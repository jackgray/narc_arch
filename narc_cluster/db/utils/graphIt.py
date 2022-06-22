
from utils.dbConnect import getVertexCollection, getEdgeCollection, addEdge


def graphIt(graph, subjectsCollectionName, narc_id, questionaire, question, answer):
    
    # Format collection names
    if narc_id != '66666':
        allAssmnts_collectionName = 'Assessments'
        assmnt_collectionName = str(questionaire.upper()).replace(' ', '')
        subj_collectionName = subjectsCollectionName
        
        assmnt_q_edgeName = 'Assessment_Question_edges'
        assmntResp_edgeName = str("_".join([questionaire.upper(), '_Response_edges'])).replace(' ', '').replace('__', '_')
        # assmnt_edgeName = str("_".join([questionaire.upper(), '_Response_edges'])).replace(' ', '').replace('__', '_')

        # KEY/ID Definitions
        subject_id = "/".join([subjectsCollectionName, narc_id])
        subject_key = narc_id
        
        question_key = str(question).replace(' ', '').replace('_', '')
        answer_key = str(answer).replace(' ', '-').replace('_', '').replace(')','_').replace('(','_').replace('/', '-')
        question_id = "/".join([assmnt_collectionName, question_key])
        
        # Makes q and a combo it's own node
        # qa_key = "_".join([question_key, answer_key])
        # qa_id = "/".join([assmnt_collectionName, qa_key])

        assessment_key = assmnt_collectionName
        assessment_id = "Assessments/" + assessment_key.split('_')[0]
        
        # Separates q into one node with many responses
        
        
        
        
        # Vertex Collections Definitions
        subj_vertices = getVertexCollection(graph, subj_collectionName)
        assmnt_questions_vertices = getVertexCollection(graph, assmnt_collectionName)
        allAssmnts_vertices = getVertexCollection(graph, 'Assessments')
        
        
        # Edge Collection Definitions
        assmntResp_edges = getEdgeCollection(graph, assmntResp_edgeName, subj_collectionName, assmnt_collectionName)
        assmntResp_edge_id = "/".join([assmntResp_edgeName, '-'.join([question_key, subject_key])])
        print("EDGE ID: ", assmntResp_edge_id)
        
        assmnt_q_edges = getEdgeCollection(graph, assmnt_q_edgeName, allAssmnts_collectionName, assmnt_collectionName)
        
       
# VERTEX      
########     Assessments/WASI    ######

        try:
            allAssmnts_vertices.insert({"_key": assessment_key, 'questions': [question_id]})
        except:
            print("Could not insert into collection ", allAssmnts_vertices, ". It may already exist, so it will attempt to update")
            
            try:
                extant_assmnt_vertex = allAssmnts_vertices.get({"_id": assessment_id})
                
                print("Retrieved extant data for assmnt questions vertex")
                # for i in extant_assmnt_vertex:
                #     print(i)
                questions = [question_id]
                
                for i in extant_assmnt_vertex['questions']:
                    # print(i, "----", question)
                    questions.append(i)
                
                questions = list(dict.fromkeys(questions))

                res=graph.update_vertex({"_id": assessment_id, "questions": questions})

                # print(res)
                print("Success")
            except: 
                print("Could not update")
                




# VERTEX    
########        WASI/1        ####

        print("Attempting to insert question vertex ", question_id)
        try:
            assmnt_questions_vertices.insert({"_key": question_key, "question": question, "responses": [answer]})
            print("Success")
            
        except: 
            print("Could not insert into collection ", assmnt_questions_vertices, ". It may already exist, so it will attempt to update.")
            # pass
        
        extant_question_vertex = assmnt_questions_vertices.get({"_id": question_id})
        print("retrieved existing data for vertex")
        answers = [answer]
        
        for i in extant_question_vertex['responses']:
            print("appending existing response ", i , " to new array for added answer ", answer)
            answers.append(i)
    
        try:

                

            # subjects = list(dict.fromkeys(subjects))
            res=graph.update_vertex({"_id": question_id, "question": question, "responses": answers})
            print("Sucessfully updated vertex: ", res)
        except:
            print("FAILED: ",res)
        
        
# EDGE       
######    Assessments/WASI ------> WASI/1    ####

        print("Attempting to add edge from question to assessment")        
        print(assessment_id, "--->", question_id)
        try:
            res=addEdge(assmnt_q_edges, assessment_id, question_id)
            print("Success: ", res)
        except: 
            print("Could not create new edge connection. : ", res)
    
    
            


# EDGE
######    WASI/1 ----> MORE_Subjects/20001    ####

        print("Attempting to link subject to assessment question") 
        print(question_id, "-->", subject_id)      
        try:
            res=addEdge(assmntResp_edges, question_id, subject_id)
            print(res)
        except: 
            print(res)
        
        print("Attempting to update edge ", assmntResp_edgeName , " with response: ", assmntResp_edge_id, answer)
        print(assmntResp_edges)
        try:   
            res=graph.update_edge({"_id": assmntResp_edge_id, 'response': answer})
            print("Boo-ya: ", res)
        except: 
            print("Boo: ", res)

        # # Add to assessment list
        # try:
        #     allAssessments_vertices.insert({"_key": assessment_key, question:[answer]})
        # except:
        #     print("Could not insert assessment name to assessments collection. Attempting to update.")
        #     print("Retreiving existing data")    
        #     try:
        #         extant_assessment_data = allAssessments_vertices.get({"_id": assessment_id})
        #         print("Pulled existing assessment data")
        #         print(extant_assessment_data)
        #         try:
        #             appended_answers = [answer]
        #             for i in extant_assessment_data[question]:
        #                 print("Existing response: ", i)
        #                 answer.append(i)
        #             appended_answers = list(dict.fromkeys(appended_answers))
        #             graph.update_vertex({"_id": assessment_id, question: appended_answers})
        #         except:
        #             print("Could not update assessments collection with ", assessment_id)
        #     except:
        #         print("Could not retreive existing data for ", assessment_id)
        

        # subjects = [narc_id]
        # try:
        #     for i in extant_to_data['responses'][answer]:
        #         print('test')
        #         if len(i) > 0:
        #             print('test2')
        #             print(i)
        #             append_data.append(i)
        #     for i in extant_to_data['questions']            
        # except: 
        #     print("No existing data found to append to.")
        #     pass
        
        # append_data = list(dict.fromkeys(append_data)) # remove duplicates WARNING: may not apply to all cases 
        # print("Retreiving existing data")    
        # extant_to_data = toColl.get({"_id": to_id})
        # print(extant_to_data)
        
        # append_data = [narc_id]
        # try:
        #     for i in extant_to_data[add_field2][answer]:
        #         print('test')
        #         if len(i) > 0:
        #             print('test2')
        #             print(i)
        #             append_data.append(i)
                    
        # except: 
        #     print("No existing data found to append to.")
        #     pass
        
        # append_data = list(dict.fromkeys(append_data)) # remove duplicates WARNING: may not apply to all cases
        
        # # QUESTION DOCUMENT UPDATE
        # graph.update_vertex({"_id": to_id, "question": question, "response": { answer: append_data }})
        
        # try:
        #     addEdge(assessment, to_id, from_id)
        #     print("Successfully linked ", from_id, " with ", to_id, " via edge collection")
        # except:
        #     print("Couldn't link vertices ", from_id, " and ", to_id)    
        #     pass