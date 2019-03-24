import real_avs

client = real_avs.connect_to_avs()
real_avs.send_rec_to_avs("out.wav", client)

print('hi') 