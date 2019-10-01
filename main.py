from pydub import AudioSegment
from google.cloud.speech import types
from google.cloud.speech import enums
from google.cloud import speech
import io

MP3_FILE_PATH = 'data/origin3.mp3'

client = speech.SpeechClient()


class SpeechToText:
    def create_config(self):
        return types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=16000,
            language_code='ja-JP')

    def transcribe_file(self, speech_flac_file: str) -> None:
        """音声ファイルの文字おこしをする

        Args:
            speech_flac_file (str): flac形式の音声ファイルパス
        """

        with io.open(speech_flac_file, 'rb') as audio_file:
            content = audio_file.read()

        audio = types.RecognitionAudio(content=content)
        config = self.create_config()

        self.print_response(
            client.recognize(config, audio)
        )

    def long_transcribe_gcs(self, gcs_uri: str) -> None:
        """1分以上の長い音声ファイルの文字おこしをする

        Args:
            gcs_uri (str): gcsの音声ファイルのパス
        """

        audio = types.RecognitionAudio(uri=gcs_uri)
        config = self.create_config()

        operation = client.long_running_recognize(config, audio)

        print('Waiting for operation to complete...')

        self.print_response(
            operation.result(timeout=90)
        )

    def print_response(self, response):
        for result in response.results:
            print(u'Transcript: {}'.format(result.alternatives[0].transcript))
            print('Confidence: {}'.format(result.alternatives[0].confidence))


def convert_mp3_to_flac(mp3_file_path: str) -> str:
    """mp3形式の音声ファイルをモノラルのflac音声ファイルに変換する

    Args:
        mp3_file_path (str): mp3形式の音声ファイルパス

    Returns:
        str: flac形式の音声ファイルパス
    """
    sound = AudioSegment.from_mp3(mp3_file_path)

    flac_file_path = mp3_file_path.replace('.mp3', '.flac')

    sound.export(
        flac_file_path,
        format="flac",
        parameters=["-ac", "1"])

    return flac_file_path


if __name__ == "__main__":
    speech_flac_file = convert_mp3_to_flac(
        MP3_FILE_PATH
    )

    speech_to_text = SpeechToText()
    speech_to_text.transcribe_file(speech_flac_file)
    # speech_to_text.long_transcribe_gcs("gs://audio_data_for_speech_to_text/speech.flac")
