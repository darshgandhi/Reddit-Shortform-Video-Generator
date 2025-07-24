import assemblyai as aai
import os
import re
from dotenv import load_dotenv

load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def transcribe_mp3(filepath, filename):
    transcript = aai.Transcriber().transcribe(filepath)
    subtitles = transcript.export_subtitles_srt()

    with open(f"./data/subtitles/{filename}.srt", "w") as out:
        out.write(subtitles)

def split_srt_lines(input_path, output_path, max_words=3):
    def time_to_seconds(t):
        h, m, s, ms = re.split('[:,]', t)
        return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000

    def seconds_to_time(s):
        h = int(s // 3600)
        m = int((s % 3600) // 60)
        sec = s % 60
        ms = int((sec - int(sec)) * 1000)
        return f"{h:02}:{m:02}:{int(sec):02},{ms:03}"

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"\n\s*\n", content.strip())
    new_blocks = []
    idx = 1

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        times = lines[1]
        text = " ".join(lines[2:])
        start, end = times.split(" --> ")
        start_sec = time_to_seconds(start)
        end_sec = time_to_seconds(end)
        words = text.split()
        n_chunks = (len(words) + max_words - 1) // max_words
        chunk_duration = (end_sec - start_sec) / n_chunks

        for i in range(n_chunks):
            chunk_words = words[i*max_words:(i+1)*max_words]
            chunk_text = " ".join(chunk_words)
            chunk_start = start_sec + i * chunk_duration
            chunk_end = chunk_start + chunk_duration
            new_blocks.append(
                f"{idx}\n{seconds_to_time(chunk_start)} --> {seconds_to_time(chunk_end)}\n{chunk_text}\n"
            )
            idx += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_blocks))

split_srt_lines("./data/subtitles/pytts_full_script.srt", "./data/subtitles/pytts_full_script_short.srt", max_words=3)