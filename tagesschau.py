import requests
import subprocess

try:
    response = requests.get('https://www.tagesschau.de/api2u/homepage')
    response.raise_for_status()
    json_data = response.json()
    text = ""
    for i, news_i in enumerate(json_data['news']):
        text += f"{news_i.get('topline', '')} {news_i.get('title', '')} {news_i.get('firstSentence', '')}\n"
        if i >= 3:
            break

    process = subprocess.Popen(
        [
            "piper/piper",
            "--model",
            "de_DE-thorsten-high.onnx",
            "--output_file",
            "output.wav"
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(input=text)
    if process.returncode != 0:
        print(f"Error: {stderr}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching the resource: {e}")
except ValueError as e:
    print(f"Error parsing JSON: {e}")


'''
TODO 
regional - n - regionID == 2? - date: title (-> details)
news - n - sort by breaking - topline: title, firstSentence
'''
