import requests
import json

# AnkiConnect local url
ANKI_URL = "http://localhost:8765"


def add_card(deck_name, front, word_translation, back_sentences, audio_files):
    # merge audio and sentences
    single_word_translation = f"<p>{word_translation}</p>"

    back_content = "<br>".join([f"<p>{back_sentences[i][0]} {back_sentences[i][1]} [sound:{audio_files[i]}]</p>"
                                for i in range(len(back_sentences))])
    back_content = single_word_translation + back_content

    # Add a card to a specific deck
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back_content

                },
                "options": {
                    "allowDuplicate": False
                },
            }
        }
    }
    response = requests.post(ANKI_URL, data=json.dumps(payload))
    return response.json()


with open("translations_results.json", 'r', encoding='utf-8') as json_file:
    word_list = json.load(json_file)

for keyword in word_list:
    word_translation = ""
    sentences = []
    audios = []
    # Build sentence list
    word_translation = word_list[keyword]["result"]
    audios.append(
        f"C:/Users/vidal/AppData/Roaming/Anki2/User 1/collection.media/{keyword}_translation_0.mp3")

    for i in range(int((len(word_list[keyword])))-1):
        sentences.append(word_list[keyword][f"sample_{i}"])
        # build the list of audios files
        audios.append(
            f"C:/Users/vidal/AppData/Roaming/Anki2/User 1/collection.media/{keyword}_sample_sentence_translation_{i}.mp3")

    # add the card with audios to the deck
    card_addition_result = add_card(
        "Tunisian_arabic_derja_top5000words", keyword, word_translation, sentences, audios)
