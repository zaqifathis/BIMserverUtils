
import  json

def map_type(java_type):
    mapping = {
        "LONG": "integer",
        "STRING": "string",
        "BOOLEAN": "boolean",
        "INT": "integer",
        "DOUBLE": "number",
        "FLOAT": "number",
        "LIST": "array",
        "SET": "array",
        "DATE": "object",
        "UNKNOWN": "object",
    }
    return mapping.get(java_type, "string")

def type_schema(item_type):
    schema = {"type": map_type(item_type)}
    if item_type in {"INT", "LONG"}:
        schema["format"] = "int32" if item_type == "INT" else "int64"
    return schema

def handle_complex_type(field):
    return {
        "type": map_type(field["type"]["simpleType"]),
        "properties": process_fields(field["type"].get("fields", []))
    }

def process_fields(fields):
    properties = {}
    for field in fields:
        field_type = field["type"]["simpleName"].upper()

        if field_type in {"SET", "LIST"}:
            generic_type = field["genericType"]["simpleType"]
            schema = {
                "type": map_type(field_type),
                "items": type_schema(generic_type)
            }
        elif field_type in {"UNKNOWN", "DATE"}:
            schema = handle_complex_type(field)
        else:
            schema = type_schema(field_type)

        properties[field["name"]] = schema
    return properties

def create_parameter_schema(param):
    param_type = param["type"]["simpleType"]

    if param_type in {"SET", "LIST"}:
        generic_type = param["genericType"]["simpleType"]
        schema = {
            "type": map_type(param_type),
            "items": type_schema(generic_type)
        }
    elif param_type in {"UNKNOWN", "DATE"}:
        schema = handle_complex_type(param)
    else:
        schema = type_schema(param_type)

    return {
        "name": param["name"],
        "in": "query",
        "required": True,
        "description": param.get("doc", ""),
        "schema": schema,
    }

def generate_openapi_schema(input_data):
    paths = []

    for service in input_data["services"]:
        service_name = service["simpleName"]
        for method in service["methods"]:
            path_key = f"/{service_name}/{method["name"]}"
            http_method = "post"
            parameters = [create_parameter_schema(param) for param in method.get("parameters", [])]

            # add service/method to the paths
            paths.append({
                path_key: {
                    http_method: {
                        "description": method["doc"],
                        "responses": {
                            "200": {
                                "description": method["returnDoc"],
                                "content": {}
                            }
                        },
                        "parameters": parameters
                    }
                }
            })

    return {"paths": paths}

def load_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def save_json_file(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

def main():
    file_path = "./services.json"
    input_data = load_json_file(file_path)
    openapi_schema = generate_openapi_schema(input_data)
    save_json_file(openapi_schema, "formatted_openapi.json")
    print("Conversion done!")


if __name__ == "__main__":
    main()