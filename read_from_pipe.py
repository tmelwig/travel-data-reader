import os
import json

pipe_path = "/tmp/reco_pipe"

# Ensure the pipe exists before reading
if not os.path.exists(pipe_path):
    raise FileNotFoundError(f"Pipe {pipe_path} not found.")

# Open the pipe in read mode
with open(pipe_path, "r") as pipe:
    while True:
        line = pipe.readline()  # Read each line (which is a JSON object)
        if line:
            try:
                # Deserialize the JSON data
                search = json.loads(line)

                # Process the JSON (e.g., save it to a file based on search_id)
                output_path = f"./json/{search['search_id']}.json"
                os.makedirs("./json", exist_ok=True)  # Ensure directory exists
                with open(output_path, "w") as json_file:
                    json.dump(search, json_file, indent=2)

                print(f"Processed search_id: {search['search_id']}")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        else:
            break
