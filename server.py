#!/usr/bin/env python3
"""
Simple TCP echo server for midterm.
Usage:
    python3 server.py --host 127.0.0.1 --port 9000
"""
import socket
import threading
import argparse
import datetime

def now():
    return datetime.datetime.now().isoformat(sep=" ", timespec="seconds")

def handle_client(conn: socket.socket, addr):
    print(f"[{now()}] Connection from {addr}")
    try:
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:
                    # client closed connection
                    print(f"[{now()}] {addr} disconnected")
                    break
                text = data.decode(errors="replace").strip()
                print(f"[{now()}] Received from {addr}: {text}")
                response = f"Server echo: {text}\n"
                conn.sendall(response.encode())
    except Exception as e:
        print(f"[{now()}] Error with {addr}: {e}")

def run_server(host: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # allow fast reuse during tests
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((host, port))
        sock.listen(5)
        print(f"[{now()}] Server listening on {host}:{port}")
        while True:
            conn, addr = sock.accept()
            t = threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            )
            t.start()
    except KeyboardInterrupt:
        print(f"\n[{now()}] Server shutting down (KeyboardInterrupt).")
    except Exception as e:
        print(f"[{now()}] Server error: {e}")
    finally:
        sock.close()
        print(f"[{now()}] Socket closed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple TCP echo server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    parser.add_argument("--port", type=int, default=9000, help="Port to bind")
    args = parser.parse_args()
    run_server(args.host, args.port)
  
