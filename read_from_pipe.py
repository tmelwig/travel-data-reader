import os
import json

PIPE_PATH = "/tmp/reco_pipe"


def reco_from_pipe():
    """
    Reads JSON objects from the named pipe (FIFO) and processes them one by one.
    """
    print("Waiting for data from EC2...")

    # Open the pipe in read mode
    with open(PIPE_PATH, "r") as pipe:
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


if __name__ == "__main__":
    reco_from_pipe()
