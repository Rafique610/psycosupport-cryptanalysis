"""PsycoSupport terminal client: encrypts username, mood and concern, sends them to the server, prints the reply."""

import requests

from affine import decrypt, encrypt

SERVER_HOST = "muhammadrafique"  # "host file" name from the brief; maps to 127.0.0.1 in /etc/hosts
URL = f"http://{SERVER_HOST}:5000/submit"

if __name__ == "__main__":
    fields = {k: input(f"{k.capitalize()}: ") for k in ("username", "mood", "concern")}
    r = requests.post(URL, json={k: encrypt(v) for k, v in fields.items()}, timeout=300)
    r.raise_for_status()
    print("\nPsychologist:\n" + decrypt(r.json()["reply"]))
