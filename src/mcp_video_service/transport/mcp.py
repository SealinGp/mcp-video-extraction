# from contextlib import asynccontextmanager
# from collections.abc import AsyncIterator
# import mcp.server.stdio
# import mcp.types as types
# from mcp.server.lowlevel import NotificationOptions, Server
# from mcp.server.models import InitializationOptions

# from mcp_video_service.services.video_service import VideoService

# class MCPTransport:
#     def __init__(self, server: Server):
#         self.server = server
#         self._setup_server()

#     def _setup_server(self):
#         """设置服务器配置和处理程序"""
#         self.server.lifespan = self._server_lifespan
#         self._setup_tools()

#     @asynccontextmanager
#     async def _server_lifespan(self, server: Server) -> AsyncIterator[dict]:
#         """管理服务器的生命周期。"""
#         # 初始化服务
#         video_service = VideoService()
#         try:
#             yield {
#                 "video_service": video_service
#             }
#         finally:
#             # 清理资源
#             pass

#     def _setup_tools(self):
#         """设置服务器工具"""
#         @self.server.list_tools()
#         async def handle_list_tools() -> list[types.Tool]:
#             """列出可用的工具。"""
#             return [
#                 types.Tool(
#                     name="video_download",
#                     description="从支持的视频平台下载视频",
#                     parameters=[
#                         types.ToolParameter(
#                             name="url",
#                             description="视频URL",
#                             required=True,
#                             type="string"
#                         ),
#                         types.ToolParameter(
#                             name="output_dir",
#                             description="输出目录路径",
#                             required=False,
#                             type="string"
#                         )
#                     ]
#                 ),
#                 types.Tool(
#                     name="audio_download",
#                     description="从支持的视频平台下载音频",
#                     parameters=[
#                         types.ToolParameter(
#                             name="url",
#                             description="视频URL",
#                             required=True,
#                             type="string"
#                         )
#                     ]
#                 ),
#                 types.Tool(
#                     name="video_extract",
#                     description="从视频中提取文字内容",
#                     parameters=[
#                         types.ToolParameter(
#                             name="url",
#                             description="视频URL",
#                             required=True,
#                             type="string"
#                         )
#                     ]
#                 ),
#                 types.Tool(
#                     name="audio_extract",
#                     description="从音频文件中提取文字内容",
#                     parameters=[
#                         types.ToolParameter(
#                             name="audio_path",
#                             description="音频文件路径",
#                             required=True,
#                             type="string"
#                         )
#                     ]
#                 )
#             ]

#         @self.server.call_tool()
#         async def handle_call_tool(name: str, arguments: dict) -> str:
#             """处理工具调用。"""
#             ctx = self.server.request_context
#             services = ctx.lifespan_context
#             video_service: VideoService = services["video_service"]

#             try:
#                 if name == "video_download":
#                     output_dir = arguments.get("output_dir", ".")
#                     return await video_service.download(arguments["url"], output_dir)
                
#                 elif name == "audio_download":
#                     return await video_service.download_audio(arguments["url"])
                
#                 elif name == "video_extract":
#                     return await video_service.process_video(arguments["url"])
                
#                 elif name == "audio_extract":
#                     return await video_service.extract_text(arguments["audio_path"])
                
#                 else:
#                     raise ValueError(f"未知的工具: {name}")
            
#             except Exception as e:
#                 raise ValueError(f"工具执行失败: {str(e)}")

#     async def start(self):
        # """启动 MCP 服务器。"""
        # async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        #     await self.server.run(
        #         read_stream,
        #         write_stream,
        #         InitializationOptions(
        #             server_name="video-service",
        #             server_version="1.0.0",
        #             capabilities=self.server.get_capabilities(
        #                 notification_options=NotificationOptions(),
        #                 experimental_capabilities={},
        #             ),
        #         ),
        #     ) 