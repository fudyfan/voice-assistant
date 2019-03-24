from alexa_client import AlexaClient

def connect_to_avs():
	client = AlexaClient(
	    client_id='amzn1.application-oa2-client.525fbe13dd8847cf9db70b37c7ab55be',
	    secret='a94a2625e22d715d1578abfdba4ad93d2afe6f1f34ae245a4c9681eb83b6ff15',
	    refresh_token='Atzr|IwEBII018elk-PO7ghmHkqIwr-yRUuM2lRtteH0lw853BNKuA0-TN3q6IdJFoau4BHlB85AySJuapMWmclI6DXrPZztA_0bLqF_XnL-Cl9Otq2j-W0X7BVuJZwzC16IzZ_AhUlGc0rNpT4LHP-8IQ3k5lE7d7kJab670SA0Q8Z2HpzNC3nCYMB7Blbe4SKrgz2od0SyDmLleUBRZF26NryNXr67aR_EQoIjzsgxjDt_nOhQg7b5gz2q5ImlSaWlCgvF-lF8mcR14qeh2zAj9x3UWf2MaIRR6lA4Ww8KTzVKvBl-PQmtH4eOFj9_o2PRdVCWhUE-3dwONF3aIjJryRsSMxmrIJmB9HrkBfMyJlapEcBDDSFn1yFP27aHN1J9NpK-4Nq5EMXDmD3TcI-65Lb9IZXVXpFZnY5wSTKeyyqcsnhHQ16zrCwUuumJx6K9SmVoSUe66TaJuxd5DqmHxKkhUJ0Yna6P3BAMBGyDirBTcQ-bU6HyqR4OIKZ_DiS7kaiNk0RAyd-eOBrji5bR4BPYtLFEXWgIRIy5kcHeRPELAJJ4tRg',
	)
	client.connect()  # authenticate and other handshaking steps
	return client

def send_rec_to_avs(wav_file, client):
	outfiles = []
	with open(wav_file, 'rb') as f:
	    for i, directive in enumerate(client.send_audio_file(f)):
	        if directive.name in ['Speak', 'Play']:
	            with open('./output_{}.mp3'.format(i), 'wb') as f:
	                f.write(directive.audio_attachment)
	                outfiles += ['output_{}.mp3'.format(i)]
	return outfiles