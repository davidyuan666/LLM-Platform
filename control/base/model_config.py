from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import json
import yaml

class BaseModelConfig(ABC):
    """
    模型配置管理基类，负责模型配置的加载和更新
    """
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.config_path: Optional[str] = None
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        self.config_path = config_path
        
        if config_path.endswith('.json'):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        elif config_path.endswith('.yaml') or config_path.endswith('.yml'):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        else:
            raise ValueError("Unsupported config file format")
            
        return self.config
    
    @abstractmethod
    def update_config(self, updates: Dict[str, Any]) -> None:
        """更新配置"""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """验证配置有效性"""
        pass
    
    def save_config(self) -> None:
        """保存配置到文件"""
        if not self.config_path:
            raise ValueError("Config path not set")
            
        if self.config_path.endswith('.json'):
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        elif self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f)