sudo apt upgrade
sudo apt update
sudo apt install curl
sudo apt install python3.10-venv
cd backend
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
playwright install 
playwright install-deps                     

playwright install firefox

sudo apt remove nodejs -y
sudo apt purge nodejs -y
sudo apt autoremove -y

sudo rm -rf /usr/lib/node_modules
sudo rm -rf ~/.npm
sudo rm -rf ~/.node-gyp


curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install node
sudo rm -rf /usr/local/bin/node
sudo rm -rf /usr/local/bin/npm
sudo rm -rf /usr/local/lib/node_modules
sudo apt-get install zstd
curl -fsSL https://ollama.com/install.sh | sh


#ollama pull qwen3.5:35b