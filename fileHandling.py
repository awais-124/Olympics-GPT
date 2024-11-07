import json

def add_key_value_to_file(file_path, key, value):
    data = get_file_data(file_path)
    if data == -1: return
    data[key] = value

    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print("-" * 50)
        print(f"Error writing to file: {str(e)}")
        print("-" * 50)

def get_file_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("-" * 50)
        print(f"Error: File not found at '{file_path}'.")
        print("-" * 50)
        return -1
    except json.JSONDecodeError:
        print("-" * 50)
        print(f"Error: Invalid JSON format in file at '{file_path}'.")
        print("-" * 50)
        return -1
    except Exception as e:
        print("-" * 50)
        print(f"Error: {str(e)}")
        print("-" * 50)
        return -1