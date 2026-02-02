"""File where integration contacts with API."""

import base64
import hashlib
import json
import socket
import time


class WhatsMinerAPI:  # One class - One device
    """Main class in API."""

    def __init__(self, host, port, account="super", password="admin") -> None:
        "Init function for API."
        self._host = host
        self._port = port
        self._account = account
        self._password = password
        self._type: str | None = None

        try:
            self._type = self._fetch_device_type()
        except (OSError, KeyError, ValueError):
            self._type = "WhatsMiner"

    def get_device_type(self) -> str | None:
        """Return cached miner type."""
        return self._type

    def get_status(self) -> dict:
        """Return miner status summary."""
        return self._send_command(
            cmd="get.miner.status",
            param="summary",
        )

    def get_working_status(self) -> bool:
        """Return True if miner is working."""
        resp = self._send_command(
            cmd="get.device.info",
            param="miner",
        )
        working = resp.get("msg", {}).get("miner", {}).get("working", "false")
        return working.lower() == "true"

    def _fetch_device_type(self) -> str:
        """Fetch miner model from device."""
        resp = self._send_command(
            cmd="get.device.info",
            param="miner",
        )
        return resp.get("msg", {}).get("miner", {}).get("type", "WhatsMiner")

    def _send_command(self, cmd: str, param: str) -> dict:
        """Send command to miner and return response."""
        salt = self._get_salt()
        ts = int(time.time())
        token = self._generate_token(cmd, salt, ts)

        req = {
            "cmd": cmd,
            "ts": ts,
            "token": token,
            "account": self._account,
            "param": param,
        }

        sock = socket.socket()
        sock.settimeout(5)
        sock.connect((self._host, self._port))
        self._send_json(sock, req)
        resp = self._recv_json(sock)
        sock.close()

        return resp

    def _get_salt(self) -> str:
        """Get salt from miner."""
        sock = socket.socket()
        sock.settimeout(5)
        sock.connect((self._host, self._port))
        self._send_json(sock, {"cmd": "get.device.info", "param": "salt"})
        resp = self._recv_json(sock)
        sock.close()

        return resp["msg"]["salt"]

    def _generate_token(self, cmd: str, salt: str, ts: int) -> str:
        """Generate token for API command."""
        raw = f"{cmd}{self._password}{salt}{ts}"
        sha = hashlib.sha256(raw.encode()).digest()
        token = base64.b64encode(sha).decode()
        return token[:8]

    def _send_json(self, sock: socket.socket, data: dict) -> None:
        payload = json.dumps(data, separators=(",", ":")).encode()
        length = len(payload).to_bytes(4, "little")
        sock.sendall(length + payload)

    def _recv_json(self, sock: socket.socket) -> dict:
        hdr = self._recv_exact(sock, 4)
        length = int.from_bytes(hdr, "little")
        payload = self._recv_exact(sock, length)
        return json.loads(payload.decode())

    def _recv_exact(self, sock: socket.socket, length: int) -> bytes:
        data = b""
        while len(data) < length:
            chunk = sock.recv(length - len(data))
            if not chunk:
                raise ConnectionError("Socket closed")
            data += chunk
        return data
