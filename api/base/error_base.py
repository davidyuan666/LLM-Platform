from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

class BaseErrorHandler(ABC):
    """错误处理基类，处理所有API相关错误"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_counts: Dict[str, int] = {}
        self.max_retries: int = 3
        self.error_callbacks: Dict[str, callable] = {}

    async def handle_error(self, error: Exception, context: Dict[str, Any]) -> None:
        """处理错误"""
        error_type = type(error).__name__
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1

        await self._log_error(error, context)
        await self._execute_error_callback(error_type, error, context)
        await self._check_error_threshold(error_type)

    @abstractmethod
    async def _log_error(self, error: Exception, context: Dict[str, Any]) -> None:
        """记录错误"""
        pass

    @abstractmethod
    async def _execute_error_callback(self, 
                                    error_type: str, 
                                    error: Exception, 
                                    context: Dict[str, Any]) -> None:
        """执行错误回调"""
        pass

    @abstractmethod
    async def _check_error_threshold(self, error_type: str) -> None:
        """检查错误阈值"""
        pass

    def register_error_callback(self, 
                              error_type: str, 
                              callback: callable) -> None:
        """注册错误回调"""
        self.error_callbacks[error_type] = callback

    def reset_error_count(self, error_type: str) -> None:
        """重置错误计数"""
        self.error_counts[error_type] = 0