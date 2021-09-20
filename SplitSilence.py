"""
Script to split audio by silence
The script will divide your mp3 file into chunks divided by where there is silence
"""
"""
Modifying the code of Vašek R.
"""
import os
import shutil
from pydub import AudioSegment
from pydub.silence import split_on_silence
from mutagen.mp3 import MP3


def match_target_amplitude(aChunk, target_dBFS):
    """Normalize given audio chunk"""
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

def read(audio_file):
    """ The file name in my case was SubjectName_sentence.mp3 """
    
    root = audio_file.replace(audio_file.split("/")[-1],"")
    sub = (audio_file.split("/")[-1]).split("_")[0]
    subject = root + sub
    
    if not os.path.exists(subject):
        os.mkdir(subject)
    
    sent = (audio_file.split("/")[-1].replace(sub,"")).replace(".mp3","")[1:]
    sound = AudioSegment.from_mp3(audio_file)
    dBFS = sound.dBFS
    chunks = split_on_silence(sound, min_silence_len = 2000,silence_thresh = dBFS-20)
    # Process each chunk with your parameters
    for i, chunk in enumerate(chunks):
        # Create a silence chunk that is 1 second (or 1000 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=1000)
        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunk + silence_chunk
        # Normalize the entire chunk.
        normalized_chunk = match_target_amplitude(audio_chunk, -20.0)
        # Export the audio chunk with new bitrate.
        name = os.path.join(subject,sent+"_chunk{0}.mp3".format(i))        
        print("Exporting ",name)
        normalized_chunk.export(name,bitrate = "192k",format = "mp3")
    for root, dirs, files in os.walk(subject):
        for name in files:
            audio = MP3(os.path.join(subject,name))
            if audio.info.length<3:
                os.remove(os.path.join(subject,name))

           

def copy_files():
    """ Copies the original files from a folder 'audio' into a new folder 'audioModified' """ 
    if os.path.exists("audioModified"):
        shutil.rmtree('audioModified')
    shutil.copytree("audio", "audioModified") 

if __name__ == "__main__":
    #copy_files()
    audio_path = "audioModified"
    for root, dirs, files in os.walk(audio_path):
        for name in files:
            if ".mp3" in name:
                read(os.path.join(root,name))
