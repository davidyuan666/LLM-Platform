from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import os

class BaseModelLoader(ABC):
    """
    模型加载基类，负责模型的加载和初始化
    """
    def __init__(self):
        self.model_path: str = ""
        self.supported_formats = ['.pt', '.pth', '.bin', '.onnx']
        
    @abstractmethod
    async def load_model(self, model_path: str, **kwargs) -> Any:
        """异步加载模型"""
        pass
    
    @abstractmethod
    def load_model_sync(self, model_path: str, **kwargs) -> Any:
        """同步加载模型"""
        pass
    
    def validate_model_file(self, model_path: str) -> bool:
        """验证模型文件"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        file_extension = os.path.splitext(model_path)[1]
        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported model format: {file_extension}")
        
        return True
    
    @abstractmethod
    def preprocess_model(self, model: Any) -> Any:
        """模型预处理"""
        pass