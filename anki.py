import requests
import json

# AnkiConnect local url
ANKI_URL = "http://localhost:8765"


def add_card(deck_name, front, back_sentences, audio_files):
    # merge audio and sentences
    back_content = "<br>".join([f"<p>{sentence}</p><audio src='{audio}' controls></audio>"
                                for sentence, audio in zip(back_sentences, audio_files)])
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
                }
            }
        }
    }
    response = requests.post(ANKI_URL, data=json.dumps(payload))
    return response.json()


with open("translations_results.json", 'r', encoding='utf-8') as json_file:
    word_list = json.load(json_file)

for keyword in word_list:
    sentences = []
    audios = []
    # Build sentence list
    sentences.append(word_list[keyword]["result"])
    for i in range(int((len(word_list[keyword])-1)/2)):
        print(keyword, int((len(word_list[keyword])-1)/2))
        sentences.append(word_list[keyword][f"english_sample_{i}"])
        sentences.append(word_list[keyword][f"arabic_sample_{i}"])
        # build the list of audios files
        audios.append(f"audios/{keyword}_translation_0")
        audios.append(f"audios/{keyword}_sample_sentence_translation_0")

    # add the card with audios to the deck
    card_addition_result = add_card(
        "Tunisian_arabic_derja_top5000words", keyword, sentences, audios)
