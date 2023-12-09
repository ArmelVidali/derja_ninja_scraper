# Build your Tunisian arabic dataset

Get Tunisian translation, audio and sample sentence for the most common 20.000 english word for the awsome website https://derja.ninja/

You can get the Anki flashcard deck i created with this script, containing 11.215 words and sentences here : https://ankiweb.net/shared/info/1875413457, looking like this : 


<img src="https://github.com/ArmelVidali/derja_ninja_scraper/assets/84096571/3f2b949d-7352-4383-b431-13942140f17f" alt="image" width="300">




## Install

To download the project, run 

    git clone https://github.com/ArmelVidali/derja_ninja_scraper

Install depencencies 

    pip install -r requirements.txt

Run scraper.py to start scraping :

    python scraper.py

Run anki.py (need Anki app installed on your computer, with Anki connector https://foosoft.net/projects/anki-connect/, with the Anki desktop app opened)

    python anki.py

## Output

You will get a `translations_results.json` with the translations and an audio url for each translated word and sample sentence provided by Derja Ninja.
If you want to download the audios, use the `download_mp3` function from `download_audios.py`.
