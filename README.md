# Allora-Worker-Chronos-Model


 
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
#### Step 1: 
```bash
rm -rf allora.sh allora-chain/ basic-coin-prediction-node/
```

#### Step 2: 
```bash
apt install wget
```

#### Step 3: Install Allora ( This will take time )
```bash
wget https://raw.githubusercontent.com/0xtnpxsgt/alloranode/main/allora-oneclickguide.sh && chmod +x allora-oneclickguide.sh && ./allora-oneclickguide.sh
```
- In the middle of the command execution, it will ask for keyring phrase, Here you need write a password (example : 12345678)
- During pasting `HEAD_ID` , Don't use `Ctrl+C` to copy and `Ctrl+V` to paste, instead just select the whole `KEY_ID` and Press Right Click

