import speech_recognition as sr
import webbrowser
import pyttsx3
from openai import OpenAI
import personalLibrary
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()

# def aiProcess(command):
#     client = OpenAI(api_key="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"
#  )

#     completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a virtual assistant name jarvis."},
#         {
#             "role": "user",
#             "content": command
#         }
#     ]
# )

#     return completion.choices[0].message.content


def call_person_on_messenger(link):
    try:
        # Configure Chrome options to prevent automatic browser closure
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        # Use WebDriverManager to manage ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Open the Messenger chat link
        driver.get(link)

        # Wait for the call button to appear and click it
        call_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Start a voice call']"))
        )
        call_button.click()

        speak("Calling now.")
        print("Calling via Messenger...")
    except Exception as e:
        print(f"Error while calling: {e}")
        speak("I encountered an error. Please try again.")


def process_command(command):
    print(command)
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif "open instagram" in command.lower():
        webbrowser.open("https://instagram.com")
    elif "open github" in command.lower():
        webbrowser.open("https://github.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif command.lower().startswith("play my favourite"):
        video = command.lower().split(" ")[3]
        link = personalLibrary.fav[video]
        webbrowser.open(link)
    elif command.lower().startswith("open my favourite"):
        video = command.lower().split(" ")[3]
        link = personalLibrary.fav[video]
        webbrowser.open(link)
    elif "call" in command.lower():
        person = command.lower().split(" ")[1]
        # Add predefined links to a dictionary
        contacts = {
            "dad": "https://www.facebook.com/messages/e2ee/requests/t/7110356212360208",
            "mom": "https://www.facebook.com/messages/e2ee/requests/t/7110356212360208",
            # Add other contacts as needed
        }
        if person in contacts:
            link = contacts[person]
            call_person_on_messenger(link)
        else:
            speak("I don't have a contact for that person.")
    else:
        speak("Command not recognized.")
   
        # speak("ther is some error")
        # let open ai handle the request
        # output=aiProcess(command)
        # speak(output)


if __name__ == "__main__":
    speak("Initializing jarvis...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for the wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                wake_word = recognizer.recognize_google(audio).lower()

                if wake_word == "jarvis":
                    speak("Yes?")
                    print("Jarvis activated. Listening for your command...")
                    with sr.Microphone() as source:
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio)
                        process_command(command)
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
