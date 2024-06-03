import asyncio
import websockets
import json

connected_clients = set()

async def register(websocket, name):
    connected_clients.add((websocket, name))
    print(f"{name} connected from {websocket.remote_address}")

async def unregister(websocket, name):
    connected_clients.remove((websocket, name))
    print(f"{name} disconnected from {websocket.remote_address}")

async def broadcast(message):
    if connected_clients:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([client[0].send(message) for client in connected_clients])

async def handle_client(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        if data["type"] == "register":
            name = data["data"]
            await register(websocket, name)
            join_message = json.dumps({"type": "message", "data": f"{name} has joined the chat."})
            await broadcast(join_message)
        elif data["type"] == "message":
            await broadcast(json.dumps({"type": "message", "data": data["data"]}))
        elif data["type"] == "unregister":
            name = data["data"]
            await unregister(websocket, name)

start_server = websockets.serve(handle_client, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
