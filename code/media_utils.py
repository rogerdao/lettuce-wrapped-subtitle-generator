from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Optional

import whisper
from whisper.utils import write_srt
from yt_dlp import YoutubeDL


def _ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def download_video(
    url: str,
    output_dir: str | Path = "downloads",
    filename: Optional[str] = None,
    ytdlp_options: Optional[dict] = None,
) -> Path:
    """
    Download a video using yt-dlp and return the local file path.

    Args:
        url: Video URL supported by yt-dlp.
        output_dir: Directory where the video will be stored.
        filename: Optional base filename (without extension). Defaults to yt-dlp template.
        ytdlp_options: Optional overrides passed directly to YoutubeDL.
    """
    _ensure(isinstance(url, str) and url.strip(), "A non-empty URL is required.")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    _ensure(output_path.exists(), "Output directory must exist after creation.")

    outtmpl = str(output_path / (filename or "%(title)s.%(ext)s"))
    opts = {
        "outtmpl": outtmpl,
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": False,
    }
    if ytdlp_options:
        opts.update(ytdlp_options)

    with YoutubeDL(opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        if info_dict is None:
            raise RuntimeError(f"yt-dlp failed to download url: {url}")
        filepath = ydl.prepare_filename(info_dict)

    file_path_obj = Path(filepath)
    _ensure(file_path_obj.exists(), "Downloaded file was not created.")
    return file_path_obj


def convert_video_to_mp3(
    video_path: str | Path,
    output_path: Optional[str | Path] = None,
    bitrate: str = "192k",
) -> Path:
    """
    Convert a video file to MP3 using ffmpeg.

    Args:
        video_path: Path to the downloaded video file.
        output_path: Optional path for the resulting MP3 file.
        bitrate: Audio bitrate passed to ffmpeg.
    """
    _ensure(isinstance(bitrate, str) and bitrate.endswith("k"), "Bitrate must end with 'k'.")
    video = Path(video_path)
    if not video.exists():
        raise FileNotFoundError(f"Video file not found: {video}")
    _ensure(video.suffix.lower() != ".mp3", "Source video must not already be an MP3.")

    if output_path is None:
        output_path = video.with_suffix(".mp3")
    audio = Path(output_path)
    audio.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video),
        "-vn",
        "-acodec",
        "libmp3lame",
        "-ab",
        bitrate,
        str(audio),
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        error_details = json.dumps(
            {"stdout": result.stdout, "stderr": result.stderr},
            ensure_ascii=False,
            indent=2,
        )
        raise RuntimeError(
            "ffmpeg failed to convert video to mp3:\n"
            f"{error_details}"
        )

    _ensure(audio.exists(), "MP3 conversion reported success but file is missing.")
    return audio


def transcribe_mp3_to_srt(
    audio_path: str | Path,
    output_path: Optional[str | Path] = None,
    model_name: str = "small",
    language: Optional[str] = None,
) -> Path:
    """
    Generate an SRT subtitle file from an MP3 using OpenAI Whisper.

    Args:
        audio_path: Path to the MP3 file.
        output_path: Optional path for the resulting SRT file.
        model_name: Whisper model to load (e.g., tiny, base, small, medium, large).
        language: Optional ISO language code hint for Whisper.
    """
    _ensure(isinstance(model_name, str) and model_name.strip(), "Model name must be provided.")
    audio = Path(audio_path)
    if not audio.exists():
        raise FileNotFoundError(f"Audio file not found: {audio}")
    _ensure(audio.suffix.lower() == ".mp3", "Transcription source must be an MP3.")

    if output_path is None:
        output_path = audio.with_suffix(".srt")
    srt_path = Path(output_path)
    srt_path.parent.mkdir(parents=True, exist_ok=True)

    model = whisper.load_model(model_name)
    result = model.transcribe(str(audio), language=language)

    with srt_path.open("w", encoding="utf-8") as outfile:
        write_srt(result, file=outfile)

    _ensure(srt_path.exists(), "SRT file must exist after writing.")
    return srt_path

