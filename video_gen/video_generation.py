from moviepy import TextClip, CompositeVideoClip, ColorClip, AudioFileClip, VideoFileClip  
from video_gen.create_subtitles import transcribe_mp3, split_srt_lines
import pysrt

def generate_video(comments, show_screenshots, video_size=(1080, 1920), font_size=48, font_color="White", font="C:/Windows/Fonts/Comic.ttf"):
    transcribe_mp3("./data/audio/pytts_full_script.mp3", "pytts_full_script")
    split_srt_lines("./data/subtitles/pytts_full_script.srt", "./data/subtitles/pytts_full_script.srt", max_words=4)

    subtitles = pysrt.open("./data/subtitles/pytts_full_script.srt")
    video_clips = []
    for line in subtitles:
        start = line.start.ordinal / 1000
        end = line.end.ordinal / 1000
        duration = end - start

        # Only pass font if method is not 'caption'
        text_clip = TextClip(
            font=font,
            text=line.text,
            font_size=font_size,
            color=font_color,
            size=(video_size[0] - 100, None),
            method="caption",
            text_align="center"
        ).with_start(start).with_duration(duration).with_position("center")
        video_clips.append(text_clip)


    # Create a black background
    bg = VideoFileClip("./data/backgrounds/videoplayback.mp4").subclipped(0, 30).resized(video_size)
    
    # Setup Audio
    audio = AudioFileClip("./data/audio/pytts_full_script.mp3").subclipped(0, 30)

    # Final Composite
    final = CompositeVideoClip([bg] + video_clips, size=video_size).with_audio(audio)
    final = final.subclipped(0, 10)
    final.write_videofile("./data/video/subtitles_only.mov", codec="libx264", audio_codec="aac", fps=24)

    if show_screenshots:
        for idx, _ in enumerate(comments):
            filepath = f"./data/audio/pytts_comment_{idx}.mp3"
            filename = f"pytts_comment_{idx}.mp3"
            transcribe_mp3(filepath, filename)

#generate_video([1, 2, 3, 4, 5], False)