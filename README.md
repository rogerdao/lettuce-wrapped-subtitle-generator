# Media Subtitle Prototype

Prototype utility for downloading online videos, extracting MP3 audio, and generating SRT subtitles using OpenAI Whisper.

## Requirements

- Python 3.10+
- `ffmpeg` installed and on PATH
- Python dependencies:
  ```bash
  pip install yt-dlp openai-whisper
  ```

## Quick Start

1. Clone the repository and install dependencies.
2. Run the CLI to download a video and generate subtitles:
   ```bash
   python -m code.cli "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --model medium.en
   ```

## CLI Usage

`python -m code.cli [URL] [options]`

Key options:

- `--video-path PATH` reuse an existing video instead of downloading
- `--output-dir DIR` download destination (`downloads` by default)
- `--filename NAME` custom base name for download artifacts
- `--mp3-output PATH` explicit MP3 target
- `--srt-output PATH` explicit SRT target
- `--bitrate 192k` audio bitrate for ffmpeg
- `--model medium.en` Whisper model (`tiny`, `base`, `small`, `medium`, `large`, etc.)
- `--language en` optional language hint
- `--ytdlp-option KEY=VALUE` pass additional yt-dlp overrides (repeatable)

Example using a local video:

```bash
python -m code.cli --video-path downloads/sample.mp4 --language en
```

## Modules

- `code/media_utils.py` – helper functions to download video, convert to MP3, and transcribe to SRT.
- `code/cli.py` – command-line wrapper orchestrating the full pipeline.

## Notes

- Ensure enough disk space for large downloads.
- Whisper model selection impacts accuracy and runtime; larger models are slower but generally more accurate.
- The project is a learning prototype; hardening (e.g., retries, resumable downloads) is out of scope.

