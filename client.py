#!/usr/bin/env python3
"""
Simple TCP client to test server.py
Usage:
    python3 client.py --host 127.0.0.1 --port 9000
Then type messages; Ctrl+D (or Ctrl+C) to quit.
"""
import socket
import argparse
import datetime

def now():
    return datetime.datetime.now().isoformat(sep=' ', timespec='seconds')

def run_client(host: str, port: int):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[{now()}] Connecting to {host}:{port} ...")
        sock.connect((host, port))
        print(f"[{now()}] Connected.")
        print("Type messages and press Enter. Ctrl+C to quit.")
        with sock:
            while True:
                try:
                    msg = input("> ")
                except EOFError:
                    print("\nEOF received; closing.")
                    break
                if not msg:
                    continue
                sock.sendall((msg + "\n").encode())
                data = sock.recv(4096)
                if not data:
                    print(f"[{now()}] Server closed connection.")
                    break
                print(f"[{now()}] Server replied: {data.decode().strip()}")
    except ConnectionRefusedError:
        print(
            f"[{now()}] ERROR: Could not connect to {host}:{port} "
            "(connection refused)."
        )
    except KeyboardInterrupt:
        print(f"\n[{now()}] Client interrupted by user.")
    except Exception as e:
        print(f"[{now()}] Client error: {e}")
    finally:
        try:
            sock.close()
        except Exception:
            pass
        print(f"[{now()}] Client exiting.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple TCP client")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")
    parser.add_argument("--port", type=int, default=9000, help="Server port")
    args = parser.parse_args()
    run_client(args.host, args.port)
