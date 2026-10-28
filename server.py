import asyncio
import websockets
from websockets.exceptions import ConnectionClosed

users = set()

async def chat_handler(websocket):
    users.add(websocket)
    print(f"New client connected. Total online: {len(users)}")

    try:
        async for encrypted_message in websocket:
            # سرور فقط پیام رمز شده را به بقیه پخش می‌کند
            dead = []
            for user in users:
                if user != websocket:
                    try:
                        await user.send(encrypted_message)
                    except ConnectionClosed:
                        dead.append(user)
            for u in dead:
                users.discard(u)
    except ConnectionClosed:
        pass
    finally:
        users.discard(websocket)
        print(f"Client disconnected. Total online: {len(users)}")

async def main():
    async with websockets.serve(chat_handler, "0.0.0.0", 8765):
        print("Server running on port 8765...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
