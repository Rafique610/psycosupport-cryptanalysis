"""Extract every encrypted JSON value from the loopback capture into ciphertexts.csv.

Reads the pcapng file with the standard library only (tshark is not installed on the lab box),
reassembles each TCP stream on port 5000 per direction, and keeps each ciphertext exactly as it
crossed the wire (JSON escaping such as \\n included).
"""

import csv
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PCAP = ROOT / "evidence/task2/session_all.pcap"
OUT = ROOT / "ciphertexts.csv"
PORT = 5000
ENHANCED_PACKET_BLOCK = 6
LOOPBACK_HEADER = 14  # Linux "lo" frames carry a 14-byte Ethernet-style header


def tcp_streams(path):
    """Yield {'client_to_server': bytes, 'server_to_client': bytes} per TCP stream, in capture order."""
    data, pos, streams = path.read_bytes(), 0, {}
    while pos < len(data):
        block_type, block_len = struct.unpack_from("<II", data, pos)
        if block_type == ENHANCED_PACKET_BLOCK:
            caplen = struct.unpack_from("<I", data, pos + 20)[0]
            ip = data[pos + 28 + LOOPBACK_HEADER : pos + 28 + caplen]
            if ip and ip[0] >> 4 == 4 and ip[9] == 6:  # IPv4 + TCP
                ihl = (ip[0] & 15) * 4
                sport, dport = struct.unpack_from("!HH", ip, ihl)
                payload = ip[ihl + (ip[ihl + 12] >> 4) * 4 : struct.unpack_from("!H", ip, 2)[0]]
                client = sport if dport == PORT else dport
                stream = streams.setdefault(client, {"client_to_server": b"", "server_to_client": b""})
                stream["client_to_server" if dport == PORT else "server_to_client"] += payload
        pos += block_len
    return list(streams.values())


def rows():
    for case_id, stream in enumerate(tcp_streams(PCAP), start=1):
        for direction, raw in stream.items():
            body = json.loads(raw.split(b"\r\n\r\n", 1)[1])
            for field, value in body.items():
                ciphertext = json.dumps(value)[1:-1]  # re-escape exactly as on the wire
                yield {"case_id": case_id, "direction": direction, "field": field,
                       "length": len(ciphertext), "ciphertext": ciphertext}


if __name__ == "__main__":
    out = list(rows())
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["case_id", "direction", "field", "length", "ciphertext"])
        writer.writeheader()
        writer.writerows(out)
    print(f"wrote {len(out)} ciphertexts from {len({r['case_id'] for r in out})} streams to {OUT.relative_to(ROOT)}")
