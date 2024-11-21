from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
from pathlib import Path

class BaseModel(ABC):
    """AI模型基类"""

    def __init__(self, model_id: str, model_path: Union[str, Path], **kwargs):
        self.model_id = model_id
        self.model_path = Path(model_path)
        self.model: Optional[Any] = None
        self.config: Dict[str, Any] = kwargs

    @abstractmethod
    def load(self) -> None:
        """加载模型"""
        pass

    @abstractmethod
    def unload(self) -> None:
        """卸载模型"""
        pass

    def is_loaded(self) -> bool:
        """检查模型是否已加载"""
        return self.model is not None

    def get_config(self) -> Dict[str, Any]:
        """获取模型配置"""
        return self.config