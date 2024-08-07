echo Installing dependencies
scoop install wget sudo
# install custom build of caddy
echo Downloading caddy
wget https://github.com/javaarchive/xcontentmanagerd/releases/download/assets/caddy_windows_amd64_custom.exe -O caddy.exe
