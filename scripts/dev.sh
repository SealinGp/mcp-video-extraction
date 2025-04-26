#!/bin/bash

# 运行 mcp-video-extraction
npx @modelcontextprotocol/inspector uv tool run mcp-video-extraction

# 运行 mcp-video-extraction 的开发环境
npx @modelcontextprotocol/inspector uv run mcp dev src/mcp_video_service/__main__.py

# 构建
uv build

# 发布
uv publish