# Build your Tunisian arabic dataset

Get Tunisian translation, audio and sample sentence for the most common 20.000 english word for the awsome website https://derja.ninja/

## Install

To download the project, run 

    git clone https://github.com/ArmelVidali/derja_ninja_scraper

Install depencencies 

    pip install -r requirements.txt

Run scraper.py to start scraping :

    python scraper.py

Run anki.py (need Anki app installed on your computer, with Anki connector https://foosoft.net/projects/anki-connect/ )

    python anki.py

## Output

You will get a `translations_results.json` with the translations and an `audios` folder containing audio files for each translated word and sample sentence provided by Derja Ninja
