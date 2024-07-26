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
rm -rf allora.sh allora-chain/ basic-coin-prediction-node/
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

## Step 4: Edit App.py
- Export New Head-ID
```bash
cat head-data/keys/identity
```

## Step 5: Edit App.py
- Register on Coingecko & Create Demo API KEY
- Replace API with your `COINGECKO API` , then save `Ctrl+X Y ENTER`.
```bash
nano allora-chain/basic-coin-prediction-node/app.py
```

## Step 6: Edit docker-compose.yml
- Replace `HEAD-ID`  `WALLETSEEDPHRASE` 
```bash
nano allora-chain/basic-coin-prediction-node/docker-compose.yml
```
## Step 7: Build.
- 1 
```bash
cd allora-chain/basic-coin-prediction-node/
```
- 2
```bash
docker compose up -d --build
```
------------------------------------------------------------------------------

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
wget -O checkyourworker.sh https://raw.githubusercontent.com/casual1st/alloraworkersetup/main/checkyourworker.sh && chmod +x checkyourworker.sh && ./checkyourworker.sh
```

#### Run Checker
```bash
./checkyourworker.sh
```

### HAVING PROBLEM WITH THE SETUP? JOIN US HERE: https://discord.gg/QTAqpuRDhP





