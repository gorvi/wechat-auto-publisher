"""
Core module for WeChat API integration
"""

from .publisher import WeChatAutoPublisher, WeChatAPIError

__all__ = ["WeChatAutoPublisher", "WeChatAPIError"]
