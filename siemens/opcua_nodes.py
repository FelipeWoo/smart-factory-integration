from opcua import Client

URL = "opc.tcp://192.168.8.211:4840"


def walk(node, level=0, max_depth=4):
    if level > max_depth:
        return
    try:
        print("  " * level +
              f"- {node} | {node.get_browse_name()} | {node.get_display_name().Text}")
    except Exception as e:
        print("  " * level + f"- {node} | error: {e}")
        return

    try:
        for child in node.get_children():
            walk(child, level + 1, max_depth)
    except Exception:
        pass


client = Client(URL)

try:
    print(f"connecting to {URL} ...")
    client.connect()
    print("connected")

    objects = client.get_objects_node()
    walk(objects, max_depth=4)

finally:
    client.disconnect()
    print("disconnected")
