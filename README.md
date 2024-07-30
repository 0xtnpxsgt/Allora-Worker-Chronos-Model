# Allora-2 Worker-Chronos-Model


 
- You must need to buy a VPS for running Allora Worker
- You can buy from : Contabo
- You should buy VPS which is fulfilling all these requirements : 
```bash
Operating System : Ubuntu 22.04
CPU: Minimum of 1/2 core.
Memory: 2 to 4 GB.
Storage: SSD or NVMe with at least 5GB of space.
```

### Deployment - Read Carefully! 
## Step 1: 
```bash
rm -rf allora-model.sh allora-chain/ basic-coin-prediction-node/
```

## Step 2: 
```bash
apt install wget
```

## Step 3: Install Allora ( This will take time )
```bash
wget https://raw.githubusercontent.com/0xtnpxsgt/Allora-Worker-Chronos-Model/main/allora-model.sh && chmod +x allora-model.sh && ./allora-model.sh
```
- In the middle of the command execution, it will ask for keyring phrase, Here you need write a password (example : 12345678)
- During pasting `HEAD_ID` , Don't use `Ctrl+C` to copy and `Ctrl+V` to paste, instead just select the whole `KEY_ID` and Press Right Click

- Once Done Proceed to Step 4

## Step 4: Edit App.py
- Export Head-ID
```bash
cd allora-chain/basic-coin-prediction-node/
```

```bash
cat head-data/keys/identity
```

## Step 5: Edit App.py
- Register on Coingecko https://www.coingecko.com/en/developers/dashboard & Create Demo API KEY
- Copy & Replace API with your `COINGECKO API` , then save `Ctrl+X Y ENTER`.
```bash
sudo rm -rf app.py && sudo nano app.py
```
```bash
from flask import Flask, Response
import requests
import json
import pandas as pd
import torch
from chronos import ChronosPipeline
 
# create our Flask app
app = Flask(__name__)
 
# define the Hugging Face model we will use
model_name = "amazon/chronos-t5-tiny"
 
# define our endpoint
@app.route("/inference/<string:token>")
def get_inference(token):
    """Generate inference for given token."""
    try:
        # use a pipeline as a high-level helper
        pipeline = ChronosPipeline.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )
    except Exception as e:
        return Response(json.dumps({"pipeline error": str(e)}), status=500, mimetype='application/json')
 
    # get the data from Coingecko
    url = "https://api.coingecko.com/api/v3/coins/"
    if token.upper() == 'ETH':
        url += "ethereum"
    if token.upper() == 'SOL':
        url += "solana"
    if token.upper() == 'BTC':
        url += "bitcoin"
    if token.upper() == 'BNB':
        url += "binancecoin"
    if token.upper() == 'ARB':
        url += "arbitrum"       
    url += "/market_chart?vs_currency=usd&days=30&interval=daily"
    
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-XXXXXXXXXXXXXXXXXXXX" # replace with your API key
    }
 
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["prices"])
        df.columns = ["date", "price"]
        df["date"] = pd.to_datetime(df["date"], unit = "ms")
        df = df[:-1] # removing today's price
        print(df.tail(5))
    else:
        return Response(json.dumps({"Failed to retrieve data from the API": str(response.text)}), 
                        status=response.status_code, 
                        mimetype='application/json')
 
    # define the context and the prediction length
    context = torch.tensor(df["price"])
    prediction_length = 1
 
    try:
        forecast = pipeline.predict(context, prediction_length)  # shape [num_series, num_samples, prediction_length]
        print(forecast[0].mean().item()) # taking the mean of the forecasted prediction
        return Response(str(forecast[0].mean().item()), status=200)
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')
 
# run our Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
```

