import openai
import os
import pyaudio
import wave
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
from chatgpt_bot import Conversation

openai.api_key = "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"


def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=400,
        temperature=0.3,
    )
    # para eliminar el audio en blanco de mi recopilación según entiendo
    return response.choices[0].text.strip()


# Configuración de reconocimiento de voz
recognizer = sr.Recognizer()
microphone = sr.Microphone()


def record_audio(filename):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    frames = []

    print("Habla y mantén presionado el botón. Cuando termines click CTRL-C")

    while True:
        try:
            data = stream.read(CHUNK)
            frames.append(data)
        except KeyboardInterrupt:
            break

    print("Grabación finalizada.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()


def text_to_speech(text, output_file):
    tts = gTTS(text, lang="en", slow=False, tld="com", lang_check=False)
    tts.save(output_file)
    os.system(f"start {output_file}")


# Obtener el prompt por voz
def get_voice_input():
    record_audio("user_input.wav")
    with sr.AudioFile("user_input.wav") as source:
        try:
            user_input = recognizer.record(source)
            print("Transcribiendo audio...")
            user_input_text = recognizer.recognize_google(user_input, language="en-EN")
            print(f"Has dicho: {user_input_text}")
            return user_input_text
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
            return ""
        except sr.RequestError:
            print("Error al realizar la solicitud de reconocimiento de voz.")
            return ""


# Obtén el prompt por voz
# prompt_voz = get_voice_input()
# Bucle para mantener la conversación
while True:
    # Obtén la respuesta del usuario por voz
    print("Habla para continuar la conversación o escribe 'bye' para terminar.")
    prompt_voz = get_voice_input()

    if prompt_voz.lower() == "bye":
        # Si el usuario escribe "bye", termina la conversación
        print("Hasta luego. Conversación finalizada.")
        break


# Si se pudo obtener un prompt por voz, continuar
if prompt_voz:
    prompt = f"""
    "I would like you to serve as my spoken English tutor and improvement guide. I will converse with you in English, 
    and you will respond in English to help me enhance my spoken language skills. Please ensure your responses are concise, 
    limiting them to 70 words. Your primary task is to correct any grammar mistakes, typos, and factual errors in my speech. 
    Additionally, include a short question in your reply. I´m a beggineer english learner so start with basics. Let's begin our practice session; you can initiate by asking me a question. 
    We will commence with personal 
    inquiries and gradually transition to professional and job interview-related questions.
    Make the conversation feel more like a friend than a teacher" 
    
    "{prompt_voz}"
    """
    respuesta = chat_with_gpt(prompt)
    print(respuesta)
    text_to_speech(respuesta, "respuesta.mp3")
