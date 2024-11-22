import asyncio
import edge_tts
import argparse

# Define available voices
VOICES = ['vi-VN-HoaiMyNeural', 'vi-VN-NamMinhNeural']

# Set up argparse to get the voice as a command-line argument
parser = argparse.ArgumentParser(description="Generate speech from text.")
parser.add_argument(
    '--voice',
    type=int,
    choices=range(len(VOICES)),
    default=1,
    help=f"Choose a voice (default: 1). Available: {', '.join([str(i) + ': ' + voice for i, voice in enumerate(VOICES)])}"
)

args = parser.parse_args()

# Get the voice based on the argument
VOICE = VOICES[args.voice]

# Read the text from the file
with open("text.txt", "r", encoding="utf-8") as file:
    TEXT = file.read()

OUTPUT_FILE = "test.mp3"

async def amain() -> None:
    comunicate = edge_tts.Communicate(TEXT, VOICE, rate='+20%')
    await comunicate.save(OUTPUT_FILE)

loop = asyncio.get_event_loop_policy().get_event_loop()
try: 
    loop.run_until_complete(amain())
finally: 
    loop.close()
