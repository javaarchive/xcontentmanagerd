from dotenv import load_dotenv

load_dotenv()

import sys
import os
import requests

HAS_LIMITED_INTERNET = False
CF_API_KEY = os.getenv("CF_API_KEY", None)
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
        requests.post()
    else:
        print("SKIP_DNS_UPDATE is set, but no CF_API_KEY is set. skipping dns update.")


print("Done!")