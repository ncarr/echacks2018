import asyncio
import json
import websockets

async def counter(websocket, path):
  try:
      async for message in websocket:
          print(message)
  except:
    pass

asyncio.get_event_loop().run_until_complete(
    websockets.serve(counter, '0.0.0.0', 6789))
asyncio.get_event_loop().run_forever()
