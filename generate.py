from dotenv import load_dotenv

load_dotenv()

import sys
import os
import requests

HAS_LIMITED_INTERNET = False
if os.getenv("HAS_LIMITED_INTERNET", None):
    HAS_LIMITED_INTERNET = True
CF_API_KEY = os.getenv("CF_API_KEY", None)
CF_ZONE_ID = os.getenv("CF_ZONE_ID", None)
CF_DNS_ID = os.getenv("CF_DNS_ID", None)
if len(sys.argv) < 2:
    print("Usage: python3 generate.py <ip on network interface to use>")
    sys.exit(1)

host = sys.argv[1]

with open("base/Caddyfile", "r") as f:
    caddyfile_contents = f.read()
    caddyfile_contents = caddyfile_contents.replace("myip", host)
    if CF_API_KEY:
        caddyfile_contents = caddyfile_contents.replace("$cf_api_key", CF_API_KEY)
    if HAS_LIMITED_INTERNET:
        # uncomment out the blocks between "# BEGIN: HTTPS" and "# END: HTTPS"
        lines = caddyfile_contents.replace("\r\n", "\n").split("\n")
        UNCOMMENTING = False
        for i, line in enumerate(lines):
            if line == "# BEGIN: HTTPS":
                UNCOMMENTING = True
            elif line == "# END: HTTPS":
                UNCOMMENTING = False
            elif UNCOMMENTING:
                lines[i] = line.replace("# ", "") # hack but it works
        caddyfile_contents = "\n".join(lines)
    with open("Caddyfile", "w") as f:
        f.write(caddyfile_contents)
    print("Wrote Caddyfile...")

print("Wrote configs...")    
if HAS_LIMITED_INTERNET and not os.getenv("SKIP_DNS_UPDATE", False):
    # use cloudflare dns to update dns records
    if CF_API_KEY:
        print("Updating DNS records...")
        print("Get existing dns records...")
        response = requests.get(f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records", headers = {
            # "X-Auth-Email": os.getenv("CF_EMAIL", None),
            "Authorization": f"Bearer {CF_API_KEY}",
        })
        result = response.json()
        if result["success"]:
            records = result["result"]
            print("Got existing dns records count:", len(records))
            dns_id = CF_DNS_ID
            for record in records:
                if record["name"] == "intra.smashcloud.org":
                    dns_id = record["id"]
                    print("Found existing dns record with id", dns_id, " ignoring env var...", CF_DNS_ID)
                    break
            response = requests.patch(f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records/{dns_id}", json = {
                "content": host,
                "type": "A",
                "name": "intra.smashcloud.org",
                "proxied": False,
                "comment": "Automatically added by xcontentmanagerd",
                "ttl": 86400 # cache as much as possible in case internet die
            }, headers = {
                "Authorization": f"Bearer {CF_API_KEY}",
            })
            print("Updated DNS records:", response.json())
        else:
            print("Failed to get existing dns records:", result)
    else:
        print("SKIP_DNS_UPDATE is set, but no CF_API_KEY is set. skipping dns update.")


print("Done!")