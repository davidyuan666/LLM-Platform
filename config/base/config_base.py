from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
from pathlib import Path
import json
import yaml
from datetime import datetime

class BaseModelConfig(ABC):
    """模型配置基类"""

    def __init__(self, config_path: Union[str, Path]):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.version: str = "1.0.0"
        self.last_updated: datetime = datetime.now()

    def load_config(self) -> None:
        """加载配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        if self.config_path.suffix == '.json':
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        elif self.config_path.suffix in ['.yml', '.yaml']:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported config file format: {self.config_path.suffix}")

    def save_config(self, path: Optional[Union[str, Path]] = None) -> None:
        """保存配置文件
        
        Args:
            path: 保存路径，默认使用原配置文件路径
        """
        save_path = Path(path) if path else self.config_path
        
        self.config['version'] = self.version
        self.config['last_updated'] = self.last_updated.isoformat()

        if save_path.suffix == '.json':
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        elif save_path.suffix in ['.yml', '.yaml']:
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, allow_unicode=True)
        else:
            raise ValueError(f"Unsupported config file format: {save_path.suffix}")