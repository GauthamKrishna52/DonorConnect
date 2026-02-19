import os
from google.cloud import vision

# This tells Python where your Google key is
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_key.json'

def extract_text_from_image(image_path):
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description # This returns all the text found
    return "No text found."

# Testing it (you'll need a photo named 'test.jpg' in the folder)
# print(extract_text_from_image('test.jpg'))