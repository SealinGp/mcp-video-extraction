# MCP 视频服务

一个功能强大的 MCP 服务器，用于从各种平台下载视频并提取文本。

## 支持的平台

- YouTube（油管）
- 哔哩哔哩
- 抖音国际版
- Instagram（照片墙）
- Twitter/X（推特）
- Facebook（脸书）
- Vimeo
- Dailymotion
- SoundCloud

## 功能特性

- 视频下载
- 音频提取
- 视频文本提取
- 音频文本提取

## 前置要求

### 安装 FFmpeg

音频处理需要 FFmpeg。您可以从 [FFmpeg 官网](https://ffmpeg.org/) 下载。

不同平台的安装命令：

```bash
# Ubuntu 或 Debian
sudo apt update && sudo apt install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg

# MacOS
brew install ffmpeg

# Windows（使用 Chocolatey）
choco install ffmpeg

# Windows（使用 Scoop）
scoop install ffmpeg
```

## 安装

```bash
pip install mcp-video-service
```

## 使用方法

您可以通过 MCP 协议使用此服务。以下是 mcp.so 的示例配置：

```json
{
  "name": "video-service",
  "description": "视频下载和文本提取服务",
  "fetch": {
    "command": "uvx mcp-video-service",
    "type": "stdio"
  }
}
```

## 配置

服务可以通过 `config.yaml` 进行配置。以下是可用选项：

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

## 许可证

MIT 