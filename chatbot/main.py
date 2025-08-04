import speech_recognition as sr
import pyttsx3
import openai  # <-- Official OpenAI SDK

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Set voice properties
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', voices[0].id)
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 1.0)

# Set your OpenAI API key
openai.api_key = ""
def speak(text):
    print(f"Assistant: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

def get_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful and friendly voice assistant."},
                {"role": "user", "content": user_input},
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("API Error:", e)
        return "Sorry, there was an issue getting my response."

def main():
    mic_list = sr.Microphone.list_microphone_names()
    print("Available microphones:")
    for i, mic_name in enumerate(mic_list):
        print(f"{i}: {mic_name}")
    
    try:
        mic_index = int(input("Enter the microphone index: "))
        mic = sr.Microphone(device_index=mic_index)
    except (ValueError, IndexError):
        print("Invalid mic index. Using default microphone.")
        mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        speak("Hello! I'm your assistant. You can talk to me. Say 'exit' to stop.")

        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                user_input = recognizer.recognize_google(audio)
                print(f"You said: {user_input}")

                if user_input.lower() in ["exit", "quit", "bye"]:
                    speak("Goodbye! Have a great day.")
                    break

                response = get_response(user_input)
                speak(response)

            except sr.WaitTimeoutError:
                speak("I didn’t hear anything. Please try again.")
            except sr.UnknownValueError:
                speak("Sorry, I didn’t catch that. Can you repeat?")
            except sr.RequestError as e:
                speak("I’m having trouble with the speech service.")
            except KeyboardInterrupt:
                speak("Goodbye!")
                break

if __name__ == "__main__":
    main()
