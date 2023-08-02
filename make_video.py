from moviepy.editor import *
import os
import analyze_audio


def make_clip_from_image(image_file, duration, fps=15):
    clip = ImageClip(image_file, duration=duration).set_fps(fps)
    return clip


def concatenate_clips_one_after_one(clips):
    return concatenate_videoclips(clips, method="compose")


def preview_video(video):
    try:
        video.preview()
    except Exception as e:
        print("Exception in preview")
        print(e)


def make_video_from_images(images, audio_file, duration=15, audio_start=0, min_clip_length=0.1, show_preview=False):
    """Make video from images.
    Extracts the beat from the audio and syncs the images with the audio (using the beat).
    Input:
        images: list of image file names [img1.jpeg, img2.png, ...]
        audio_file: audio file name - string (e.g "song.mp3")
        duration: length of the video in seconds - int
        audio_start: second at which to start syncing the video with - int
        min_clip_length: minimum time of an individual image to be displayed in the final video - float/int
        show_preview: preview the video - bool
    Output:
        moviepy video"""

    beat_timestamps = analyze_audio.get_beat_timestamps(audio_file)
    beat_timestamps = [beat_timestamp - audio_start for beat_timestamp in beat_timestamps if beat_timestamp - audio_start > 0]
    beat_intervals = analyze_audio.get_beat_intervals_greater_than_threshold(beat_timestamps, min_clip_length)
    clips = list(map(lambda image, interval: make_clip_from_image(image, interval), images, beat_intervals))
    video = concatenate_clips_one_after_one(clips)
    video = video.subclip(t_start=0, t_end=duration)
    audio_clip = AudioFileClip(audio_file).subclip(t_start=audio_start, t_end=audio_start + duration)
    video.audio = audio_clip
    if show_preview:
        preview_video(video)
    return video


def get_all_images_from_folder(image_folder):
    return [os.path.join(image_folder, f) for f in os.listdir(image_folder) if
            os.path.isfile(os.path.join(image_folder, f)) and f.endswith(".jpg")]


def save_video(video, filename, mute=True):
    if mute:
        video.write_videofile(filename, audio=False, codec="mpeg4")
    else:
        video.write_videofile(filename, codec="mpeg4")


if __name__ == '__main__':
    images = get_all_images_from_folder(image_folder="images")
    audio = "audio/Bill_Withers_Lovely_Day.mp3"
    video = make_video_from_images(images, audio, audio_start=52, min_clip_length=1, show_preview=False, duration=23)
    save_video(video, filename="videos/reel.mp4", mute=False)
