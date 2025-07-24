import pyttsx3
import pandas as pd

def create_tts_subtitles(title, description, comments, show_screenshots):
    # Initialize pyttsx3 engine
    engine = pyttsx3.init()

    # Set voice
    voices = engine.getProperty('voices')
    for voice in voices:
        if "male" in voice.name.lower() or "david" in voice.name.lower() or "alex" in voice.name.lower():
            male_voice_id = voice.id
            break

    # Rate and volume
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 0.9)

    # Merge Post and Comments
    if show_screenshots:
        # Future Update...
        print("Show screenshots is currently not available...")
        # Generate audio files for each row (Old Code, Only Used for multiple audio files)
        for idx, text in enumerate(comments):

            filename = f"./data/audio/pytts_comment_{idx}.mp3"
            
            # Save to file
            engine.save_to_file(text, filename)
            print(f"Saved {filename}")
        
        title_description =  " ".join([title, description])
        engine.save_to_file(title_description, "./data/audio/pytts_full_script.mp3")
        
    else:
        comment_str = " ".join(x for _, x in comments)
        full_script = " ".join([title, description, comment_str])

        #print(full_script)

        # Make audio files for title and description
        engine.save_to_file(full_script, "./data/audio/pytts_full_script.mp3")

    # Finalize the engine
    engine.runAndWait()