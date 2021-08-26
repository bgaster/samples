import asyncio
import json
import websockets
import uuid

import Sample as S

CLIENTS = set()

def join_event():
    client_id = uuid.uuid1().int
    CLIENTS.add(client_id)
    return json.dumps({"type": "join_evt", "client_id": client_id})

async def send_payload_message(websocket, message):

    ping_message = {
        'payload': message
    }

    await websocket.send(json.dumps(ping_message))

async def decode_payload_message(message):

    message = json.loads(message)
    return message['payload']

async def sample_server(websocket, path):
    try:
        sample = S.Sample()

        await websocket.send(join_event())
        async for message in websocket:
            payload = await decode_payload_message(message)

            print(message)

            if 'id' in payload:
                id = payload['id']
                if id == "put":
                     put_sample = sample.make_sample(payload)
                     if put_sample != None:
                         sample.write(put_sample)    
                     await send_payload_message(websocket, json.dumps({ 'id': 'put_reply', 'error': 0 }))
                elif id == "get": 
                    samples = sample.query_unread()
                    # convert timestamps to int from Decimal
                    samples = list(map(lambda s: {'timestamp': int(s['timestamp']), 'values': s['values']}, samples))
                    resp = { 'id': 'get_reply',
                             'samples': samples,
                             'error': 0,
                           }     
                    await send_payload_message(websocket, json.dumps(resp))
                elif id == "mark":
                    if "timestamp" in payload:
                        sample.mark_read(payload['timestamp'], True)
                        await send_payload_message(websocket, json.dumps({ 'id': 'mark_reply', 'error': 0 }))
                    else:
                        await send_payload_message(websocket, json.dumps({ 'id': 'mark_reply', 'error': 1 }))
                elif id == "unmark":
                    if "timestamp" in payload:
                        sample.mark_read(payload['timestamp'], False)
                        await send_payload_message(websocket, json.dumps({ 'id': 'unmark_reply', 'error': 0 }))
                    else:
                        await send_payload_message(websocket, json.dumps({ 'id': 'unmark_reply', 'error': 2 }))
                else:
                    await send_payload_message(websocket, json.dumps({ 'id': 'unsupported command', 'error': 3 })
            else:
                await send_payload_message(websocket, json.dumps({ 'id': 'invalid payload', 'error': 4 })
            
    finally:
        print("Client Disconnected")

start_server = websockets.serve(sample_server, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()