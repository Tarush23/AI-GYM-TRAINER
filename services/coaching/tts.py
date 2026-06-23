from io import BytesIO
from gtts import gTTS

class TextToSpeech:
    def speak(self,text,lang="en"):
        if text is None:
            return
        
        else:
            cleaned = text.strip()

            buffer = BytesIO()
            gTTS(text=cleaned,lang=lang).write_to_fp(buffer)

            buffer.seek(0)

            return buffer.read()


