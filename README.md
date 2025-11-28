# Media Subtitle Prototype - Thanksgiving project

Prototype utility for downloading online videos, extracting MP3 audio, and generating SRT subtitles using OpenAI Whisper.
The project is a learning prototype; hardening (e.g., retries, resumable downloads) is out of scope.

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
- w11, wsl ubuntu cuda drivers, for your convienence.
  ```bash
  windows 11:
  https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local
  
  wsl ubuntu:
  https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_local
  
  test:
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
- cuDNN
  ```bash
  https://developer.nvidia.com/cudnn
  
  on w11: add the cuDNN bin folder path to the path variable in environment variables if you're not using an installer.
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
- For non-English subtitling: accuracy is unacceptable when not using the large model.

   runs `medium.en` by default for English subtitles (--model medium.en)
   ```bash
   python -m code.cli "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   ```

   non-English videos: be sure to specify using the `large` model. 
   ```bash
   python -m code.cli "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --model large
   ```

   example using a local video:
   ```bash
   python -m code.cli --video-path downloads/sample.mp4 --language en
   ```
   
3. Play the video back using any video player of your choice and the generated SRT file.

## CLI Usage

`python code.cli URL [options]`

Key options:

- `--video-path PATH` choose an existing video instead of downloading
- `--mp3-output PATH` explicit MP3 target
- `--srt-output PATH` explicit SRT target

- `--output-dir DIR` download destination (`downloads` by default)
- `--filename NAME` custom base name for download artifacts

- `--ytdlp-option KEY=VALUE` pass additional yt-dlp overrides (repeatable)
- `--bitrate 192k` audio bitrate for ffmpeg

- `--model medium.en` Whisper model (`medium`, `large`, `turbo` etc.)
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
Subtitle step would take quarter time. (200 + 45 + 150s subtitle)
```


