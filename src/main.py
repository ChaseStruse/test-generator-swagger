import json
from string import Template

template = """import requests


def test_${test_case_name}_returns_200_given_valid_data():
    url = f"${base_url}/${path}"
    expected = 200
    actual = requests.get(url)
    assert actual.status_code == expected

"""


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


def create_get_paths_subbing_in_test_data_for_vars(get_calls, test_data):
    paths = []
    for path in get_calls.keys():
        finished_path = ""
        split_path = path.split("/")
        split_path.pop(0)
        for part_path in split_path:
            if '{' in part_path:
                part_path = test_data[part_path[1:-1]]
                finished_path += str(part_path) + "/"
            else:
                finished_path += str(part_path) + "/"

        paths.append(finished_path)

    return paths


if __name__ == '__main__':
    swagger_dict = get_swagger_doc()
    data = parse_dict(swagger_dict)
    paths = create_get_paths_subbing_in_test_data_for_vars(data['get'], {"petId": "1", "orderId": "1", "username": "testUser"})
    temp_data = {
        "test_case_name": "please_work",
        "base_url": "petstore.swagger.io/v2",
        "path": paths[1]
    }
    template_obj = Template(template)
    generated = template_obj.substitute(temp_data)
    with open("test.py", "w") as f:
        f.write(generated)

