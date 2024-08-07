# xcontentmanagerd
low power content server details for long trips with limited internet, it's like those airplane menus but cooler

## details
cheap laptop runs windows 10, runs some wifi hotspot software. it has scoop installed and git sh so we have these cursed shell scripts on windowss.

## services
### caddy
runs on port 80, should optionally try to get ssl for domain pointing to local ip but this may not be doable under poor connectivity. custom build that has cloudflare module enabled, nothing special. wget it from releases. 

### content manager (jellyfin)
your average jellyfin server, runs on port 8096. proxied by caddy cause why not and i like the look of https sometimes.

### python3 http.server???
to host downloads when friends are using it.
