import requests

import env
from edi_model.enums import ObjectType


def convert_files_with_multipart(files, is_ndjson=False, is_validate=True):
    """Creates a multipart request with the list of files and posts it"""
    api_url = env.api_url + '/edi/json'
    # we need to pass an array of tuples (field_name, file-like obj)
    # The field name is always 'files'
    field_and_file_objects = []
    for f in files:
        field_and_file_objects.append(('files', open(f, 'rb')))
    # If ndjson: True, the server will return a new-line separated list of objects (claims) instead of an array
    # 'validate' tells the converter to validate EDI and serialize validation issues (objectType: VALIDATION)
    params = {'ndjson': is_ndjson, 'validate': is_validate}
    # Use stream=True to stream the response instead of loading it in memory
    api_response = requests.post(api_url, files=field_and_file_objects, params=params, stream=True)
    if api_response.status_code not in {200}:
        raise Exception(f'Error converting EDI; Error: {api_response.text}')

    return api_response


def convert_file(file, is_ndjson=False, is_validate=True):
    """Open a file and post the content in streaming mode"""
    print('Converting ' + file)
    api_url = env.api_url + '/edi/json'
    # Always use splitTran: True for 837/835 transactions
    # If ndjson: True, the server will return a new-line separated list of objects (claims) instead of an array
    # ediFileName parameter will propagate the original file name to transaction.fileInfo.name field; if not provided,
    # the converter will generate a name
    # 'validate' tells the converter to validate EDI and serialize validation issues (objectType: VALIDATION)
    params = {'ndjson': is_ndjson, 'validate': is_validate, 'ediFileName': file}

    with open(file) as f:
        # Use stream=True to stream the response instead of loading it in memory
        # Note that we're posting the file-like object instead of reading the file into memory
        # This allows for streaming content to the server
        api_response = requests.post(api_url, data=f, params=params, stream=True)
        if api_response.status_code not in {200}:
            raise Exception(f'Error converting EDI; Error: {api_response.text}')
    return api_response


def _generate_edi(request, path):
    """Post an EDI generation request object and return the response."""
    api_url = env.api_url + path
    api_response = requests.post(
        api_url,
        json=request.model_dump(by_alias=True, exclude_none=True, mode='json'),
        timeout=30,
    )
    if api_response.status_code not in {200, 417}:
        raise Exception(f'Error generating EDI; Error: {api_response.text}')
    return api_response


def generate_claim_edi(request):
    """Post an EDI generation request object to /edi/gen/837 and return the response."""
    return _generate_edi(request, '/edi/gen/837')


def generate_payment_edi(request):
    """Post an EDI generation request object to /edi/gen/835 and return the response."""
    return _generate_edi(request, '/edi/gen/835')


def handle_warning_error(obj):
    # In case of errors or warnings, objectType is set to ERROR or WARNING
    object_type = ObjectType(obj['objectType'])
    if object_type == ObjectType.ERROR:
        raise Exception(f'Error parsing EDI; Error: {obj}')
    # If we set warningsInResponse=True, we need to check for warnings too
    elif object_type == ObjectType.WARNING:
        file_name = obj['fileName']
        message = obj['message']
        print(f'Encountered parsing issue with file {file_name}. Warning: {message}')
        return True
    elif object_type == ObjectType.VALIDATION:
        print(obj)
        return True
    return None
