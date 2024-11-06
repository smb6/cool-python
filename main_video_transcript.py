import speech_recognition as sr
import moviepy.editor as mp

# Load the video file
video_path = ("/Users/pabloc/tmp/video_to_spanish.mp4")

# Extract audio from video
clip = mp.VideoFileClip(video_path)
audio_path = "/Users/pabloc/tmp/video_to_spanish.wav"
clip.audio.write_audiofile(audio_path)

# Transcribe audio
recognizer = sr.Recognizer()

# Load audio file for transcription
with sr.AudioFile(audio_path) as source:
    audio = recognizer.record(source)

# Attempt transcription
try:
    transcription = recognizer.recognize_google(audio, language="es-ES")  # Assuming Spanish audio
except sr.UnknownValueError:
    transcription = "Audio not clear enough for transcription."
except sr.RequestError:
    transcription = "Could not request results from the transcription service."

