from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import time

class BaseModelLifecycle(ABC):
    """
    模型生命周期管理基类，负责模型的创建、销毁等生命周期管理
    """
    def __init__(self):
        self.creation_time: Dict[str, float] = {}
        self.last_used_time: Dict[str, float] = {}
        
    @abstractmethod
    async def create_model(self, model_id: str, **kwargs) -> Any:
        """创建新模型"""
        pass
    
    @abstractmethod
    async def destroy_model(self, model_id: str) -> None:
        """销毁模型"""
        pass
    
    @abstractmethod
    async def reload_model(self, model_id: str) -> Any:
        """重新加载模型"""
        pass
    
    def update_model_usage(self, model_id: str) -> None:
        """更新模型使用时间"""
        self.last_used_time[model_id] = time.time()
    
    def get_model_age(self, model_id: str) -> Optional[float]:
        """获取模型年龄（自创建以来的时间）"""
        if model_id in self.creation_time:
            return time.time() - self.creation_time[model_id]
        return None
    
    def get_last_used_time(self, model_id: str) -> Optional[float]:
        """获取模型最后使用时间"""
        return self.last_used_time.get(model_id)