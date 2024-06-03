import asyncio
import websockets
import json

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")
        
        # Register the user
        await websocket.send(json.dumps({"type": "register", "data": name}))

        # Sending a message
        async def send_message():
            while True:
                message = input("Enter message: ")
                await websocket.send(json.dumps({"type": "message", "data": message}))

        # Receiving messages
        async def receive_message():
            async for message in websocket:
                data = json.loads(message)
                if data["type"] == "message":
                    print(f"< {data['data']}")

        await asyncio.gather(receive_message(), send_message())

asyncio.get_event_loop().run_until_complete(hello())
