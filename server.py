import asyncio
import websockets
import json
import cv2 as cv
import time
import base64

#FPS = 300

cam_port = 0
cam = cv.VideoCapture(cam_port) 

cam.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

def get_jpg_as_b64():
    ret, frame = cam.read()
    ret, buffer = cv.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    js = json.dumps({"type": "DISPLAY_MESSAGE", "data": {"image": jpg_as_text}})
    return js

async def send_msg(websocket):
    while(True):
        frame = get_jpg_as_b64()
        await websocket.send(frame)
        #await asyncio.sleep(1/FPS)

async def echo(websocket):
    
    async for message in websocket:
        await send_msg(websocket)
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "localhost", 8000):
    #async with websockets.serve(echo, "192.168.0.29", 8000):
        await asyncio.Future()  # run forever

asyncio.run(main())