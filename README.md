# xcontentmanagerd
low power content server details for long trips with limited internet, it's like those airplane menus but cooler, runs on any computer capable of running a hotspot
![IMG_9501](https://github.com/user-attachments/assets/dc82d248-8eea-4349-ba1a-c0016b164b98)


## details
cheap laptop runs windows 10, runs some wifi hotspot software. it has scoop installed and git bash so we have these cursed shell scripts on windows. you will also need a working python install with pip.

## services
### caddy
runs on port 80, should optionally try to get ssl for domain pointing to local ip but this may not be doable under poor connectivity. custom build that has cloudflare module enabled, nothing special. wget it from releases. 

### content manager (jellyfin)
your average jellyfin server, runs on port 8096. proxied by caddy cause why not and i like the look of https sometimes.

### python3 http.server???
to host downloads when friends are using it.

## running scripts through git bash
`bash <filename>`
