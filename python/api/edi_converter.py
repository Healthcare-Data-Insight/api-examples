import env
from edi_model.enums import ObjectType
from ediconvert_sdk import EdiConverterClient

_client = EdiConverterClient(base_url=env.api_url)


def convert_files_with_multipart(files, is_ndjson=False, is_validate=True):
    """Creates a multipart request with the list of files and posts it"""
    # If ndjson: True, the server will return a new-line separated list of objects (claims) instead of an array
    # 'validate' tells the converter to validate EDI and serialize validation issues (objectType: VALIDATION)
    return _client.conversion.to_json_files(files, ndjson=is_ndjson, validate=is_validate)


def convert_file(file, is_ndjson=False, is_validate=True):
    """Open a file and post the content in streaming mode"""
    print('Converting ' + file)
    # Always use splitTran: True for 837/835 transactions
    # If ndjson: True, the server will return a new-line separated list of objects (claims) instead of an array
    # ediFileName parameter will propagate the original file name to transaction.fileInfo.name field; if not provided,
    # the converter will generate a name
    # 'validate' tells the converter to validate EDI and serialize validation issues (objectType: VALIDATION)
    return _client.conversion.to_json_file(file, ndjson=is_ndjson, validate=is_validate)


def _generate_edi(request, path):
    """Post an EDI generation request object and return the response."""
    if path == '/edi/gen/837':
        return _client.generation.generate_837_response(request)
    if path == '/edi/gen/835':
        return _client.generation.generate_835_response(request)
    raise ValueError(f'Unsupported EDI generation path: {path}')


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