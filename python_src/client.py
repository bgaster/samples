import asyncio
import websockets
import json
import sys

async def send_message(websocket, message, client_id):
    outward_message = {
        'client_id': client_id,
        'payload': message
    }

    await websocket.send(json.dumps(outward_message))

async def recv_message(websocket):
    message = json.loads(await websocket.recv())
    return message['payload']

async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s+' '))
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)

async def main():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        # After joining server will send client unique id.
        message = json.loads(await websocket.recv())
        print(message)

        # Get the client_id from the join message
        if message['type'] == 'join_evt':
            client_id = message['client_id']
        else:
            # If first message is not the join message exit
            print("Did not receive a correct join message")
            return 0

        input = await ainput("Enter a string: \n")
        while input != "end\n":
            # Send a ping to the server
            await send_message(websocket, input, client_id)

            # Wait for the 'pong' response from the server
            response = await recv_message(websocket)

            print("The Server Sent Back:")
            print(response)
            input = await ainput("Enter a string: \n")

        return 0

if __name__ == "__main__":
    print("Echo client")
    asyncio.run(main())