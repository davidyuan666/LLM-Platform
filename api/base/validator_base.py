from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import jsonschema

class BaseValidator(ABC):
    """验证基类，处理请求和响应的验证"""

    def __init__(self):
        self.request_schemas: Dict[str, Dict] = {}
        self.response_schemas: Dict[str, Dict] = {}

    def validate_request(self, endpoint: str, data: Dict[Any, Any]) -> None:
        """验证请求数据"""
        schema = self.request_schemas.get(endpoint)
        if schema:
            try:
                jsonschema.validate(instance=data, schema=schema)
            except jsonschema.exceptions.ValidationError as e:
                raise ValueError(f"Request validation failed: {str(e)}")

    def validate_response(self, endpoint: str, data: Dict[Any, Any]) -> None:
        """验证响应数据"""
        schema = self.response_schemas.get(endpoint)
        if schema:
            try:
                jsonschema.validate(instance=data, schema=schema)
            except jsonschema.exceptions.ValidationError as e:
                raise ValueError(f"Response validation failed: {str(e)}")

    @abstractmethod
    def add_request_schema(self, endpoint: str, schema: Dict[str, Any]) -> None:
        """添加请求架构"""
        pass

    @abstractmethod
    def add_response_schema(self, endpoint: str, schema: Dict[str, Any]) -> None:
        """添加响应架构"""
        pass

    @abstractmethod
    def validate_business_rules(self, data: Dict[Any, Any]) -> None:
        """验证业务规则"""
        pass