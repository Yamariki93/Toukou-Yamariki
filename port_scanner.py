#!/usr/bin/env python3
"""
Simple TCP port scanner.

Usage examples:
  python3 port_scanner.py --host 127.0.0.1 --ports 20-1024 \
    --timeout 0.5 --threads 50
  python3 port_scanner.py --host scanme.nmap.org --ports 20-102 \
    --timeout 0.6 --threads 50

Security notes:
 - Only scan hosts you are authorized to scan (localhost and
   scanme.nmap.org allowed for tests).
 - Be polite: keep timeouts reasonable and add small delays.
"""
import socket
import argparse
import datetime
import concurrent.futures
import time
from typing import Tuple


def now():
    return datetime.datetime.now().isoformat(sep=' ', timespec='seconds')


def scan_port(host: str, port: int, timeout: float) -> Tuple[int, bool, str]:
    """Return (port, is_open, reason)"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            if result == 0:
                return (port, True, "open")
            else:
                return (port, False, f"closed ({result})")
    except socket.gaierror:
        return (port, False, "resolve error")
    except Exception as e:
        return (port, False, f"error: {e}")


def parse_ports(ports_str: str):
    # Accept single port "80", range "20-1024", or comma-separated
    # "22,80,443,8000-8010"
    ports = set()
    for part in ports_str.split(','):
        part = part.strip()
        if '-' in part:
            lo, hi = part.split('-', 1)
            lo = int(lo)
            hi = int(hi)
            if lo < 1 or hi > 65535 or lo > hi:
                raise ValueError("Invalid port range")
            ports.update(range(lo, hi+1))
        else:
            p = int(part)
            if p < 1 or p > 65535:
                raise ValueError("Invalid port number")
            ports.add(p)
    return sorted(ports)


def run_scan(
    host: str,
    ports_list,
    timeout: float,
    threads: int,
    delay: float
):
    print(
        f"[{now()}] Starting scan on {host} - {len(ports_list)} ports "
        f"(timeout={timeout}, threads={threads})"
    )
    open_ports = []
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=threads
    ) as executor:
        future_to_port = {
            executor.submit(scan_port, host, p, timeout): p
            for p in ports_list
        }
        for fut in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[fut]
            try:
                p, is_open, reason = fut.result()
                print(f"[{now()}] Port {p}: {reason}")
                if is_open:
                    open_ports.append(p)
            except Exception as e:
                print(f"[{now()}] Port {port}: scan task error: {e}")
            if delay:
                time.sleep(delay)
    elapsed = time.time() - start
    print(
        f"[{now()}] Scan complete in {elapsed:.2f}s. "
        f"Open ports: {open_ports}"
    )
    return open_ports


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple TCP port scanner")
    parser.add_argument(
        "--host",
        required=True,
        help=(
            "Target host "
            "(127.0.0.1 or scanme.nmap.org)"
        )
    )
    parser.add_argument(
        "--ports",
        default="1-1024",
        help="Ports: 80 or 22,80,443 or 1-1024"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        help="Socket timeout in seconds"
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=50,
        help="Number of concurrent threads"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.01,
        help="Delay between finished tasks to be polite (seconds)"
    )
    args = parser.parse_args()
    try:
        ports = parse_ports(args.ports)
    except ValueError as ve:
        print(f"[{now()}] Invalid ports argument: {ve}")
        exit(2)
    # Basic host resolution check
    try:
        socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"[{now()}] ERROR: Host resolution failed for {args.host}")
        exit(3)
    run_scan(args.host, ports, args.timeout, args.threads, args.delay)
