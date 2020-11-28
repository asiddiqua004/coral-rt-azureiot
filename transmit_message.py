import os
import asyncio
import uuid
import time
import sys
import json
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
from coral.enviro.board import EnviroBoard

async def main():

    conn_str = "HostName=5G-IoT-System-For-Emergency-Responders.azure-devices.net;DeviceId=application_device1;SharedAccessKey=x84oYfc8Wm4lL7nfMzNm87X7YmFbC+TtHX4ny+bV8ck="
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client.
    await device_client.connect()

    # Send a few messages
    count = 0
    enviro = EnviroBoard()
    threshold_temp = 40.00
    threshold_ambient_light = 80.00
    file = open("/home/mendel/person_detected.txt","r")
    while count < 50:
        current_temp = enviro.temperature
        current_ambient_light = enviro.ambient_light
        person_detected = file.read(1)
        #print(person_detected)
        message_properties = {"personDetected" : 0}
        if person_detected == '1':
            if current_temp > threshold_temp:
                print("WARNING: Person Detected under high temp conditions!!")
                message_properties["personDetected"] = 1
            if current_ambient_light > threshold_ambient_light:
                print("WARNING: Person Detected under high ambient light conditions!!")
                message_properties["personDetected"] = 1
            #else:
                #print("Person detected under normal conditions!")
        #else:
            #print("Preson Not Detected")
        file.seek(0)
        message_properties["temperature"] = current_temp
        message_properties["humidity"] = enviro.humidity
        message_properties["ambientLight"] = current_ambient_light
        message_properties["pressure"] = enviro.pressure
        message_properties["deviceId"] = "Google-Coral"
        message_properties["lat"] = 37.38574713765911
        message_properties["long"] = -121.89022121011448
        msg = Message(json.dumps(message_properties))
        msg.message_id = uuid.uuid4()
        msg.content_type = 'application/json'
        await device_client.send_message(msg)
        print("Message successfully sent:" + str(msg))
        print()
        count = count + 1
        time.sleep(5)

    # finally, disconnect
    await device_client.disconnect()
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
