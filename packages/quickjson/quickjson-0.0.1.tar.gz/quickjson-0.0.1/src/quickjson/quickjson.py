import json, os

class QuickJson:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        try:
            open(self.json_file_path, 'r')
        except FileNotFoundError:
            self.create_json_file()

    def read_json_file(self):
        with open(self.json_file_path, 'r') as json_file:
            data = json.load(json_file)
        return data

    def write_json_file(self, data):
        with open(self.json_file_path, 'w') as json_file_writer:
            json.dump(data, json_file_writer)

    def write_list_json_file(self, list_dict, data_to_write):
        with open(self.json_file_path, 'r') as json_file_reader:
            contents_unloaded = json.load(json_file_reader)
        required_list = contents_unloaded[list_dict]
        required_list.append(data_to_write)
        with open(self.json_file_path, 'w') as json_file_writer:
            json.dump(contents_unloaded, json_file_writer)

    def delete_json_file(self):
        os.remove(self.json_file_path)

    def clear_json_file(self):
        clear_value = {}
        self.write_json_file(clear_value)

    def remove_element_from_list(self, list_dict, element):
        with open(self.json_file_path, 'r') as json_file_reader:
            contents_unloaded = json.load(json_file_reader)
        required_list = contents_unloaded[list_dict]
        required_list.remove(element)
        with open(self.json_file_path, 'w') as json_file_writer:
            json.dump(contents_unloaded, json_file_writer)

    def clear_list_json_file(self, list_dict):
        with open(self.json_file_path, 'r') as json_file_reader:
            contents_unloaded = json.load(json_file_reader)
        required_list = contents_unloaded[list_dict]
        for content in reversed(required_list):
            required_list.remove(content)
        with open(self.json_file_path, 'w') as json_file_writer:
            json.dump(contents_unloaded, json_file_writer)

    def create_json_file(self):
        file = open(self.json_file_path, 'w')
        file.close()