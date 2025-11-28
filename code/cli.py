from __future__ import annotations

import argparse
import sys
from pathlib import Path

from media_utils import (
    convert_video_to_mp3,
    download_video,
    transcribe_mp3_to_srt,
)

MAX_YTDLP_OPTIONS = 16


def _ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download a video, extract MP3 audio, and create SRT subtitles."
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="Video URL supported by yt-dlp (omit if providing --video-path).",
    )
    parser.add_argument(
        "--video-path",
        type=Path,
        help="Existing video file to reuse instead of downloading.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("downloads"),
        help="Directory to store downloaded videos (default: downloads).",
    )
    parser.add_argument(
        "--filename",
        help="Base filename (without extension) to use for downloads.",
    )
    parser.add_argument(
        "--mp3-output",
        type=Path,
        help="Optional path for the generated MP3 (defaults to video filename with .mp3).",
    )
    parser.add_argument(
        "--srt-output",
        type=Path,
        help="Optional path for the generated SRT (defaults to MP3 filename with .srt).",
    )
    parser.add_argument(
        "--bitrate",
        default="192k",
        help="Audio bitrate passed to ffmpeg (default: 192k).",
    )
    parser.add_argument(
        "--model",
        default="medium.en",
        help="Whisper model size (tiny, base, small, medium, large). Default: medium.en.",
    )
    parser.add_argument(
        "--language",
        help="Optional ISO language code hint for Whisper transcription.",
    )
    parser.add_argument(
        "--ytdlp-option",
        action="append",
        metavar="KEY=VALUE",
        help="Extra yt-dlp option overrides (can be repeated). Example: --ytdlp-option format=bestvideo",
    )
    return parser.parse_args(argv)


def parse_ytdlp_overrides(pairs: list[str] | None) -> dict:
    if not pairs:
        return {}
    _ensure(len(pairs) <= MAX_YTDLP_OPTIONS, "Too many yt-dlp overrides provided.")
    overrides: dict = {}
    for idx in range(MAX_YTDLP_OPTIONS):
        if idx >= len(pairs):
            break
        pair = pairs[idx]
        if "=" not in pair:
            raise ValueError(f"Invalid yt-dlp option '{pair}'. Use KEY=VALUE format.")
        key, value = pair.split("=", 1)
        overrides[key.strip()] = value.strip()
    _ensure(len(overrides) == len(pairs), "Duplicate yt-dlp override keys detected.")
    return overrides


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    _ensure(isinstance(args, argparse.Namespace), "Argument parsing failed.")

    if not args.video_path and not args.url:
        raise SystemExit("Either a URL or --video-path must be provided.")

    video_path: Path
    if args.video_path:
        video_path = args.video_path
        if not video_path.exists():
            raise SystemExit(f"Provided video file does not exist: {video_path}")
    else:
        overrides = parse_ytdlp_overrides(args.ytdlp_option)
        video_path = download_video(
            args.url,
            output_dir=args.output_dir,
            filename=args.filename,
            ytdlp_options=overrides or None,
        )
        print(f"Downloaded video to: {video_path}")

    mp3_path = convert_video_to_mp3(
        video_path=video_path,
        output_path=args.mp3_output,
        bitrate=args.bitrate,
    )
    print(f"Converted audio to MP3: {mp3_path}")

    srt_path = transcribe_mp3_to_srt(
        audio_path=mp3_path,
        output_path=args.srt_output,
        model_name=args.model,
        language=args.language,
    )
    print(f"Created subtitles: {srt_path}")

    _ensure(video_path.exists(), "Video path must still exist after processing.")
    _ensure(mp3_path.exists() and srt_path.exists(), "Artifacts missing after completion.")
    print("\nAll steps completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

