import json

class JsonHelper:

    @staticmethod
    def write(data, file: str):

        if not file.endswith(".json"):
            print("File should be of JSON format")
            return

        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    
    @staticmethod
    def read(file: str):
        
        if not file.endswith(".json"):
            print("File should be of JSON format")
            return
    
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
 