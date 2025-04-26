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

- Python 3.10+
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

### Using uv (recommended)

When using uv no specific installation is needed. We will use uvx to directly run the video extraction server:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install FFmpeg

FFmpeg is required for audio processing. You can install it through various methods:

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

### Configure for Claude/Cursor

Add to your Claude/Cursor settings:

```json
"mcpServers": {
  "video-extraction": {
    "command": "uvx",
    "args": ["mcp-video-extraction"]
  }
}
```

### Available MCP Tools

1. Video download: Download videos from supported platforms
2. Audio download: Extract audio from videos on supported platforms
3. Video text extraction: Extract text from videos (download and transcribe)
4. Audio file text extraction: Extract text from audio files

## Configuration

The service can be configured through environment variables:

### Whisper Configuration
- `WHISPER_MODEL`: Whisper model size (tiny/base/small/medium/large), default: 'base'
- `WHISPER_LANGUAGE`: Language setting for transcription, default: 'auto'

### YouTube Download Configuration
- `YOUTUBE_FORMAT`: Video format for download, default: 'bestaudio'
- `AUDIO_FORMAT`: Audio format for extraction, default: 'mp3'
- `AUDIO_QUALITY`: Audio quality setting, default: '192'

### Storage Configuration
- `TEMP_DIR`: Temporary file storage location, default: '/tmp/mcp-video'

### Download Settings
- `DOWNLOAD_RETRIES`: Number of download retries, default: 10
- `FRAGMENT_RETRIES`: Number of fragment download retries, default: 10
- `SOCKET_TIMEOUT`: Socket timeout in seconds, default: 30

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

## License

MIT