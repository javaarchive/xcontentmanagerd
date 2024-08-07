echo Installing dependencies
scoop install wget sudo
# install custom build of caddy
echo Downloading caddy
wget https://github.com/javaarchive/xcontentmanagerd/releases/download/assets/caddy_windows_amd64_custom.exe -O caddy.exe
echo Installing requirements for setup script
python -m pip install -r requirements.txt
python -m pip install -r dnschef/requirements.txt
cp dnschef/dnschef.py dnschef.py