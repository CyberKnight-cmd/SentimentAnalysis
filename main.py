# print("Loading..")

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import speech_recognition as sr

print("Initializing...")
# Load tokenizer and model
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
recognizer = sr.Recognizer()

while True:
    with sr.Microphone() as mic:
        r = input("Press Enter to start listening : ")
        print("Hello!\nI am listening you ..........")
        audio = recognizer.listen(mic)

        # Optionally adjust for ambient noise
        recognizer.adjust_for_ambient_noise(mic)

        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            inputs = tokenizer(text, return_tensors="pt")
            outputs = model(**inputs)

            # Compute probabilities
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            labels = ["negative", "neutral", "positive"]

            # Find the label with the highest score
            predicted_label = labels[torch.argmax(probs)]
            print(f"Sentiment: {predicted_label}")

        except Exception as e:
            print(f"Error recognizing speech: {e}")

