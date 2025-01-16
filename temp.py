from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import speech_recognition as sr


class SentimentApp(App):
    def build(self):
        self.recognizer = sr.Recognizer()
        self.tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
        self.model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

        layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Press the button to start listening.", font_size=20)
        self.result_label = Label(text="", font_size=20, color=[0, 1, 0, 1])
        self.button = Button(text="Start Listening", size_hint=(1, 0.2), font_size=18)
        self.button.bind(on_press=self.recognize_speech)

        layout.add_widget(self.label)
        layout.add_widget(self.result_label)
        layout.add_widget(self.button)

        return layout

    def recognize_speech(self, instance):
        self.label.text = "Listening..."
        with sr.Microphone() as mic:
            try:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(mic)
                audio = self.recognizer.listen(mic)

                # Recognize speech
                text = self.recognizer.recognize_google(audio)
                self.label.text = f"Recognized: {text}"

                # Perform sentiment analysis
                inputs = self.tokenizer(text, return_tensors="pt")
                outputs = self.model(**inputs)
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
                labels = ["negative", "neutral", "positive"]
                predicted_label = labels[torch.argmax(probs)]
                self.result_label.text = f"Sentiment: {predicted_label}"
            except Exception as e:
                self.label.text = f"Error: {e}"


if __name__ == "__main__":
    SentimentApp().run()
