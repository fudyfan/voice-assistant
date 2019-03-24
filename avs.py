from alexa_client import AlexaClient
from alexa_client import constants

from dotenv import load_dotenv
import os
load_dotenv()

client = AlexaClient(
    client_id='amzn1.application-oa2-client.525fbe13dd8847cf9db70b37c7ab55be',
    secret=os.getenv('CLIENT_SECRET'),
    refresh_token=os.getenv('REFRESH_TOKEN'),
)


client.connect()  # authenticate and other handshaking steps
with open('out.wav', 'rb') as f:
    
    obj = client.send_audio_file(audio_file=f, distance_profile=constants.FAR_FIELD)
    for i, directive in enumerate(obj):
        if directive.name in ['Speak', 'Play']:
            with open(f'./output_{i}.mp3', 'wb') as f:
                f.write(directive.audio_attachment)

print("hi")