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

    # Download & rename Clip
    os.system('youtube-dl {}'.format(args.url))
    os.system('mv *.mkv clip.mkv')

    # Convert mkv (movie) to mp3 & split to save RAM
    clip_paths = []

    for i in range(args.start, args.end, 10):
        clip = mp.VideoFileClip("clip.mkv")
        end = min(clip.duration, i+10)
        clip = clip.subclip(i,end)

        clip.audio.write_audiofile("audio_" + str(i) + ".mp3")
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

        logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = tokenizer.batch_decode(predicted_ids)[0]

        cc += transcription + "  "

    # Output CC - Can also write to a .txt if needed
    print(cc)    