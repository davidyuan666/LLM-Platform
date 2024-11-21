from typing import Dict, Any, List, Optional
from datetime import datetime
import semver
from pathlib import Path
import json
from .config_base import BaseModelConfig

class BaseVersionControl:
    """版本控制基类"""

    def __init__(self, version_file: Union[str, Path]):
        self.version_file = Path(version_file)
        self.version_history: List[Dict[str, Any]] = []
        self.current_version: Optional[str] = None
        self._load_version_history()

    def _load_version_history(self) -> None:
        """加载版本历史"""
        if self.version_file.exists():
            with open(self.version_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.version_history = data['history']
                self.current_version = data['current_version']

    def _save_version_history(self) -> None:
        """保存版本历史"""
        with open(self.version_file, 'w', encoding='utf-8') as f:
            json.dump({
                'current_version': self.current_version,
                'history': self.version_history
            }, f, indent=2, ensure_ascii=False)

    def create_version(
        self,
        config: BaseModelConfig,
        version_type: str = 'patch',
        description: str = ''
    ) -> str:
        """创建新版本
        
        Args:
            config: 配置实例
            version_type: 版本更新类型 ('major', 'minor', 'patch')
            description: 版本更新说明
        
        Returns:
            新版本号
        """
        if not self.current_version:
            new_version = '1.0.0'
        else:
            ver = semver.VersionInfo.parse(self.current_version)
            if version_type == 'major':
                new_version = str(ver.bump_major())
            elif version_type == 'minor':
                new_version = str(ver.bump_minor())
            else:
                new_version = str(ver.bump_patch())

        version_info = {
            'version': new_version,
            'timestamp': datetime.now().isoformat(),
            'description': description,
            'config_snapshot': config.config
        }
        
        self.version_history.append(version_info)
        self.current_version = new_version
        self._save_version_history()
        
        return new_version

    def get_version_info(self, version: Optional[str] = None) -> Dict[str, Any]:
        """获取版本信息"""
        target_version = version or self.current_version
        for ver_info in self.version_history:
            if ver_info['version'] == target_version:
                return ver_info
        raise ValueError(f"Version not found: {target_version}")

    def rollback_version(self, target_version: str) -> None:
        """回滚到指定版本"""
        if not any(v['version'] == target_version for v in self.version_history):
            raise ValueError(f"Target version not found: {target_version}")
            
        self.current_version = target_version
        self._save_version_history()