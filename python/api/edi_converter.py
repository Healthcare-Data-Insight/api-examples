from enum import Enum

import requests

import env


class ObjectType(Enum):
    # 837I/P/D
    CLAIM = "CLAIM"
    # 835 paid claim
    PAYMENT = "PAYMENT"
    # 835 provider-level adjustment
    PROVIDER_ADJUSTMENT = "PROVIDER_ADJUSTMENT"
    # 834
    MEMBER_COVERAGE = "MEMBER_COVERAGE"
    # parser's errors or warnings
    ERROR = "ERROR"
    WARNING = "WARNING"


def convert_files_with_multipart(files, is_ndjson):
    """Creates a multipart request with the list of files and posts it"""
    api_url = env.api_url + '/edi/json'
    # we need to pass an array of tuples (field_name, file-like obj)
    # The field name is always 'files'
    field_and_file_objects = []
    for f in files:
        field_and_file_objects.append(('files', open(f, 'rb')))
    # Always use splitTran: True for 837/835 transactions
    # If ndjson: True, the server will return a new-line separated list of objects (claims) instead of an array
    params = {'ndjson': is_ndjson}
    # Use stream=True to stream the response instead of loading it in memory
    api_response = requests.post(api_url, files=field_and_file_objects, params=params, stream=True)
    api_response.raise_for_status()

    return api_response


def convert_file(file, is_ndjson):
    """Open a file and post the content in streaming mode"""
    print('Converting ' + file)
    api_url = env.api_url + '/edi/json'
    # Always use splitTran: True for 837/835 transactions
    # If ndjson: True, the server will return a new-line separated list of objects (claims) instead of an array
    # ediFileName parameter will propagate the original file name to transaction.fileInfo.name field; if not provided,
    # the converter will generate a name
    # warningsInResponse tells the converter to return parsing warnings to the client as objects (objectType: WARNING)
    params = {'ndjson': is_ndjson, 'warningsInResponse': True, 'ediFileName': file}

    with open(file) as f:
        # Use stream=True to stream the response instead of loading it in memory
        # Note that we're posting the file-like object instead of reading the file into memory
        # This allows for streaming content to the server
        api_response = requests.post(api_url, data=f, params=params, stream=True)
        api_response.raise_for_status()
    return api_response


def generate_claim_edi(request):
    """Post an EDI generation request object to /edi/gen/claim and return the response."""
    api_url = env.api_url + '/edi/gen/claim'
    api_response = requests.post(
        api_url,
        json=request.model_dump(by_alias=True, exclude_none=True, mode='json'),
        timeout=30,
    )
    if api_response.status_code not in {200, 417}:
        api_response.raise_for_status()
    return api_response


def handle_warning_error(obj):
    # In case of errors or warnings, objectType is set to ERROR or WARNING
    object_type = ObjectType(obj['objectType'])
    if object_type == ObjectType.ERROR:
        raise Exception(f'Error parsing EDI; Error: {obj}')
    # since we set warningsInResponse=True, we need to check for warnings too
    elif object_type == ObjectType.WARNING:
        file_name = obj['fileName']
        message = obj['message']
        print(f'Encountered parsing issue with file {file_name}. Warning: {message}')
        return True
    return None