## Step 6: Create main.py file
- Copy & Paste this code: , then save `Ctrl+X Y ENTER`.
```bash
sudo rm -rf main.py && sudo nano main.py
```
```bash
import requests
import sys
import json
 
def process(argument):
    headers = {'Content-Type': 'application/json'}
    url = f"http://inference:8000/inference/{argument}"
    response = requests.get(url, headers=headers)
    return response.text
 
if __name__ == "__main__":
    # Your code logic with the parsed argument goes here
    try:
        if len(sys.argv) < 5:
            value = json.dumps({"error": f"Not enough arguments provided: {len(sys.argv)}, expected 4 arguments: topic_id, blockHeight, blockHeightEval, default_arg"})
        else:
            topic_id = sys.argv[1]
            blockHeight = sys.argv[2]
            blockHeightEval = sys.argv[3]
            default_arg = sys.argv[4]

            response_inference = process(argument=default_arg)
            response_dict = {"infererValue": response_inference}
            value = json.dumps(response_dict)
    except Exception as e:
        value = json.dumps({"error": {str(e)}})
    print(value)
```
## Step 7: Create requirments.txt
- Copy & Paste this code: , then save `Ctrl+X Y ENTER`.
```bash
sudo rm -rf requirements.txt && sudo nano requirements.txt
```
```bash
flask[async]
gunicorn[gthread]
numpy==1.26.2
pandas
Requests==2.32.0
transformers[torch]
scikit_learn==1.3.2
werkzeug>=3.0.3 # not directly required, pinned by Snyk to avoid a vulnerability
git+https://github.com/amazon-science/chronos-forecasting.git
python-dotenv
```

## Step 8: Create Dockerfile
- Copy & Paste this code , `Ctrl+X Y ENTER` to save.

```bash
sudo rm -rf Dockerfile && sudo nano Dockerfile
```
```bash
# Use an official Python runtime AS the base image
FROM amd64/python:3.9-buster as project_env

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools \
    && pip install -r requirements.txt

FROM project_env

COPY . /app/

# Set the entrypoint command
CMD ["gunicorn", "--conf", "/app/gunicorn_conf.py", "main:app"]

```

