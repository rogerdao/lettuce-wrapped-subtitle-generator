# Media Subtitle Prototype - Thanksgiving project

Prototype utility for downloading online videos, extracting MP3 audio, and generating SRT subtitles using OpenAI Whisper.

The project is a learning prototype; hardening (e.g., retries, resumable downloads) is out of scope.

Runs using CUDA by default.
Uses audio to generate subtitles.

Supports transcription and generation of subtitles for both English and non-English videos.
Supports downloaded videos, and URL of videos.

## Requirements

- Python 3.10+
- `ffmpeg` installed and on PATH
  ```bash
  sudo apt install ffmpeg
  ```
- Python dependencies:
  ```bash
  pip install yt-dlp openai-whisper
  ```
- w11, wsl ubuntu CUDA drivers, for your convenience.
  ```bash
  windows 11:
  https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local
  
  wsl ubuntu:
  https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_local
  
  verify:
  nvcc --version
  ```
- CUDA compute capability:
  ```bash
  https://en.wikipedia.org/wiki/CUDA#GPUs_supported
  ```
- CUDA toolkit
  ```bash
  https://developer.nvidia.com/cuda-toolkit-archive
  ```
- cuDNN, w11: bin folder on PATH if not using installer
  ```bash
  https://developer.nvidia.com/cudnn
  ```
- get pytorch version corresponding to CUDA
  ```bash
  https://pytorch.org/get-started/locally/

  verify in python:
  import torch
  print(torch.__version__)
  print(torch.cuda.is_available())
  ```  
  

## Quick Start

1. Clone the repository and install dependencies.
2. Run the CLI to download a video and generate subtitles:

- Whisper model selection impacts accuracy and runtime; larger models are slower but generally more accurate.
- For non-English subtitling: accuracy is unacceptable when not using the `large` model
- Be sure to specifiy translation if desired, hint is optional.

   runs `medium.en` by default
   ```bash
   python cli.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   ```

   non-English videos to English: be sure to specify using the `large` model, as well as translate flag.
   language hint is optional.
   ```bash
   python cli.py "https://youtu.be/MwP4gqRys4c" --model large --translate --language ja
   ```

   example using a local video:
   ```bash
   python cli.py --video-path downloads/sample.mp4 --language en
   ```
   
3. Play the video back using any video player of your choice and the generated SRT file.

## CLI Usage

`python cli.py URL [options]`

Key options:

- `--video-path PATH` select an existing video as input instead of downloading
- `--bitrate 192k` audio bitrate for ffmpeg
- `--ytdlp-option KEY=VALUE` pass additional yt-dlp overrides (repeatable)
  
- `--output-dir DIR` download destination (`downloads` by default)
- `--filename NAME` custom base name for download artifacts
- `--mp3-output PATH` explicit MP3 target
- `--srt-output PATH` explicit SRT target 

- `--model medium.en` Whisper model (`medium`, `large`, `turbo` etc.)
- `--translate` force Whisper translate task (English subtitles; requires multilingual model)
- `--language en` optional language hint

## Modules

- `code/media_utils.py` – helper functions to download video, convert to MP3, and transcribe to SRT.
- `code/cli.py` – command-line wrapper orchestrating the full pipeline.

## Notes

- Trial run:

```bash
for a 46 minute video

~200s for download 1500mb @ 7.5MBps (cox fiber and Wi-Fi)

~45 seconds to split a 46 minute video
.webm -> .mp3 + .mp4

~600 seconds (5:39) For subtitle generation step
.mp3 -> .srt

Total: (200s + 45s + 600s) = ~14min

We used `medium.en` as a relative time benchmark
For non-english, we MUST use `large` otherwise accuracy is unusable

If we use the `large` model, 	~24min
The subtitle time would roughly double. (200 + 45 + 1200s subtitle)

If we use the `turbo` model, 	~7min
Subtitling step would take quarter time. (200 + 45 + 150s subtitle)
```


