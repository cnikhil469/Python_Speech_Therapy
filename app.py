from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from gtts import gTTS
from pydub import AudioSegment
import os
import time

app = Flask(__name__)

recordings_folder = "static"
os.makedirs(recordings_folder, exist_ok=True)

def cleanup_old_files():
    files = os.listdir(recordings_folder)
    for file in files:
        if file.startswith("word_") or file == "user_recording.wav":
            file_path = os.path.join(recordings_folder, file)
            os.remove(file_path)
            print(f"Deleted old file: {file_path}")

@app.route("/", methods=["GET", "POST"])
def index():
    word = request.args.get('word', '')
    file_name = request.args.get('file_name', '')

    if request.method == "POST":
        cleanup_old_files()

        if "word" in request.form:
            word = request.form["word"]
            if word:  
                timestamp = str(int(time.time()))
                file_name = f"word_{timestamp}.mp3"
                file_path = os.path.join(recordings_folder, file_name)
                
                tts = gTTS(text=word, lang='en')
                tts.save(file_path)
                print(f"Generated speech for the word: {word}, saved at: {file_path}")

        elif "audio" in request.files:
            audio = request.files["audio"]
            audio_path = os.path.join(recordings_folder, "user_recording.webm")
            audio.save(audio_path)
            sound = AudioSegment.from_file(audio_path, format="webm")
            wav_path = os.path.join(recordings_folder, "user_recording.wav")
            sound.export(wav_path, format="wav")
            print(f"Uploaded audio saved as: {wav_path}")

        return redirect(url_for("index", file_name=file_name, word=word))

    return render_template("index.html", file_name=file_name, word=word)

@app.route('/play/<filename>')
def play(filename):
    return send_from_directory(recordings_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
