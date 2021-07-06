

## Youtube Clip CCs

Quickly generate closed captions for youtube clips. 
This simple repo makes use of Facebooks Wav2Vec2 model to generate English Subtitles / Captions for a YT Clip.
The notebook is now also part of huggingface's community notebooks and can be found here: https://huggingface.co/transformers/master/community.html#community-notebooks

## Usage

``git clone https://github.com/Muennighoff/ytclipcc.git`` <br>
``cd ytclipcc`` <br>
``pip install -r requirements.txt`` <br>
``python create_cc.py`` <br>

To run it with your own clip & timestamps run e.g. <br>
``python create_cc.py --url https://www.youtube.com/watch?v=7Ood-IE7sx4 --start 1 --end 4`` <br>
& it should print out: <br>
I HAVE THE HIGH GROUND 
