from pydub import AudioSegment
from google.cloud.speech import types
from google.cloud.speech import enums
from google.cloud import speech
import io
import os

DATA_DIR_PATH = os.path.join(
    os.path.dirname(__file__),
    'data'
)

MP3_FILE_PATH = DATA_DIR_PATH + '/speech_origin.mp3'
SPLITTED_FILE_FILE = DATA_DIR_PATH + '/output0.flac'
RESULT_FILE_PATH = DATA_DIR_PATH + 'result.json'

client = speech.SpeechClient()


def speech_to_text(speech_flac_file):
    """Transcribe the given audio file."""

    with io.open(speech_flac_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='ja-JP')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(result.alternatives[0].transcript)


def convert_mp3_to_flac(file_path):
    sound = AudioSegment.from_mp3(file_path)

    sound.export(
        SPLITTED_FILE_FILE,
        format="flac",
        parameters=["-ac", "1"])

    return SPLITTED_FILE_FILE


if __name__ == "__main__":
    speech_flac_file = convert_mp3_to_flac(
        MP3_FILE_PATH
    )

    speech_to_text(SPLITTED_FILE_FILE)
