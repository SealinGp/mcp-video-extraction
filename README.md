# MCP Video & Audio Text Extraction Server

An MCP server that provides text extraction capabilities from various video platforms and audio files. This server implements the Model Context Protocol (MCP) to provide standardized access to audio transcription services.

## Supported Platforms

This service supports downloading videos and extracting audio from various platforms, including but not limited to:

- YouTube
- Bilibili
- TikTok
- Instagram
- Twitter/X
- Facebook
- Vimeo
- Dailymotion
- SoundCloud

For a complete list of supported platforms, please visit [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Core Technology

This project utilizes OpenAI's Whisper model for audio-to-text processing through MCP tools. The server exposes four main tools:

1. Video download: Download videos from supported platforms
2. Audio download: Extract audio from videos on supported platforms
3. Video text extraction: Extract text from videos (download and transcribe)
4. Audio file text extraction: Extract text from audio files

### MCP Integration

This server is built using the Model Context Protocol, which provides:
- Standardized way to expose tools to LLMs
- Secure access to video content and audio files
- Integration with MCP clients like Claude Desktop

## Features

- High-quality speech recognition based on Whisper
- Multi-language text recognition
- Support for various audio formats (mp3, wav, m4a, etc.)
- MCP-compliant tools interface
- Asynchronous processing for large files

## Tech Stack

- Python 3.9+
- Model Context Protocol (MCP) Python SDK
- yt-dlp (YouTube video download)
- openai-whisper (Core audio-to-text engine)
- pydantic

## System Requirements

- FFmpeg (Required for audio processing)
- Minimum 8GB RAM
- Recommended GPU acceleration (NVIDIA GPU + CUDA)
- Sufficient disk space (for model download and temporary files)

## Important First Run Notice

**Important:** On first run, the system will automatically download the Whisper model file (approximately 1GB). This process may take several minutes to tens of minutes, depending on your network conditions. The model file will be cached locally and won't need to be downloaded again for subsequent runs.

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd mcp-ytb-text-extraction
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install FFmpeg (if not already installed):

FFmpeg is required for audio processing. You can download it from [FFmpeg's official website](https://ffmpeg.org/) or install it using your system's package manager:

```bash
# Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg

# MacOS
brew install ffmpeg

# Windows (using Chocolatey)
choco install ffmpeg

# Windows (using Scoop)
scoop install ffmpeg
```

## Usage

### Start the MCP Server

```bash
python server.py
```

### Available MCP Tools

1. Video Download Tool
```json
{
    "name": "video_download",
    "description": "Download video from supported platforms",
    "parameters": {
        "url": "Video URL",
        "output_dir": "Output directory path (optional)"
    }
}
```

2. Audio Download Tool
```json
{
    "name": "audio_download",
    "description": "Download audio from supported platforms",
    "parameters": {
        "url": "Video URL"
    }
}
```

3. Video Text Extraction Tool
```json
{
    "name": "video_extract",
    "description": "Extract text from a video",
    "parameters": {
        "url": "Video URL"
    }
}
```

4. Audio Text Extraction Tool
```json
{
    "name": "audio_extract",
    "description": "Extract text from an audio file",
    "parameters": {
        "audio_path": "Path to the audio file"
    }
}
```

## Configuration

Configuration file is located at `config.yaml`, where you can modify parameters such as:

- Whisper model size (tiny/base/small/medium/large)
- Language settings
- Server configuration
- Temporary file storage location

## Performance Optimization Tips

1. GPU Acceleration:
   - Install CUDA and cuDNN
   - Ensure GPU version of PyTorch is installed

2. Model Size Adjustment:
   - tiny: Fastest but lower accuracy
   - base: Balanced speed and accuracy
   - large: Highest accuracy but requires more resources

3. Use SSD storage for temporary files to improve I/O performance

## Notes

- Whisper model (approximately 1GB) needs to be downloaded on first run
- Ensure sufficient disk space for temporary audio files
- Stable network connection required for YouTube video downloads
- GPU recommended for faster audio processing
- Processing long videos may take considerable time

## MCP Integration Guide

This server can be used with any MCP-compatible client, such as:
- Claude Desktop
- Custom MCP clients
- Other MCP-enabled applications

For more information about MCP, visit [Model Context Protocol](https://modelcontextprotocol.io/introduction).

## Documentation

For Chinese version of this documentation, please refer to [README_zh.md](README_zh.md)

# MCP Video Service

A versatile MCP server for video downloading and text extraction from various platforms.

## Supported Platforms

- YouTube
- Bilibili
- TikTok
- Instagram
- Twitter/X
- Facebook
- Vimeo
- Dailymotion
- SoundCloud

## Features

- Video download
- Audio extraction
- Video text extraction
- Audio text extraction

## Prerequisites

### FFmpeg Installation

FFmpeg is required for audio processing. You can download it from [FFmpeg's official website](https://ffmpeg.org/).

Installation commands for different platforms:

```bash
# Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg

# MacOS
brew install ffmpeg

# Windows (using Chocolatey)
choco install ffmpeg

# Windows (using Scoop)
scoop install ffmpeg
```

## Installation

```bash
pip install mcp-video-service
```

## Usage

You can use this service through the MCP protocol. Here's an example configuration for mcp.so:

```json
{
  "name": "video-service",
  "description": "Video download and text extraction service",
  "fetch": {
    "command": "uvx mcp-video-service",
    "type": "stdio"
  }
}
```

## Configuration

The service can be configured through `config.yaml`. Here are the available options:

```yaml
server:
  host: localhost
  port: 8080
  
service:
  whisper:
    model: base
    language: auto
  audio:
    format: mp3
    quality: 192k
  temp_dir: /tmp/mcp-video
```

## License

MIT
