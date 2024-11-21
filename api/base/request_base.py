from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import requests
from urllib.parse import urljoin

class BaseRequest(ABC):
    """请求基础类，处理所有HTTP请求相关的基础功能"""
    
    def __init__(self):
        self.base_url: str = ""
        self.timeout: int = 30
        self.default_headers: Dict[str, str] = {
            "Content-Type": "application/json"
        }
        self.session = requests.Session()

    def _prepare_request(self, 
                        endpoint: str, 
                        headers: Optional[Dict[str, str]] = None,
                        **kwargs) -> Dict[str, Any]:
        """准备请求参数"""
        url = urljoin(self.base_url, endpoint)
        request_headers = {**self.default_headers, **(headers or {})}
        
        return {
            "url": url,
            "headers": request_headers,
            "timeout": kwargs.get("timeout", self.timeout),
            **kwargs
        }

    async def make_request(self, 
                          method: str, 
                          endpoint: str, 
                          **kwargs) -> requests.Response:
        """发送请求"""
        request_params = self._prepare_request(endpoint, **kwargs)
        
        try:
            response = self.session.request(method, **request_params)
            self._handle_response_status(response)
            return response
        except Exception as e:
            await self._handle_request_error(e, endpoint)
            raise

    @abstractmethod
    async def _handle_request_error(self, error: Exception, endpoint: str) -> None:
        """处理请求错误"""
        pass

    @abstractmethod
    def _handle_response_status(self, response: requests.Response) -> None:
        """处理响应状态"""
        pass

    def set_base_url(self, base_url: str) -> None:
        """设置基础URL"""
        self.base_url = base_url.rstrip('/')

    def set_default_headers(self, headers: Dict[str, str]) -> None:
        """设置默认请求头"""
        self.default_headers.update(headers)