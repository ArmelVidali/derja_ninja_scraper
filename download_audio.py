import requests


def download_mp3(mp3_url, output_name):

    file_url = mp3_url
    output_file = output_name

    response = requests.get(file_url)

    if response.status_code == 200:
        with open(output_file, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded as '{output_file}'")
    else:
        print("Failed to download the file")
