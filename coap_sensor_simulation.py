import asyncio
import random
from aiocoap import *

async def simulate_sensor_data():
    protocol = await Context.create_client_context()
    print("CoAP sensor simulation started")
    print("Note: Connection errors are expected if no CoAP server is running")
    print("Press Ctrl+C to stop\n")
    
    while True:
        temperature = random.uniform(20.0, 25.0)
        humidity = random.uniform(30.0, 50.0)
        payload = f'{{"temperature": {temperature:.2f}, "humidity": {humidity:.2f}}}'.encode('utf-8')
        request = Message(code=POST, payload=payload)
        request.set_request_uri('coap://localhost/sensor/data')
        
        try:
            response = await protocol.request(request).response
            print(f'CoAP Result: {response.code}')
            print(f'Payload: {response.payload.decode()}\n')
        except Exception as e:
            print(f'CoAP Error: {e}')
            print(f'Generated data: {payload.decode()}\n')
        
        await asyncio.sleep(1)

try:
    asyncio.run(simulate_sensor_data())
except KeyboardInterrupt:
    print("\nStopping CoAP sensor...")