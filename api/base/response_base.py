from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import json

class BaseResponse(ABC):
    """响应处理基类，处理所有响应相关的功能"""

    def __init__(self):
        self.response_handlers: Dict[int, callable] = {
            200: self._handle_success,
            400: self._handle_bad_request,
            401: self._handle_unauthorized,
            403: self._handle_forbidden,
            404: self._handle_not_found,
            500: self._handle_server_error
        }

    def process_response(self, response: Any) -> Dict[Any, Any]:
        """处理响应"""
        handler = self.response_handlers.get(
            response.status_code, 
            self._handle_unknown
        )
        return handler(response)

    @abstractmethod
    def _handle_success(self, response: Any) -> Dict[Any, Any]:
        """处理成功响应"""
        pass

    @abstractmethod
    def _handle_bad_request(self, response: Any) -> Dict[Any, Any]:
        """处理错误请求"""
        pass

    @abstractmethod
    def _handle_unauthorized(self, response: Any) -> Dict[Any, Any]:
        """处理未授权请求"""
        pass

    @abstractmethod
    def _handle_forbidden(self, response: Any) -> Dict[Any, Any]:
        """处理禁止访问"""
        pass

    @abstractmethod
    def _handle_not_found(self, response: Any) -> Dict[Any, Any]:
        """处理未找到资源"""
        pass

    @abstractmethod
    def _handle_server_error(self, response: Any) -> Dict[Any, Any]:
        """处理服务器错误"""
        pass

    @abstractmethod
    def _handle_unknown(self, response: Any) -> Dict[Any, Any]:
        """处理未知状态码"""
        pass