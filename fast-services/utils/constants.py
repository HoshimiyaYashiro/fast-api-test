# declare constants
from enum import Enum


models = {
    'user': 'user',
    'users': 'users',
    'profile': 'profile'
}


crud_messages = {
    'updated': 'updated successfully',
    'update_failed': 'update failed',
    'created': 'created successfully',
    'create_failed': 'creation failed',
    'deleted': 'deleted successfully',
    'delete_failed': 'deletion failed',
    'retrieved': 'retrieved successfully',
    'retrieve_failed': 'retrieval failed',
}

model_messages = dict()

for message_key, message_value in crud_messages.items():
    for model_key, model_val in models.items():
        model_messages[f'{model_key}_{message_key}'] = f'{model_val} {message_value}'.capitalize()


ModelMsgs = Enum('ModelMsgs', model_messages)
