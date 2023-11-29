import requests
import os


def download_mp3(mp3_url, output_name):

    file_url = mp3_url
    os.chdir(r"C:/Users/vidal/AppData/Roaming/Anki2/User 1/collection.media/")
    output_file = output_name + ".mp3"

    response = requests.get(file_url)

    if response.status_code == 200:
        with open(output_file, 'wb') as file:
            file.write(response.content)
    else:
        print("Failed to download the file")
