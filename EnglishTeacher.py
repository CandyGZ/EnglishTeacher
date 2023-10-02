# BE SURE TO ADD YOU CAHTGPT API ON LINE 15 !!

import openai
import os
import pyaudio
import wave
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS

# from chatgpt_bot import Conversation

# future Update: add pocketsphinx for speech recognition

openai.api_key = "YOUR API"


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


def check_grammar():
    with open("C:\DataScience\Python\EnglishTeacher\englishClass.txt", "r") as file:
        conversacion_anterior = file.read()

    print("Revisando Gramática y generando consejos para mejorar")
    prompt = f"""
    "check grammar of this text, what kind of errors do you see when user responds, make observations about it to help the user to improve and be natual talking in english.
    Review only should be made from text from user and not teacher". 
    {conversacion_anterior}" 
    """

    respuesta = chat_with_gpt(prompt)
    # Guarda la respuesta en un archivo o imprímela según tu preferencia
    with open("C:\DataScience\Python\EnglishTeacher\correcciones.txt", "w") as file:
        file.write(respuesta)

    text_to_speech(respuesta, "corrections.mp3")
    print(respuesta)


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
# conversacion_anterior = ""
# prompt_voz = get_voice_input()

while True:
    #     # Obtén la respuesta del usuario por voz
    #     if conversacion_anterior == "":
    #         prompt = f"""
    #         "Say hello, invent a name for you and make a very short presentation of yourself as an english teacher, ask my name."
    #         """
    #         respuesta = chat_with_gpt(prompt)
    #         conversacion_anterior += f"Usuario: {prompt_voz}\n"

    print("Habla para continuar la conversación o escribe 'bye' para terminar.")
    with open("C:\DataScience\Python\EnglishTeacher\englishClass.txt", "r") as file:
        conversacion_anterior = file.read()
    prompt_voz = get_voice_input()

    # Si se pudo obtener un prompt por voz, continuar
    if prompt_voz:
        conversacion_anterior += f"Usuario: {prompt_voz}\n"

        prompt = f"""
        "I would like you to serve as my spoken English tutor and improvement guide. I will converse with you in English, 
        and you will respond in English to help me enhance my spoken language skills. Please ensure your responses are concise, 
        limiting them to 40 words. Your primary task is to correct any grammar mistakes, typos, and factual errors in my speech. 
        Additionally, include only a one short question in your replys. I´m a beggineer english learner so start with basics. Let's begin our practice session; 
        you can initiate by asking me a question. 
        We will commence with personal inquiries and gradually transition to professional and job interview-related questions.
        Dont say hi or salute more than once". 
        
        
        "{prompt_voz}"
        {conversacion_anterior}" 
        """
        if prompt_voz == "bye":  # Lets get out of chat by voice
            print("Hasta luego. Conversación finalizada.")
            check_grammar()
            break

        # if prompt_voz == "Check grammar":  # Lets get out of chat by voice
        #     print("Revisando plática. Conversación finalizada.")
        #     check_grammar()

        respuesta = chat_with_gpt(prompt)
        conversacion_anterior += f"Teacher: {respuesta}\n"
        with open(
            "C:\DataScience\Python\EnglishTeacher\englishClass.txt", "a"
        ) as file:  # No es necesario pero genera archivo para estudiar conversación escrita
            file.write(f"Usuario: {prompt_voz}\n")
            file.write(f"Teacher: {respuesta}\n")

        print(respuesta)
        text_to_speech(respuesta, "respuesta.mp3")

    if prompt_voz.lower() == "bye":
        # Si el usuario escribe "bye", termina la conversación
        print("Hasta luego. Conversación finalizada.")
        break
