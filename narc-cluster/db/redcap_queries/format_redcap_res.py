

def formatResp(response):
    for key,value in response.items():
        
        event_name = str(response['redcap_event_name'])
        repeat_instrument = str(response['redcap_repeat_instrument'])
        repeat_instance = str(response['redcap_repeat_instance'])
        record_id = str(response['record_id'])
        count=+1
        if len(str(value)) > 0 and value != '0':   
            # print(key, ": ", value) 
            treeDepth = []
            kelements= key.split('_')
            kelement_val = key.split("___")
            subcat = kelement_val[0].split('_')

            treeDepth =+ 1  # Each element is a subcategory
            # Each item in "all_records" is a different form.
            # Output in order of subject, a batch of forms is output for every subject
            # Some of the forms share the same key:value pairs, and will be overwritten if 
            # not separated into their own event subcategories
            if len(event_name) > 0:
                update_data = {
                    event_name: {
                        key: { 
                            value    
                        }
                    }
                }
                
        
            elif len(repeat_instrument) > 0 and repeat_instrument != subcat[0]:
                update_data = {
                    repeat_instrument: {
                        # a form could be filled out multiple times (i.e. follow up visits)
                        repeat_instance: {
                            # break off first element ('[0]') in '_' separated 
                            subcat[0]: {
                                # join the remaining elements and make that the final key for the value to match to 
                                # (formatting inconsistencies make uniform parcelation unpractical)
                                '_'.join(subcat[1:]): {
                                    kelement_val[-1]: {
                                        value
                                        }
                                    }
                                }  
                            }
                        }
                    }
            elif repeat_instrument == subcat[0]:
                update_data = {
                    repeat_instrument: {
                        repeat_instance: {
                            # join the remaining elements and make that the final key for the value to match to 
                            # (formatting inconsistencies make uniform parcelation unpractical)
                            '_'.join(subcat[1:]): {
                                kelement_val[-1]: {
                                    value
                                    }
                                }
                            }  
                        }
                }
                        
            else:
                update_data = {
                    # break off first element ('[0]') in '_' separated 
                    subcat[0]: {
                        # join the remaining elements and make that the final key for the value to match to 
                        # (formatting inconsistencies make uniform parcelation unpractical)
                        '_'.join(subcat[1:]): {
                            # kelement_val[-1]: {
                            value
                        }
                            # }
                    }  
                }
            
    print("{ 'record_id': ", record_id, ", ", update_data, '\n')