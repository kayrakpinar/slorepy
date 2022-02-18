import soundfile as sf
from pedalboard import Pedalboard, Reverb
import ffmpy
import os
import json
import argparse

with open('config.json', 'r') as config:
    data=config.read()
obj = json.loads(data)

ap = argparse.ArgumentParser()
ap.add_argument("-a", "--audio", required=True,help="Audio File")
ap.add_argument("-e", "--ext", required=False,help="File Extension")
data = ap.parse_args()
audio_input = data.audio
audio_name = audio_input[:-4]
audio_ext = audio_input[-4:]
output_file_extension = "wav"
audio_speed = obj["audio_speed"]
reverb_room_size = obj["reverb_room_size"]
reverb_wet_level = obj["reverb_wet_level"]

if data.ext:
  output_file_extension = data.ext

slowed_output = "{}-slowed-output.wav".format(audio_name)
processed_output = '{}-slowed-reverb.{}'.format(audio_name, output_file_extension)

if os.path.exists(processed_output):
  print("This audio has already been processed: {}".format(os.getcwd()))
  exit()

ff = ffmpy.FFmpeg(inputs={audio_input: None}, outputs={slowed_output: "-af \"asetrate=44100*{}\"".format(audio_speed)})
ff.run()
audio, sample_rate = sf.read(slowed_output)
board = Pedalboard([Reverb(room_size=reverb_room_size, wet_level = reverb_wet_level)])
effected = board(audio, sample_rate)

sf.write("{}-slowed-reverb.wav".format(audio_name), effected, sample_rate)

if os.path.exists(slowed_output):
  os.remove(slowed_output)

if data.ext and data.ext != "wav":
  ff = ffmpy.FFmpeg(inputs={"{}-slowed-reverb.wav".format(audio_name): None}, outputs={processed_output: None})
  ff.run()
  os.remove("{}-slowed-reverb.wav".format(audio_name))
