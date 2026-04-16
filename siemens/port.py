import socket

port = 4840

try:
    s = socket.create_connection(("192.168.8.211", port), timeout=5)
    print(f"TCP {port} open")
    s.close()
except Exception as e:
    print(f"TCP {port} failed:", e)
