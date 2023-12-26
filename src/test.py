import yaml

def replaceMatchName(gameName : str, path : str):
    try:
        # Read YAML file
        with open(path, 'r') as file:
            data = yaml.safe_load(file)

        # Update the field with the new value
        data['match'] = gameName

        # Write back to the YAML file
        with open(path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    except Exception as e:
        print(f"Error: {e}")

replaceMatchName("prout", "./config.yml")