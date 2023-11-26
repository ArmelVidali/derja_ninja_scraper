from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time
import re
from download_audio import download_mp3


with open("json/sample.json", 'r') as json_file:
    word_list = json.load(json_file)


i = 0

driver = webdriver.Firefox()

driver.get('https://derja.ninja/')
output_object = {}
for word in word_list:

    search_word = word["be"]

    print(output_object)

    i += 1

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
        output_object[search_word] = {}
        # Get the first 3 results for the query
        for i in range(min(len(results), 3)):
            search_result__term_in_arabic = results[i].find(
                'div', class_='search-result__term_in_arabic').text
            # removes spaces an updatebrowser message
            search_result__term_in_arabic = re.sub(
                r'\s+', '', search_result__term_in_arabic).replace("Updateyourbrowser", "")
            # finally extract only the arabic alphabet word
            search_result__term_in_arabic = re.sub(
                r'[^؀-\u07FF\s]+', '', search_result__term_in_arabic)

            # get sample sentence in english
            search_result__example_sentence_in_english = results[i].find(
                'div', class_='search_result__example_sentence_in_english').find("span").text

            # get the translation for english sample sentence
            search_result__example_sentence_in_arabic = results[i].find(
                'div', class_='search_result__example_sentence_in_arabic').find(
                'span', class_='example-sentence').text

            output_object[search_word]["result"] = search_result__term_in_arabic
            output_object[search_word
                          ][f"english_sample_{i}"] = search_result__example_sentence_in_english
            output_object[search_word
                          ][f"arabic_sample_{i}"] = search_result__example_sentence_in_arabic

            # Some elements might not have an audio file
            try:
                word_audio_arabic = results[i].find(
                    'div', class_='search-result__term_in_arabic').find("audio").get("src")
                sentence_audio_arabic = results[i].find(
                    'div', class_='search_result__example_sentence_in_arabic').find("audio").get("src")
                download_mp3(word_audio_arabic,
                             f"audios/{search_word}_translation_{i}")
                download_mp3(sentence_audio_arabic,
                             f"audios/{search_word}_sample_sentence_translation_{i}")
            except Exception as e:
                print(e)

    # Go back to main page for next search
    main_page = driver.find_element(
        By.CSS_SELECTOR, '.navbar > a:nth-child(2)')
    main_page.click()
    time.sleep(1)
    if i == 15:
        break
driver.quit()

file_name = "translations_results.json"

with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(output_object, file, ensure_ascii=False)
