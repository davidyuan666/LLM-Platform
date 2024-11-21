from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import time
import logging
from functools import wraps

class BaseMonitor(ABC):
    """监控基类，处理性能监控和统计"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.performance_stats: Dict[str, Dict[str, float]] = {}
        self.warning_threshold: float = 5.0  # 秒
        self.error_threshold: float = 10.0   # 秒

    def monitor_performance(self, endpoint: str):
        """性能监控装饰器"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    self._record_performance(endpoint, start_time)
                    return result
                except Exception as e:
                    self._record_error(endpoint, e)
                    raise
            return wrapper
        return decorator

    def _record_performance(self, endpoint: str, start_time: float) -> None:
        """记录性能数据"""
        elapsed_time = time.time() - start_time
        
        if endpoint not in self.performance_stats:
            self.performance_stats[endpoint] = {
                'count': 0,
                'total_time': 0,
                'max_time': 0,
                'min_time': float('inf')
            }
            
        stats = self.performance_stats[endpoint]
        stats['count'] += 1
        stats['total_time'] += elapsed_time
        stats['max_time'] = max(stats['max_time'], elapsed_time)
        stats['min_time'] = min(stats['min_time'], elapsed_time)

        self._check_performance_threshold(endpoint, elapsed_time)

    @abstractmethod
    def _check_performance_threshold(self, endpoint: str, elapsed_time: float) -> None:
        """检查性能阈值"""
        pass

    @abstractmethod
    def _record_error(self, endpoint: str, error: Exception) -> None:
        """记录错误"""
        pass

    def get_performance_stats(self, endpoint: str) -> Dict[str, float]:
        """获取性能统计"""
        stats = self.performance_stats.get(endpoint, {})
        if stats and stats['count'] > 0:
            return {
                'avg_time': stats['total_time'] / stats['count'],
                'max_time': stats['max_time'],
                'min_time': stats['min_time'],
                'total_requests': stats['count']
            }
        return {}