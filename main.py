import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import pyjokes

# Initialize speech recognition, text-to-speech, and News API
recognizer = sr.Recognizer()  # Initialize the speech recognizer
engine = pyttsx3.init()  # Initialize the text-to-speech engine
newsapi_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=2fee8a1ae8e0479892ea445772e64547"  # News API URL

def speak(text):
    """Function to speak the given text"""
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    """Function to process different commands given by the user"""
    if "open google" in c.lower():
        webbrowser.open_new_tab("https://google.com")  # Open Google in a new tab
    elif "open facebook" in c.lower():
        webbrowser.open_new_tab("https://facebook.com")  # Open Facebook in a new tab
    elif "open youtube" in c.lower():
        webbrowser.open_new_tab("https://youtube.com")  # Open YouTube in a new tab
    elif "open instagram" in c.lower():
        webbrowser.open_new_tab("https://instagram.com")  # Open Instagram in a new tab
    elif "open linkedin" in c.lower():
        webbrowser.open_new_tab("https://in.linkedin.com")  # Open LinkedIn in a new tab
    elif "open whatsapp" in c.lower():
        webbrowser.open_new_tab("https://web.whatsapp.com")  # Open WhatsApp in a new tab
    elif "open reddit" in c.lower():
        webbrowser.open_new_tab("https://reddit.com")  # Open Reddit in a new tab
    elif "open amazon" in c.lower():
        webbrowser.open_new_tab("https://amazon.com")  # Open Amazon in a new tab
    elif "open ebay" in c.lower():
        webbrowser.open_new_tab("https://ebay.com")  # Open eBay in a new tab
    elif "open stackoverflow" in c.lower():
        webbrowser.open_new_tab("https://stackoverflow.com")  # Open Stack Overflow in a new tab
    elif c.lower().startswith("play"):
        song = c.lower().split("play ", 1)[1]
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open_new_tab(link)  # Open the link of the requested song
        else:
            speak("Song not found in the library.")  # Speak if the requested song is not found
    elif "news" in c.lower():
        response = requests.get(newsapi_url)
        if response.status_code == 200:
            data = response.json()
            articles = data['articles']
            speak("Here are the top news headlines:")  # Speak the introduction
            for article in articles[:5]:  # Limiting to the top 5 headlines
                speak(article['title'])  # Speak each news headline
        else:
            speak("Failed to fetch news.")  # Speak if failed to fetch news
    elif "tell me a joke" in c.lower():
        joke = pyjokes.get_joke()
        speak(joke)  # Speak a joke fetched from pyjokes
    else:
        pass  # Do nothing if the command doesn't match any of the above

if __name__ == "__main__":
    speak("Initializing Jarvis...")  # Speak initialization message
    while True:
        try:
            with sr.Microphone() as source:
                r = sr.Recognizer()  # Initialize a new recognizer for each iteration
                print("Listening for wake word...")  # Print status message
                audio = r.listen(source, timeout=5, phrase_time_limit=5)  # Listen for audio input
                word = r.recognize_google(audio)  # Recognize speech from audio
                print(f"Recognized word: {word}")  # Print recognized word

                if word.lower() == "jarvis":
                    speak("Yes")  # Confirm activation
                    print("Jarvis Active...")  # Print status message
                    audio = r.listen(source)  # Listen for command after activation
                    command = r.recognize_google(audio)  # Recognize command from audio
                    print(f"Recognized command: {command}")  # Print recognized command
                    processCommand(command)  # Process the recognized command
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")  # Handle timeout error
        except sr.UnknownValueError:
            print("Could not understand audio")  # Handle unknown value error
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")  # Handle request error
        except Exception as e:
            print(f"An error occurred: {e}")  # Handle any other exception
