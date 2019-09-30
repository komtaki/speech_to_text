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
FLAC_FILE_PATH = DATA_DIR_PATH + '/speech.flac'

client = speech.SpeechClient()


def speech_to_text(speech_flac_file: str) -> str:
    """音声ファイルの文字おこしをする

    Args:
        speech_flac_file (str): flac形式の音声ファイルパス

    Returns:
        str: 文字お越し結果
    """

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


def convert_mp3_to_flac(mp3_file_path: str) -> str:
    """mp3形式の音声ファイルをモノラルのflac音声ファイルに変換する

    Args:
        mp3_file_path (str): mp3形式の音声ファイルパス

    Returns:
        str: flac形式の音声ファイルパス
    """
    sound = AudioSegment.from_mp3(mp3_file_path)

    sound.export(
        FLAC_FILE_PATH,
        format="flac",
        parameters=["-ac", "1"])

    return FLAC_FILE_PATH


if __name__ == "__main__":
    speech_flac_file = convert_mp3_to_flac(
        MP3_FILE_PATH
    )

    speech_to_text(speech_flac_file)
