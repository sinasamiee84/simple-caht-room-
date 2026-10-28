import asyncio
import sys
import websockets
from websockets.exceptions import ConnectionClosed
from cryptography.fernet import Fernet

# کلیدی که در مرحله قبل ساختید را اینجا بگذارید (باید بین دو نفر یکسان باشد)
SECRET_KEY = b"Simple jey"
cipher = Fernet(SECRET_KEY)

SERVER_IP = "simple IP"  # آی‌پی سرور
PORT = 8765


async def receive_messages(websocket):
    try:
        async for encrypted_msg in websocket:
            try:
                # رمزگشایی پیام دریافت شده
                decrypted_msg = cipher.decrypt(encrypted_msg.encode()).decode()
                sys.stdout.write(f"\r[your friend]: {decrypted_msg}\n")
            except Exception:
                sys.stdout.write("\r[!] پیامی با کلید نامعتبر دریافت شد!\n")
            sys.stdout.write("You: ")
            sys.stdout.flush()
    except ConnectionClosed:
        print("\n[!] اتصال به سرور قطع شد.")


async def main():
    uri = f"ws://{SERVER_IP}:{PORT}"
    print(f"Connecting to {uri} ...")

    async with websockets.connect(uri) as websocket:
        print("Connected securely with End-to-End Encryption!")
        print("Type your message (type 'exit' to quit):\n")

        recv_task = asyncio.create_task(receive_messages(websocket))

        try:
            while True:
                sys.stdout.write("You: ")
                sys.stdout.flush()
                msg = await asyncio.to_thread(input)

                if msg.lower() == "exit":
                    break
                if msg.strip():
                    # قفل کردن پیام قبل از فرستادن روی شبکه
                    encrypted_msg = cipher.encrypt(msg.encode()).decode()
                    await websocket.send(encrypted_msg)
        finally:
            recv_task.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient stopped.")
