from string import Template


def get_test_get_calls_template():
    template = """
def test_${test_case_name}_path_returns_200_given_valid_data():
    url = f"${base_url}/${path}"
    expected = 200
    actual = requests.get(url)
    assert actual.status_code == expected

"""
    return Template(template)


def create_template_data_based_on_values_passed(base_url, paths):
    template_data = {}
    for path in paths:
        template_data[path] = {
            "test_case_name": path.replace("/", "_"),
            "base_url": base_url,
            "path": path
        }
    return template_data


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


def write_to_template_file(template, template_data):
    print(template_data)
    with open("test.py", "w") as f:
        f.write("import requests")
        for data in template_data.values():
            print(data)
            generated = template.substitute(data)
            f.write(generated)
