import os
import time

# Define the pipe path
PIPE_PATH = "/tmp/reco_pipe"

# Ensure the pipe exists
if not os.path.exists(PIPE_PATH):
    os.mkfifo(PIPE_PATH)

while True:
    with open(PIPE_PATH, "r") as pipe:
        data = pipe.read()
        if data:
            print("Received data:", data)
        time.sleep(1)
