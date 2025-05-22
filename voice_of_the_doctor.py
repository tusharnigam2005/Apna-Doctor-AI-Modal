#Setup Text to Speech TTs model with Gtts
import os
from gtts import gTTS
from pydub import AudioSegment 

def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

    wav_path = output_filepath.replace(".mp3", ".wav")
    sound = AudioSegment.from_mp3(output_filepath)
    sound.export(wav_path, format="wav")


#step:2 use model tO Text ouTPut to voice
import subprocess
import platform

mp3_path = r"C:\Users\umang\OneDrive\Desktop\ApnaDoctor\gtts_testing_autoplay.mp3"
wav_path = r"C:\Users\umang\OneDrive\Desktop\ApnaDoctor\gtts_testing_autoplay.wav"


def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
    )
    audioobj.save(output_filepath)

    sound = AudioSegment.from_mp3(output_filepath)
    wav_path = output_filepath.replace(".mp3", ".wav")
    sound.export(wav_path, format="wav")

    os_name = platform.system()
    try:
        if os_name=="Darwin": #formacos
            subprocess.run(['afplay', output_filepath])
        elif os_name=="Windows": #forwindows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync();'])
        elif os_name=="Linux": #forLinux
            subprocess.run('aplay', output_filepath)

        else:
            raise OSError("unsupported os")
    except Exception as e:
        print(f"an error occured while playing the audio: {e}")

        
    return output_filepath
