

## Youtube Clip CCs

Quickly generate closed captions for youtube clips. 
This simple repo makes use of FaceBooks Wav2Vec model to generate English Subtitles / Captions for a YT Clip.

## Usage

``git clone https://github.com/Muennighoff/ytclipcc.git`` <br>
``cd ytclipcc`` <br>
``pip install -r requirements.txt`` <br>
``python create_cc.py`` <br>

To run it with your own clip & timestamps run e.g. <br>
``python create_cc.py --url https://www.youtube.com/watch?v=7Ood-IE7sx4 --start 1 --end 4`` <br>
& it should print out: <br>
I HAVE THE HIGH GROUND 
