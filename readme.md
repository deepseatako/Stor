# Srtor

## Overview

`Srtor` is a tool designed for processing subtitles and video transcription. It provides functionality for:

- Recognizing speech from videos and generating `.srt` subtitle files using OpenAI's Whisper model.
- Translating subtitle files (`.srt`) from English to Chinese using Google Translate.

## Features

- **Speech Recognition**: Extracts spoken text from video files and outputs it as a subtitle file (`.srt`).
- **Subtitle Translation**: Translates English subtitles into Chinese while preserving timestamps.
- **Batch Processing**: Processes all subtitle or video files in a given folder.
- **Error Handling**: Implements retry mechanisms to handle network issues during translation.

## Dependencies

The project requires the following Python libraries:

- `pysrt`
- `googletrans`
- `tqdm`
- `whisper`
- `argparse`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd srtor
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Speech Recognition

To transcribe speech from video files and generate subtitles:

```bash
python srtor_whisper.py -p <folder_path>
```

- `<folder_path>`: Path to the folder containing video files (`.mp4`, `.mkv`).

### 2. Subtitle Translation

To translate existing `.srt` subtitle files from English to Chinese:

```bash
python srtor_googletrans.py -p <folder_path>
```

- `<folder_path>`: Path to the folder containing `.srt` subtitle files.

## Notes

- The speech recognition model used is `base` from OpenAI Whisper.
- The translation is powered by Google Translate, and network issues may cause occasional failures.
- Ensure the video and subtitle files are in supported formats (`.mp4`, `.mkv`, `.srt`).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
