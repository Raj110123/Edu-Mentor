# import speech_recognition as sr
# from elevenlabs.client import ElevenLabs
# from elevenlabs import play

# # Initialize ElevenLabs
# client = ElevenLabs(api_key="sk_b149788c0cdae82c16a93007017574ebf5e10bccb50d056c")

# # Speech recognizer
# r = sr.Recognizer()

# with sr.Microphone() as source:
#     print("Adjusting microphone...")
#     r.adjust_for_ambient_noise(source, duration=1)

#     print("Speak now...")
#     audio = r.listen(source, phrase_time_limit=5)

# # Convert speech to text
# text = r.recognize_google(audio)

# print("You said:", text)

# # Convert text to speech (slower and clearer)
# audio_response = client.text_to_speech.convert(
#     voice_id="21m00Tcm4TlvDq8ikWAM",
#     text=text,
#     voice_settings={
#         "stability": 0.5,
#         "similarity_boost": 0.8,
#         "style": 0.0,
#         "use_speaker_boost": True,
#         "speed": 0.7   # slower voice
#     }
# )

# # Play the response
# play.play(audio_response)

import speech_recognition as sr
from elevenlabs.client import ElevenLabs
from elevenlabs import play

# Initialize ElevenLabs
client = ElevenLabs(api_key="sk_b149788c0cdae82c16a93007017574ebf5e10bccb50d056c")

# Speech recognizer
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Adjusting microphone...")
    r.adjust_for_ambient_noise(source, duration=1)
    print("Speak now...")
    audio = r.listen(source, phrase_time_limit=5)

# Convert speech to text
try:
    text = r.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Could not understand audio. Please speak clearly and try again.")
    exit()
except sr.RequestError as e:
    print(f"Could not connect to Google Speech API: {e}")
    exit()

# Convert text to speech
audio_response = client.text_to_speech.convert(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    text=text,
    voice_settings={
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.0,
        "use_speaker_boost": True,
        "speed": 0.7
    }
)

# Play the response
play(audio_response)