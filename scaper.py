from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time
import re
import os
from download_audio import download_mp3

initial_path = os.getcwd()
with open("json/top_5000_words.json", 'r') as json_file:
    word_list = json.load(json_file)

nb_mots = 0
nb_essais = 0
word_not_found = []
driver = webdriver.Firefox()

driver.get('https://derja.ninja/')
output_object = {}
for word in word_list:
    nb_essais += 1

    search_word = word["be"]

    input_element = driver.find_element(
        By.CSS_SELECTOR, ".search-input.search-input--large.js-search-input")
    input_element.send_keys(search_word)

    # Adjust the selector accordingly
    ok_button = driver.find_element(By.CSS_SELECTOR, '.search-button')
    ok_button.click()

    output_page_html = driver.page_source

    soup = BeautifulSoup(output_page_html, 'html.parser')

    results = soup.find_all('li', class_='search-result')

    if len(results) > 0:
        nb_mots += 1
        output_object[search_word] = {}

        search_result__term_in_arabic = results[0].find(
            'div', class_='search-result__term_in_arabic').text
        # removes spaces an updatebrowser message
        search_result__term_in_arabic = re.sub(
            r'\s+', '', search_result__term_in_arabic).replace("Updateyourbrowser", "")
        # finally extract only the arabic alphabet word
        search_result__term_in_arabic = re.sub(
            r'[^؀-\u07FF\s]+', '', search_result__term_in_arabic)
        # get the audio, might not exist
        try:
            word_audio_arabic = results[0].find(
                'div', class_='search-result__term_in_arabic').find("audio").get("src")
            download_mp3(word_audio_arabic,
                         f"{search_word}_translation_{0}")
        except Exception as e:
            print(e)

        # Get the first 3 results for the query
        for i in range(min(len(results), 3)):

            # get sample sentence in english
            search_result__example_sentence_in_english = results[i].find(
                'div', class_='search_result__example_sentence_in_english').find("span").text

            # get the translation for english sample sentence
            search_result__example_sentence_in_arabic = results[i].find(
                'div', class_='search_result__example_sentence_in_arabic').find(
                'span', class_='example-sentence').text

            output_object[search_word]["result"] = search_result__term_in_arabic
            output_object[search_word
                          ][f"sample_{i}"] = [search_result__example_sentence_in_english, search_result__example_sentence_in_arabic]

            # Some elements might not have an audio file
            try:
                sentence_audio_arabic = results[i].find(
                    'div', class_='search_result__example_sentence_in_arabic').find("audio").get("src")
                download_mp3(sentence_audio_arabic,
                             f"{search_word}_sample_sentence_translation_{i}")
            except Exception as e:
                print(e)
        print(f"{nb_mots}/{nb_essais}")
    else:
        word_not_found.append(word)

    # Go back to main page for next search
    main_page = driver.find_element(
        By.CSS_SELECTOR, '.navbar > a:nth-child(2)')
    main_page.click()
    time.sleep(0.25)


driver.quit()

file_name = "translations_results.json"

os.chdir(initial_path)
with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(output_object, file, ensure_ascii=False)

with open("not_found_list.json", 'w', encoding='utf-8') as file:
    json.dump(word_not_found, file, ensure_ascii=False)

print(nb_mots)
print(word_not_found)
