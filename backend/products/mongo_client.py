import json

from pymongo import MongoClient
from backend_f.config import MONGO_URI

def get_mongo_client():
    # Construct MongoDB URI
    client = MongoClient(MONGO_URI)
    return client['pricecomparator']
def get_max_data():
    client = get_mongo_client()
    parameters_collection = client.get_collection('parameters')  
    result = parameters_collection.find_one({}, sort=[("parameters.maximum_index_number", -1)])
    if not result:
        initial_data = {'parameters': {'maximum_index_number': 0, 'name': 'main_parameters'}}
        parameters_collection.insert_one(initial_data)
        return initial_data['parameters']['maximum_index_number']
    return result['parameters']['maximum_index_number']

def update_max_param_data(numer_of_increments):
    client = get_mongo_client()
    db = client
    parameters_collection = db.get_collection('parameters')
    result = parameters_collection.find_one({}, sort=[("parameters.maximum_index_number", -1)])
    parameters_collection.update_one(
        {'parameters.name': 'main_parameters'}, 
        {"$set": {
            'parameters.maximum_index_number': result['parameters']['maximum_index_number'] + numer_of_increments}}
    )

def add_data_to_tracker(data_to_insert):
    client = get_mongo_client()
    parameters_collection = client.get_collection('trackeditems')
    result = parameters_collection.insert_one(data_to_insert["data"])
    return {"Data":"Inserted","data_to_insert":data_to_insert}

def delete_data_from_tracker(id):
    client = get_mongo_client()
    parameters_collection = client.get_collection('trackeditems')
    result = parameters_collection.delete_one({'parameters.id':id})
    return result.raw_result
def get_data_from_tracker():
    client = get_mongo_client()
    parameters_collection = client.get_collection('trackeditems')
    cursor = parameters_collection.find({})
    documents = list(cursor)
    for item in documents:
        item['_id'] = str(item['_id'])
    return documents



if __name__=='__main__':
    print(update_max_param_data(0))
