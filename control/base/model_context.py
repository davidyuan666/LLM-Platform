from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from contextlib import contextmanager

class BaseModelContext(ABC):
    """
    模型上下文管理基类，负责模型运行时的上下文管理
    """
    def __init__(self):
        self.current_context: Dict[str, Any] = {}
        self.context_stack: List[Dict[str, Any]] = []
        
    @contextmanager
    def model_context(self, **kwargs):
        """模型上下文管理器"""
        try:
            self.push_context(**kwargs)
            yield self.current_context
        finally:
            self.pop_context()
    
    def push_context(self, **kwargs) -> None:
        """压入新的上下文"""
        self.context_stack.append(self.current_context.copy())
        self.current_context.update(kwargs)
        self._on_context_push()
    
    def pop_context(self) -> None:
        """弹出当前上下文"""
        if self.context_stack:
            self._on_context_pop()
            self.current_context = self.context_stack.pop()
    
    @abstractmethod
    def _on_context_push(self) -> None:
        """上下文压入时的回调"""
        pass
    
    @abstractmethod
    def _on_context_pop(self) -> None:
        """上下文弹出时的回调"""
        pass