from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time
import re
import os

initial_path = os.getcwd()
with open("YOUR_JSON_PATH", 'r', encoding='utf-8') as json_file:
    word_list = json.load(json_file)

nb_mots = 0
nb_essais = 0
# Output list of unfound words
word_not_found = []
driver = webdriver.Firefox()

driver.get('https://derja.ninja/')
output_object = {}
for word in word_list:
    # to be printed
    nb_essais += 1

    search_word = word

    input_element = driver.find_element(
        By.CSS_SELECTOR, ".search-input.search-input--large.js-search-input")
    input_element.send_keys(search_word)

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

        # Get the first 3 results for the query
        for i in range(min(len(results), 3)):
            audio_found = False

            # Some elements might not have an audio file
            try:
                sentence_audio_arabic = results[i].find(
                    'div', class_='search_result__example_sentence_in_arabic').find("audio").get("src")
                audio_found = True
            except Exception as e:
                print(e)

            # get sample sentence in english
            search_result__example_sentence_in_english = results[i].find(
                'div', class_='search_result__example_sentence_in_english').find("span").text

            # get the translation for english sample sentence
            search_result__example_sentence_in_arabic = results[i].find(
                'div', class_='search_result__example_sentence_in_arabic').find(
                'span', class_='example-sentence').text

            output_object[search_word]["result"] = search_result__term_in_arabic
            if audio_found:
                output_object[search_word
                              ][f"sample_{i}"] = [search_result__example_sentence_in_english, search_result__example_sentence_in_arabic, sentence_audio_arabic]
            else:
                output_object[search_word
                              ][f"sample_{i}"] = [search_result__example_sentence_in_english, search_result__example_sentence_in_arabic]

        print(f"{nb_mots}/{nb_essais}")
    else:
        word_not_found.append(word)

    # Go back to main page for next search
    main_page = driver.find_element(
        By.CSS_SELECTOR, '.navbar > a:nth-child(2)')
    main_page.click()
    time.sleep(0.25)


driver.quit()

file_name = "YOUR_FILE_NAME"

os.chdir(initial_path)
with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(output_object, file, ensure_ascii=False)

with open(f"output_json/{file_name}", 'w', encoding='utf-8') as file:
    json.dump(word_not_found, file, ensure_ascii=False)

print(nb_mots)
print(word_not_found)
