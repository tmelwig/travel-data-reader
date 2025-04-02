# Fake Stream Generator → Decorator Pipeline

**A system for generating fake recommendation data and processing it in real-time.**

---

## 📌 Overview

This setup allows you to:

1. **Post data** to a FIFO pipe on the **Fake Stream Generator (EC2)**.
2. **Retrieve and process data** on the **Decorator (EC2)**.

---

## 🚀 Quick Start

### 1. **Post Data to FIFO (Fake Stream Generator)**

Run the Python script to generate and stream data:

```bash
./recoReader.py -f pretty_json your_csv.csv.gz

```

---

### 2. **Retrieve Data from FIFO (Decorator EC2)**

### 🔑 **Step 1: SSH Setup**

- **Generate an SSH key** (if you don’t have one):
    
    ```bash
    ssh-keygen -t rsa -b 4096 -C "your_email@gmail.com"
    
    ```
    
- **Add your key** to the Fake Stream Generator’s `authorized_keys` (ask **Thomas** or **Valentin**).

### ⚡ **Step 2: Passwordless Authentication**

Avoid entering passwords repeatedly:

```bash
eval "$(ssh-agent -s)"  # Start SSH agent
ssh-add ~/.ssh/your_private_key  # Add your key

```

**Test connection**:

```bash
ssh -i ~/.ssh/your_private_key ec2-user@<FAKE_STREAM_EC2_IP> echo "Connected"

```

### 📂 **Step 3: Project Setup**

Create directories:

```bash
mkdir jsons scripts

```

### 📜 **Step 4: Pipe Connector Script**

Save this as `scripts/pipe_connector.sh`:

```bash
#!/bin/bash

mkdir -p jsons

ssh -i ~/.ssh/ec2-tmelwig-rsa -t ec2-user@51.21.161.233 'cat /tmp/reco_pipe' | \\
while read -r json; do
    search_id=$(echo "$json" | jq -r '.search_id')
    echo "$json" > "jsons/${search_id}.json"

    # ⚠️ Replace with your processing command:
    # python decorator_algorithm.py "jsons/${search_id}.json"

    if [ $? -ne 0 ]; then
        echo "Error processing $search_id" >&2
        break
    fi
done

```

**Make it executable**:

```bash
chmod +x scripts/pipe_connector.sh

```

### ▶️ **Step 5: Run the Connector**

```bash
scripts/pipe_connector.sh

```

---

## 🛠️ Troubleshooting

- **"Permission denied (publickey)"**:
    - Ensure `~/.ssh/authorized_keys` on the **Fake Stream Generator** contains your public key.
    - Fix permissions:
        
        ```bash
        chmod 600 ~/.ssh/authorized_keys
        
        ```
        
- **SSH still asks for a password**:
    - Verify the key is loaded:
        
        ```bash
        ssh-add -L
        
        ```
        

---

## 📂 Directory Structure

```
.
├── jsons/           # Processed JSON files
├── scripts/
│   └── pipe_connector.sh  # FIFO retrieval script
└── decorator_algorithm.py # Decorator algo

```
