import json
from string import Template
from services.get_calls_service import (create_get_paths_subbing_in_test_data_for_vars, get_test_get_calls_template,
                                        create_template_data_based_on_values_passed, write_to_template_file)


def get_swagger_doc():
    #file_path = input("Enter the path to your swagger doc: ")
    file_path = "petstore.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    except LookupError as ex:
        print("Could not load json file, please try again")


def get_test_data():
    #file_path = input("Enter the path to your test data: ")
    file_path = "petstore.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    except LookupError as ex:
        print("Could not load json file, please try again")


def parse_dict(swagger_dictionary_data):
    get_calls = {}
    post_calls = {}
    put_calls = {}
    delete_calls = {}

    for path, path_data in swagger_dictionary_data["paths"].items():
        if 'get' in path_data:
            get_calls[path] = path_data
        if 'post' in path_data:
            post_calls[path] = path_data
        if 'put' in path_data:
            put_calls[path] = path_data
        if 'delete' in path_data:
            delete_calls[path] = path_data

    return {
        'get': get_calls,
        'post': post_calls,
        'put': put_calls,
        'delete': delete_calls
    }





if __name__ == '__main__':
    swagger_dict = get_swagger_doc()
    data = parse_dict(swagger_dict)
    paths = create_get_paths_subbing_in_test_data_for_vars(data['get'], {"petId": "1", "orderId": "1", "username": "testUser"})

    template_obj = get_test_get_calls_template()
    temp_data = create_template_data_based_on_values_passed("petstore.swagger.io/v2", paths)
    write_to_template_file(template_obj, temp_data)

