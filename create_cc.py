import argparse
import os

import moviepy.editor as mp
from transformers import Wav2Vec2Tokenizer, Wav2Vec2ForCTC
import torch
import librosa


def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--url", type=str, default="https://www.youtube.com/watch?v=91_G8iaokk8", help="Youtube Video to download")
    parser.add_argument("--start", type=int, default=0, help="Seconds where to start")
    parser.add_argument("--end", type=int, default=60, help="Seconds where to end")

    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = parse_args()

    # Download making sure it'll be mp4 & rename Clip
    os.system('youtube-dl {} --recode-video mp4'.format(args.url))
    os.system('mv *.mp4 clip.mp4')

    # Convert mp4 (movie) to mp3 & split to save RAM
    # Note: YT Downloand also allows for downloading only mp3
    clip_paths = []

    clip = mp.VideoFileClip("clip.mp4")
    end = min(clip.duration, args.end)

    for i in range(args.start, int(end), 10):
      sub_end = min(i+10, end)
      sub_clip = clip.subclip(i,sub_end)

      sub_clip.audio.write_audiofile("audio_" + str(i) + ".mp3")
      clip_paths.append("audio_" + str(i) + ".mp3")

    # Generate CC
    tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

    cc = ""

    # Doing one by one instead of batched to save RAM
    for path in clip_paths:
        input_audio, _ = librosa.load(path, 
                                    sr=16000)

        input_values = tokenizer(input_audio, return_tensors="pt", padding="longest").input_values
        
        with torch.no_grad():
            logits = model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            
        transcription = tokenizer.batch_decode(predicted_ids)[0]

        cc += transcription + " "

    # Output CC & clean up - Can also write to a .txt if needed
    print('-'*50)
    print(cc)   
    print('-'*50) 

    os.system('rm *.mp4')
    os.system('rm -r *.mp3')
