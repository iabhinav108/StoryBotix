import os
import re
import tempfile
from moviepy.editor import (
    ImageSequenceClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_audioclips
)
from gtts import gTTS
from moviepy.config import change_settings
import nltk
from nltk.tokenize import sent_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

def sanitize_filename(name):
    return re.sub(r'[^\w\s-]', '', name).strip().replace(" ", "_")

def create_video_from_images(image_root_folder, script_path, output_path, min_duration=30):
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    sanitized_script = sanitize_filename(script_name)

    folders = os.listdir(image_root_folder)
    matched_folder = None
    for folder in folders:
        if sanitize_filename(folder) == sanitized_script:
            matched_folder = os.path.join(image_root_folder, folder)
            break

    if not matched_folder or not os.path.exists(matched_folder):
        print(f"No matching image folder found for script: {script_name}")
        return

    images = sorted([
        os.path.join(matched_folder, f)
        for f in os.listdir(matched_folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ])

    if not images:
        print("No images found in folder:", matched_folder)
        return

    with open(script_path, "r", encoding="utf-8") as f:
        script = f.read().strip()

    sentences = sent_tokenize(script)
    print(f"Script split into {len(sentences)} sentences")

    print("Generating narration audio for each sentence...")
    audio_clips = []
    sentence_durations = []
    temp_files = []
    
    for i, sentence in enumerate(sentences):
        if sentence.strip():
            try:
                tts = gTTS(text=sentence.strip(), lang='en', slow=False)
                temp_audio_path = tempfile.mktemp(suffix=f"_{i}.mp3")
                temp_files.append(temp_audio_path)
                tts.save(temp_audio_path)
                
                audio_clip = AudioFileClip(temp_audio_path)
                original_duration = audio_clip.duration
                
                if i < len(sentences) - 1:
                    from moviepy.editor import AudioClip
                    silence = AudioClip(lambda t: [0,0], duration=0.5, fps=22050)
                    audio_clip = concatenate_audioclips([audio_clip, silence])
                
                audio_clips.append(audio_clip)
                sentence_durations.append(audio_clip.duration)
                print(f"Sentence {i+1}: {audio_clip.duration:.2f}s (original: {original_duration:.2f}s)")
                
            except Exception as e:
                print(f"Error generating audio for sentence {i+1}: {e}")
                continue

    if not audio_clips:
        print("No audio clips generated")
        return

    try:
        full_audio = concatenate_audioclips(audio_clips)
        print(f"Total audio duration: {full_audio.duration:.2f} seconds")
    except Exception as e:
        print(f"Error concatenating audio: {e}")
        return

    num_images = len(images)
    duration_per_image = max(full_audio.duration / num_images, 1.0)
    
    print(f"Creating video with {num_images} images, {duration_per_image:.2f}s per image")

    clip = ImageSequenceClip(images, durations=[duration_per_image] * num_images)
    clip = clip.set_duration(full_audio.duration)
    
    video_with_audio = clip.set_audio(full_audio)
    
    if video_with_audio.audio is None:
        print("WARNING: Audio not attached to video!")
        video_with_audio = CompositeVideoClip([clip]).set_audio(full_audio)

    subtitle_clips = []
    current_time = 0
    
    for i, (sentence, duration) in enumerate(zip(sentences, sentence_durations)):
        if sentence.strip():
            try:
                subtitle_clip = TextClip(
                    sentence.strip(),
                    fontsize=24,
                    color='white',
                    font='Arial-Bold',
                    stroke_color='black',
                    stroke_width=2,
                    method='caption',
                    size=(clip.w - 80, None),
                    align='center'
                ).set_position(('center', 0.85), relative=True).set_start(current_time).set_duration(duration - 0.5)
                
                subtitle_clips.append(subtitle_clip)
                print(f"Subtitle {i+1}: {current_time:.2f}s - {current_time + duration:.2f}s")
                
            except Exception as e:
                print(f"Error creating subtitle {i+1}: {e}")
            
            current_time += duration

    try:
        if subtitle_clips:
            final = CompositeVideoClip([video_with_audio] + subtitle_clips)
            print("Timed subtitles added successfully")
        else:
            final = video_with_audio
            print("No subtitles added")
        
    except Exception as e:
        print(f"Error compositing video: {e}")
        final = video_with_audio

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print("Rendering final video...")
    try:
        final.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac",
            fps=24,
            verbose=False,
            logger=None,
            threads=4,
            preset='medium'
        )
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Video successfully saved to {output_path}")
            print(f"File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
        else:
            print("Video file was not created or is empty")
            
    except Exception as e:
        print(f"Error writing video: {e}")
        print("Trying alternative approach...")
        
        try:
            temp_video_path = output_path.replace('.mp4', '_temp_video.mp4')
            clip.write_videofile(temp_video_path, fps=24, verbose=False, logger=None)
            
            temp_audio_path = output_path.replace('.mp4', '_temp_audio.wav')
            full_audio.write_audiofile(temp_audio_path, verbose=False, logger=None)
            
            import subprocess
            cmd = [
                'ffmpeg', '-y',
                '-i', temp_video_path,
                '-i', temp_audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"Video created using ffmpeg: {output_path}")
                os.remove(temp_video_path)
                os.remove(temp_audio_path)
            else:
                print(f"FFmpeg failed: {result.stderr}")
                
        except Exception as e2:
            print(f"Alternative method failed: {e2}")

    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except:
            pass
    
    try:
        for clip in audio_clips:
            clip.close()
        full_audio.close()
        final.close()
    except Exception as e:
        print(f"Cleanup warning: {e}")
