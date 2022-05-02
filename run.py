import asyncio
import json
from random import randint
import time
import sys
import websockets


async def send(websocket, action, data):
    message = json.dumps(
        {
            'action': action,
            'data': data,
        }
    )
    print(message)
    await websocket.send(message)


async def start(auth_token):
    uri = "ws://localhost:8001/ws?token={}".format(auth_token)
    # uri = "wss://4yyity02md.execute-api.us-east-1.amazonaws.com/ws?token={}".format(auth_token)
    while True:
        try:
            print('connection to {}'.format(uri))
            async with websockets.connect(uri) as websocket:
                await play(websocket)
        except KeyboardInterrupt:
            print('Exiting...')
            break
        except Exception:
            print('connection error!')
            time.sleep(3)


async def play(websocket):
    while True:
        try:
            response = await websocket.recv()
            print(f"< {response}")
            data = json.loads(response)
            if data['event'] == 'update_user_list':
                pass
            if data['event'] == 'gameover':
                pass
            if data['event'] == 'challenge':
                # if data['data']['opponent'] == 'favoriteopponent':
                await send(
                    websocket,
                    'accept_challenge',
                    {
                        'challenge_id': data['data']['challenge_id'],
                    },
                )
            if data['event'] == 'your_turn':
                await send(
                    websocket,
                    'move',
                    {
                        'game_id': data['data']['game_id'],
                        'turn_token': data['data']['turn_token'],
                        'from_row': randint(0, 15),
                        'from_col': randint(0, 15),
                        'to_row': randint(0, 15),
                        'to_col': randint(0, 15),
                    },
                )

        except Exception as e:
            print('error {}'.format(str(e)))
            break  # force login again


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        auth_token = sys.argv[1]
        asyncio.get_event_loop().run_until_complete(start(auth_token))
    else:
        print('please provide your auth_token')
