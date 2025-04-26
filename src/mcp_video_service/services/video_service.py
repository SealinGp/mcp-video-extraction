import os
import tempfile
import whisper
import yt_dlp
import logging
from typing import Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('video_service')

class VideoLogger:
    """自定义的 yt-dlp 日志处理器"""
    def debug(self, msg):
        # 兼容 youtube-dl，debug 和 info 都会传递到这里
        # 可以通过 '[debug] ' 前缀区分
        if msg.startswith('[debug] '):
            return
        # 非调试信息传递给 info 处理
        self.info(msg)

    def info(self, msg):
        # 不输出普通信息
        pass

    def warning(self, msg):
        # 不输出警告信息
        pass

    def error(self, msg):
        # 只输出错误信息到我们的日志系统
        logger.error(msg)

def download_hook(d):
    """下载进度回调函数"""
    if d['status'] == 'finished':
        logger.info('下载完成，开始后处理...')

class VideoService:
    """视频服务，负责下载视频的音频部分并进行文字转换处理"""
    
    def __init__(self):
        # 从环境变量读取配置
        self.config = {
            'whisper': {
                'model': os.getenv('WHISPER_MODEL', 'base'),
                'language': os.getenv('WHISPER_LANGUAGE', 'auto')
            },
            'youtube': {
                'download': {
                    'format': os.getenv('YOUTUBE_FORMAT', 'bestaudio'),
                    'audio_format': os.getenv('AUDIO_FORMAT', 'mp3'),
                    'audio_quality': os.getenv('AUDIO_QUALITY', '192')
                }
            },
            'storage': {
                'temp_dir': os.getenv('TEMP_DIR', '/tmp/mcp-video')
            }
        }
            
        logger.info("初始化 Whisper 模型...")
        self.model = whisper.load_model(self.config['whisper']['model'])
        
        # 通用下载选项
        self.common_opts = {
            'logger': VideoLogger(),  # 使用自定义日志处理器
            'progress_hooks': [download_hook],  # 使用下载进度回调
            'retries': int(os.getenv('DOWNLOAD_RETRIES', '10')),  # 重试次数
            'fragment_retries': int(os.getenv('FRAGMENT_RETRIES', '10')),  # 分片下载重试次数
            'socket_timeout': int(os.getenv('SOCKET_TIMEOUT', '30')),  # 设置较长的超时时间
            'nocheckcertificate': True,  # 忽略 SSL 证书验证
            'ignoreerrors': True,  # 忽略可恢复的错误
        }
        
        # 音频下载配置
        self.audio_opts = {
            **self.common_opts,
            'format': self.config['youtube']['download']['format'],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.config['youtube']['download']['audio_format'],
                'preferredquality': self.config['youtube']['download']['audio_quality'],
            }],
        }
        
        # 视频下载配置
        self.video_opts = {
            **self.common_opts,
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
        }

        # 确保临时目录存在
        os.makedirs(self.config['storage']['temp_dir'], exist_ok=True)

    async def download(self, url: str, output_dir: str = '.') -> Optional[str]:
        """
        从各种视频平台下载完整视频。支持的平台包括但不限于：
        - YouTube
        - Bilibili
        - TikTok
        - Instagram
        - Twitter/X
        - Facebook
        - Vimeo
        - Dailymotion
        
        完整的支持平台列表请参考：
        https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
        
        Args:
            url: 视频平台的URL
            output_dir: 视频保存目录，默认为当前目录
            
        Returns:
            str: 下载的视频文件路径
            
        Raises:
            Exception: 当下载失败时抛出异常
        """
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 设置下载选项
        opts = self.video_opts.copy()
        opts['outtmpl'] = os.path.join(output_dir, opts['outtmpl'])
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                # # 获取视频信息
                info = ydl.extract_info(url, download=True)
                # 获取下载后的文件路径
                video_path = ydl.prepare_filename(info)
                return video_path
        except Exception as e:
            raise Exception(f"下载视频失败: {str(e)}")

    async def download_audio(self, url: str) -> Optional[str]:
        """
        从各种视频平台下载音频。支持的平台包括但不限于：
        - YouTube
        - Bilibili
        - TikTok
        - Instagram
        - Twitter/X
        - Facebook
        - Vimeo
        - Dailymotion
        - SoundCloud
        
        完整的支持平台列表请参考：
        https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
        
        Args:
            url: 视频平台的URL
            
        Returns:
            str: 下载的音频文件路径（MP3格式）
            
        Raises:
            Exception: 当下载失败时抛出异常
        """
        with tempfile.TemporaryDirectory(dir=self.config['storage']['temp_dir']) as temp_dir:
            opts = self.audio_opts.copy()
            opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
            
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    return os.path.join(temp_dir, f"{info['title']}.{self.config['youtube']['download']['audio_format']}")
            except Exception as e:
                raise Exception(f"下载视频失败: {str(e)}")

    async def extract_text(self, audio_path: str) -> str:
        """
        从音频文件中提取文字
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            str: 提取的文字内容
            
        Raises:
            Exception: 当文件不存在或处理失败时
        """
        try:
            if not os.path.exists(audio_path):
                raise Exception(f"音频文件不存在: {audio_path}")

            # 使用 Whisper 模型转录音频
            result = self.model.transcribe(
                audio_path,
                language=None if self.config['whisper']['language'] == 'auto' else self.config['whisper']['language']
            )
            return result["text"]

        except Exception as e:
            raise Exception(f"文字提取失败: {str(e)}")

    async def cleanup(self, audio_path: str):
        """清理临时音频文件"""
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
        except Exception as e:
            logger.error(f"清理音频文件失败: {str(e)}")

    async def process_video(self, url: str) -> str:
        """
        处理视频：下载音频并提取文字
        
        Args:
            url: 视频 URL
            
        Returns:
            str: 提取的文字内容
            
        Raises:
            Exception: 当处理失败时
        """
        try:
            # 下载音频
            audio_path = await self.download_audio(url)
            if not audio_path:
                raise Exception("音频下载失败")
            
            logger.debug(f"音频文件路径: {audio_path}")

            try:
                # 提取文字
                return await self.extract_text(audio_path)
            finally:
                # 清理临时文件
                await self.cleanup(audio_path)

        except Exception as e:
            raise Exception(f"视频处理失败: {str(e)}") 