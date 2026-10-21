"""PsycoSupport server: receives affine-encrypted concerns on 127.0.0.1:5000 and answers via a local Ollama model."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import ollama

from affine import decrypt, encrypt

HOST, PORT = "127.0.0.1", 5000
MODEL = "llama3.2"
SYSTEM_PROMPT = (
    "You are PsycoSupport, a supportive assistant for a psychologist's patients. "
    "Reply in plain English prose in under 120 words, with calm, practical coping suggestions. "
    "Do not diagnose or prescribe medication. "
    "Always end with exactly this sentence: "
    "This is not a substitute for professional help. If you are in crisis, please contact your local emergency services."
)


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/submit":
            self.send_error(404)
            return
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        username, mood, concern = (decrypt(body[k]) for k in ("username", "mood", "concern"))
        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Patient {username} feels {mood}. Concern: {concern}"},
            ],
        )
        payload = json.dumps({"reply": encrypt(response["message"]["content"])}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    print(f"PsycoSupport server on http://{HOST}:{PORT} (model {MODEL})", flush=True)
    HTTPServer((HOST, PORT), Handler).serve_forever()