## Step 9: Edit docker-compose.yml
- Copy & Replace `HEAD-ID`  `WALLETSEEDPHRASE` Worker1 - Worker2
```bash
rm -rf docker-compose.yml && nano docker-compose.yml
```
```bash
version: '3'

services:
  inference:
    container_name: inference
    build:
      context: .
    command: python -u /app/app.py
    ports:
      - "8000:8000"
    networks:
      eth-model-local:
        aliases:
          - inference
        ipv4_address: 172.22.0.4
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/inference/ETH"]
      interval: 10s
      timeout: 10s
      retries: 12
    volumes:
      - ./inference-data:/app/data
  
  updater:
    container_name: updater
    build: .
    environment:
      - INFERENCE_API_ADDRESS=http://inference:8000
    command: >
      sh -c "
      while true; do
        python -u /app/update_app.py;
        sleep 24h;
      done
      "
    depends_on:
      inference:
        condition: service_healthy
    networks:
      eth-model-local:
        aliases:
          - updater
        ipv4_address: 172.22.0.5
  
  head:
    container_name: head
    image: alloranetwork/allora-inference-base-head:latest
    environment:
      - HOME=/data
    entrypoint:
      - "/bin/bash"
      - "-c"
      - |
        if [ ! -f /data/keys/priv.bin ]; then
          echo "Generating new private keys..."
          mkdir -p /data/keys
          cd /data/keys
          allora-keys
        fi
        allora-node --role=head --peer-db=/data/peerdb --function-db=/data/function-db  \
          --runtime-path=/app/runtime --runtime-cli=bls-runtime --workspace=/data/workspace \
          --private-key=/data/keys/priv.bin --log-level=debug --port=9010 --rest-api=:6000 \
          --boot-nodes=/dns/head-0-p2p.testnet-1.testnet.allora.network/tcp/32130/p2p/12D3KooWLBhsSucVVcyVCaM9pvK8E7tWBM9L19s7XQHqqejyqgEC,/dns/head-1-p2p.testnet-1.testnet.allora.network/tcp/32131/p2p/12D3KooWEUNWg7YHeeCtH88ju63RBfY5hbdv9hpv84ffEZpbJszt,/dns/head-2-p2p.testnet-1.testnet.allora.network/tcp/32132/p2p/12D3KooWATfUSo95wtZseHbogpckuFeSvpL4yks6XtvrjVHcCCXk
    ports:
      - "6000:6000"
    volumes:
      - ./head-data:/data
    working_dir: /data
    networks:
      eth-model-local:
        aliases:
          - head
        ipv4_address: 172.22.0.100

  worker-1:
    container_name: worker-1
    environment:
      - INFERENCE_API_ADDRESS=http://inference:8000
      - HOME=/data
    build:
      context: .
      dockerfile: Dockerfile_b7s
    entrypoint:
      - "/bin/bash"
      - "-c"
      - |
        if [ ! -f /data/keys/priv.bin ]; then
          echo "Generating new private keys..."
          mkdir -p /data/keys
          cd /data/keys
          allora-keys
        fi
        # Change boot-nodes below to the key advertised by your head
        allora-node --role=worker --peer-db=/data/peerdb --function-db=/data/function-db \
          --runtime-path=/app/runtime --runtime-cli=bls-runtime --workspace=/data/workspace \
          --private-key=/data/keys/priv.bin --log-level=debug --port=9011 \
          --boot-nodes=/ip4/172.22.0.100/tcp/9010/p2p/HEAD-ID \
          --topic=allora-topic-1-worker --allora-chain-worker-mode=worker \
          --allora-chain-restore-mnemonic='WALLETSEEDPHRASE' \
          --allora-node-rpc-address=https://allora-rpc.testnet-1.testnet.allora.network \
          --allora-chain-key-name=worker-1 \
          --allora-chain-topic-id=1
    volumes:
      - ./workers/worker-1:/data
    working_dir: /data
    depends_on:
      - inference
      - head
    networks:
      eth-model-local:
        aliases:
          - worker1
        ipv4_address: 172.22.0.12

  worker-2:
    container_name: worker-2
    environment:
      - INFERENCE_API_ADDRESS=http://inference:8000
      - HOME=/data
    build:
      context: .
      dockerfile: Dockerfile_b7s
    entrypoint:
      - "/bin/bash"
      - "-c"
      - |
        if [ ! -f /data/keys/priv.bin ]; then
          echo "Generating new private keys..."
          mkdir -p /data/keys
          cd /data/keys
          allora-keys
        fi
        # Change boot-nodes below to the key advertised by your head
        allora-node --role=worker --peer-db=/data/peerdb --function-db=/data/function-db \
          --runtime-path=/app/runtime --runtime-cli=bls-runtime --workspace=/data/workspace \
          --private-key=/data/keys/priv.bin --log-level=debug --port=9013 \
          --boot-nodes=/ip4/172.22.0.100/tcp/9010/p2p/HEAD-ID \
          --topic=allora-topic-2-worker --allora-chain-worker-mode=worker \
          --allora-chain-restore-mnemonic='WALLETSEEDPHRASE' \
          --allora-node-rpc-address=https://allora-rpc.testnet-1.testnet.allora.network \
          --allora-chain-key-name=worker-2 \
          --allora-chain-topic-id=2
    volumes:
      - ./workers/worker-2:/data
    working_dir: /data
    depends_on:
      - inference
      - head
    networks:
      eth-model-local:
        aliases:
          - worker1
        ipv4_address: 172.22.0.13
  
networks:
  eth-model-local:
    driver: bridge
    ipam:
      config:
        - subnet: 172.22.0.0/24

volumes:
  inference-data:
  workers:
  head-data:
```


## Step 10: Build.
```bash
docker compose build && docker compose up -d
```
------------------------------------------------------------------------------

#### Check Docker Status
```bash
docker ps
```
# Result:
<img width="1370" alt="Screenshot 1403-05-05 at 6 55 33 PM" src="https://github.com/user-attachments/assets/b58b264b-b4d7-4bb2-8ca2-2908b5d6e70c">


#### Check your node status
```bash
# Check worker 2 logs
docker compose logs -f worker-2

# Check worker 1 logs
docker compose logs -f worker-1

# Check worker infernence - result 200 means- success.
docker compose logs -f inference
```
#### Check your worker logs and test the inferences using curl

```bash
# Download Checker
wget -O checkyourworker.sh https://raw.githubusercontent.com/casual1st/alloraworkersetup/main/checkyourworker.sh
chmod +x checkyourworker.sh
./checkyourworker.sh
```

#### Run Checker
```bash
./checkyourworker.sh
```

#### HAVING PROBLEM WITH THE SETUP? JOIN US HERE: https://discord.gg/r6PPSjRZec | help is on the way! :D





