"""
智能体基类
所有业务智能体都继承自这个基类

作者：凉贸通团队
版本：v1.0
日期：2026年6月
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional


class BaseAgent:
    """
    智能体基类
    提供通用的智能体功能接口
    """
    
    def __init__(self, agent_name: str):
        """
        初始化智能体
        
        Args:
            agent_name: 智能体名称
        """
        self.agent_name = agent_name
        self.status = "idle"  # idle / running / paused / error
        self.config = self._load_config()
        self.short_term_memory = []  # 短期记忆
        self.long_term_memory = {}   # 长期记忆
        
    def _load_config(self) -> Dict:
        """
        加载智能体配置
        
        Returns:
            配置字典
        """
        # 演示版本：使用默认配置
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "language": "zh-CN"
        }
    
    def run(self, input_data: Any) -> Any:
        """
        运行智能体处理任务
        
        Args:
            input_data: 输入数据
            
        Returns:
            处理结果
        """
        self.status = "running"
        try:
            result = self.process(input_data)
            self.status = "idle"
            return result
        except Exception as e:
            self.status = "error"
            raise e
    
    def process(self, input_data: Any) -> Any:
        """
        处理逻辑（子类需要实现）
        
        Args:
            input_data: 输入数据
            
        Returns:
            处理结果
            
        Raises:
            NotImplementedError: 子类未实现时抛出
        """
        raise NotImplementedError("子类必须实现process方法")
    
    def get_status(self) -> str:
        """
        获取智能体状态
        
        Returns:
            状态字符串
        """
        return self.status
    
    def add_to_memory(self, data: Any, memory_type: str = "short"):
        """
        添加到记忆
        
        Args:
            data: 要存储的数据
            memory_type: 记忆类型 short/long
        """
        if memory_type == "short":
            self.short_term_memory.append({
                "timestamp": datetime.now().isoformat(),
                "data": data
            })
            # 只保留最近100条
            if len(self.short_term_memory) > 100:
                self.short_term_memory = self.short_term_memory[-100:]
        else:
            # 长期记忆
            key = f"memory_{len(self.long_term_memory)}"
            self.long_term_memory[key] = {
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
    
    def clear_memory(self, memory_type: str = "short"):
        """
        清空记忆
        
        Args:
            memory_type: 记忆类型 short/long/all
        """
        if memory_type == "short":
            self.short_term_memory = []
        elif memory_type == "long":
            self.long_term_memory = {}
        else:
            self.short_term_memory = []
            self.long_term_memory = {}
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.agent_name} (status: {self.status})"
    
    def __repr__(self) -> str:
        """repr表示"""
        return self.__str__()
