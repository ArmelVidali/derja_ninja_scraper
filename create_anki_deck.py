import requests
import json

# AnkiConnect local url
ANKI_URL = "http://localhost:8765"


def add_card(deck_name, front, word_translation, back_sentences):
    # merge audio and sentences
    single_word_translation = f"<p><span style='font-size: 35px;'>{word_translation}</span></p>"

    back_content = ""
    # handle poentially missing audio url
    for i in range(len(back_sentences)):
        if len(back_sentences[i]) == 3:
            back_content += f"<p>{back_sentences[i][0]}<br><span style='font-size: 45px;'>{back_sentences[i][1]}</span><br><audio controls><source src={back_sentences[i][2]} type=\"audio/mp3\"></audio></p>"

        else:
            back_content += f"<p>{back_sentences[i][0]}<br>{back_sentences[i][1]} ]</p>"

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


with open("translations_results_11k.json", 'r', encoding='utf-8') as json_file:
    word_list = json.load(json_file)
nb_mots = 0
for keyword in word_list:
    print(f"{nb_mots}/11000")
    word_translation = ""
    sentences = []
    # Build sentence list
    word_translation = word_list[keyword]["result"]

    for i in range(int((len(word_list[keyword])))-1):
        sentences.append(word_list[keyword][f"sample_{i}"])

    # add the card with audios to the deck
    card_addition_result = add_card(
        "Tunisian_arabic_derja_top5000words", keyword, word_translation, sentences)
    nb_mots += 1
