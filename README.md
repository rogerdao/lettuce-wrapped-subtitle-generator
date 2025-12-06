# Media Subtitle Prototype - Thanksgiving weekend project

Presented on 12/5 at AI Club @ SDSU
https://docs.google.com/presentation/d/1jImkubl8rhaT4OiMCtalAMdsbXoVy3KNKOZpCp_N6_8/edit?slide=id.g3ae2df02bb3_0_0#slide=id.g3ae2df02bb3_0_0

Prototype utility for downloading online videos, extracting MP3 audio, and generating SRT subtitles using OpenAI Whisper.

The project is a learning prototype; hardening (e.g., retries, resumable downloads) is out of scope.

Runs using CUDA by default.
Uses audio to generate subtitles.

The program is an end-to-end system, 
- Supports transcription and generation of subtitles for both English and non-English videos.
- Supports downloaded videos, and URL of videos.
- Can be used for adjacent applications, such as downloading a video, keeping in mind YouTube's compressed audio bitrate, and specifying a audio bitrate suitable to preserve file storage on a local .mp3 playback device

## Requirements

- Python 3.10+
- `ffmpeg` installed and on PATH
  ```bash
  sudo apt install ffmpeg
  
  w11 on powershell with winget: (or use an installer)
  winget install Gyan.FFmpeg
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
- get CUDA toolkit corresponding to CUDA
  ```bash
  https://developer.nvidia.com/cuda-toolkit-archive
  ```
- get cuDNN corresponding to CUDA
  ```bash
  https://developer.nvidia.com/cudnn
  for w11: bin folder on PATH if not using installer
  ```
- get pytorch version corresponding to CUDA
  ```bash
  https://pytorch.org/get-started/locally/

  verify the above, in python:
  import torch
  print(torch.__version__)
  print(torch.cuda.is_available())
  ```  
  

## Quick Start

1. Clone the repository and install dependencies.
2. Run the CLI to download a video and generate subtitles:
   example commands provided below.

- Whisper model selection impacts accuracy and runtime; larger models are slower but generally more accurate.
- For non-English subtitling: accuracy is unacceptable when not using the `large` model
- Be sure to specifiy translation if desired, hint is optional.

   runs `medium.en` (I think) by default (use `--model turbo` for faster speeds for English transcription)
   ```bash
   python cli.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   ```

   non-English videos to English: be sure to specify using the `large` model, as well as translate flag.
   language hint is optional.
   ```bash
   python cli.py "https://youtu.be/MwP4gqRys4c" --model large --translate --language ja
   ```

   example using a local video:
   the program will warn you when you are not using `large` model for translation.
   ```bash
   python cli.py --video-path downloads/sample.mp4 --language en
   ```
   
3. Play the video back using any video player of your choice and the generated SRT file.

## CLI Usage

`python cli.py URL [options]`

Key options:

- `--video-path PATH` select an existing video as input instead of downloading
- `--srt-output PATH` explicit SRT target (good to use with above if local video is not in downloads folder)
- `--filename NAME` custom base name for download artifacts (renames the downloaded video, audio file, subtitle file)

- `--model medium.en` Whisper model (`medium`, `large`, `turbo` etc.)
- `--translate` force Whisper translate task (English subtitles; requires multilingual model)
- `--language en` optional language hint
  
- `--mp3-output PATH` explicit MP3 target (to transcibe local mp3 audio -> for whisper to transcribe)
- `--bitrate 192k` audio bitrate for ffmpeg (if you want to specify the bitrate, i.e keep the MP3 from a video for your own use)
- `--output-dir DIR` download destination (`downloads` by default)

- `--ytdlp-option KEY=VALUE` pass additional yt-dlp overrides (repeatable)

## Modules

- `code/media_utils.py` – helper functions to download video, convert to MP3, and transcribe to SRT.
- `code/cli.py` – command-line wrapper orchestrating the full pipeline.

## Notes

- Trial run: (correct times this time)

```bash
for a 46 minute video

~200s for download 1500mb @ 7.5MBps (cox fiber and Wi-Fi)

~45 seconds to split a 46 minute video
.webm -> .mp3 + .mp4

~400s seconds (6:39) For subtitle generation step
.mp3 -> .srt

Total: (200s + 45s + 400s) = ~10.75min

We used `medium.en` as a relative time benchmark
For non-English, we MUST use `large` otherwise accuracy is unusable
For English, turbo has similar demands as medium.en, but accuracy closer to large (better) 

If we use the `large` model, 	~17.50min (done in under 40% of runtime)
The subtitle time would roughly double. (200 + 45 + 800s subtitle)

If we use the `turbo` model, 	~5.75min (done in under 15% of runtime)
Subtitle step would take quarter time. (200 + 45 + 100s subtitle)
```

- Anime episode: large model only,
```bash
just look at times for large and nothing else
```
  


