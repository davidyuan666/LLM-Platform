from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union, List
from pathlib import Path

class BaseModelRepository(ABC):
    """模型仓库基类，用于管理不同类型的AI模型"""

    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.model_configs: Dict[str, Dict[str, Any]] = {}

    @abstractmethod
    def load_text_model(self, model_id: str, model_path: Union[str, Path], **kwargs) -> None:
        """加载文本类模型（如对话、文本生成等）
        
        Args:
            model_id: 模型唯一标识符
            model_path: 模型文件路径
            **kwargs: 额外的模型参数
        """
        pass

    @abstractmethod
    def load_image_model(self, model_id: str, model_path: Union[str, Path], **kwargs) -> None:
        """加载图像处理模型（如图像分类、目标检测等）
        
        Args:
            model_id: 模型唯一标识符
            model_path: 模型文件路径
            **kwargs: 额外的模型参数
        """
        pass

    @abstractmethod
    def load_text2image_model(self, model_id: str, model_path: Union[str, Path], **kwargs) -> None:
        """加载文生图模型
        
        Args:
            model_id: 模型唯一标识符
            model_path: 模型文件路径
            **kwargs: 额外的模型参数
        """
        pass

    @abstractmethod
    def get_model(self, model_id: str) -> Any:
        """获取指定ID的模型实例
        
        Args:
            model_id: 模型唯一标识符
        
        Returns:
            模型实例
        """
        pass

    @abstractmethod
    def unload_model(self, model_id: str) -> None:
        """卸载指定ID的模型
        
        Args:
            model_id: 模型唯一标识符
        """
        pass

    def get_model_config(self, model_id: str) -> Optional[Dict[str, Any]]:
        """获取模型配置信息
        
        Args:
            model_id: 模型唯一标识符
            
        Returns:
            模型配置信息字典
        """
        return self.model_configs.get(model_id)

    def list_models(self) -> List[str]:
        """获取所有已加载模型的ID列表
        
        Returns:
            模型ID列表
        """
        return list(self.models.keys())