from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

class BaseModelManager(ABC):
    """
    模型管理基类，负责模型的整体控制和状态管理
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.models: Dict[str, Any] = {}  # 存储已加载的模型
        self.model_states: Dict[str, str] = {}  # 存储模型状态
        
    @abstractmethod
    def register_model(self, model_id: str, model: Any) -> None:
        """注册模型到管理器"""
        pass
    
    @abstractmethod
    def unregister_model(self, model_id: str) -> None:
        """从管理器中移除模型"""
        pass
    
    @abstractmethod
    def get_model(self, model_id: str) -> Optional[Any]:
        """获取指定模型"""
        pass
    
    @abstractmethod
    def list_models(self) -> Dict[str, Any]:
        """列出所有已注册的模型"""
        pass
    
    def get_model_state(self, model_id: str) -> str:
        """获取模型状态"""
        return self.model_states.get(model_id, "unknown")