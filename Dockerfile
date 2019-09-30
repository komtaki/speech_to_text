FROM  python:3.7-slim

RUN apt-get update && apt-get install -y ffmpeg

COPY ./ /app/speech_to_text/

WORKDIR /app/speech_to_text/

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]