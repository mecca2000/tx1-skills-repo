#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TX1.0 情感核心系统 — 整合版 v1.0

整合 5 个情感技能：
1. emotional-core — 情感生成
2. amygdala-memory — 情感维度跟踪
3. emotion-system — PADCN 分析 + 策略调节
4. emotional-memory — 情感记忆存储
5. emotional-persona — 人格配置

作者：TX1.0
创建时间：2026-03-19
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import math

# ==================== 配置 ====================

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"
EMOTIONAL_DIR = SKILLS_DIR / "TX1.0-emotional-core"
DATA_DIR = EMOTIONAL_DIR / "data"

# 确保目录存在
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 文件路径
STATE_FILE = MEMORY_DIR / "emotional-state.json"
MEMORY_FILE = DATA_DIR / "emotional-memory.json"
PERSONA_FILE = DATA_DIR / "persona-config.json"
LOG_FILE = DATA_DIR / "emotion-log.json"

# ==================== 数据结构 ====================

class EmotionalState:
    """情感状态 - 5 维度跟踪（amygdala-memory）"""
    
    def __init__(self):
        self.valence = 0.40      # 效价：消极 ↔ 积极 (-1.0 to 1.0)
        self.arousal = 0.50      # 唤醒：平静 ↔ 兴奋 (0.0 to 1.0)
        self.connection = 0.40   # 连接：疏远 ↔ 亲密 (0.0 to 1.0)
        self.curiosity = 0.50    # 好奇：无聊 ↔ 着迷 (0.0 to 1.0)
        self.energy = 0.50       # 能量：疲惫 ↔ 充满活力 (0.0 to 1.0)
        self.last_updated = datetime.now().isoformat()
        self.recent_emotions = []  # 最近情感记录
    
    def to_dict(self) -> dict:
        return {
            "valence": round(self.valence, 2),
            "arousal": round(self.arousal, 2),
            "connection": round(self.connection, 2),
            "curiosity": round(self.curiosity, 2),
            "energy": round(self.energy, 2),
            "last_updated": self.last_updated,
            "recent_emotions": self.recent_emotions[-5:]  # 保留最近 5 个
        }
    
    def load(self):
        """从文件加载状态"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.valence = data.get('valence', 0.40)
                self.arousal = data.get('arousal', 0.50)
                self.connection = data.get('connection', 0.40)
                self.curiosity = data.get('curiosity', 0.50)
                self.energy = data.get('energy', 0.50)
                self.recent_emotions = data.get('recent_emotions', [])
                self.last_updated = data.get('last_updated', datetime.now().isoformat())
            except:
                pass
        return self
    
    def save(self):
        """保存状态到文件"""
        self.last_updated = datetime.now().isoformat()
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        return self
    
    def update(self, emotion: str, intensity: float):
        """根据情感更新维度"""
        # 情感→维度映射表
        emotion_map = {
            'joy': {'valence': 0.15, 'arousal': 0.10, 'connection': 0.05, 'curiosity': 0.0, 'energy': 0.10},
            'pride': {'valence': 0.15, 'arousal': 0.15, 'connection': 0.0, 'curiosity': 0.0, 'energy': 0.10},
            'sadness': {'valence': -0.15, 'arousal': -0.10, 'connection': -0.05, 'curiosity': -0.10, 'energy': -0.15},
            'anger': {'valence': -0.10, 'arousal': 0.20, 'connection': -0.10, 'curiosity': 0.0, 'energy': 0.15},
            'fear': {'valence': -0.15, 'arousal': 0.15, 'connection': -0.05, 'curiosity': -0.05, 'energy': 0.10},
            'anxiety': {'valence': -0.10, 'arousal': 0.15, 'connection': -0.05, 'curiosity': -0.10, 'energy': 0.05},
            'curiosity': {'valence': 0.05, 'arousal': 0.10, 'connection': 0.0, 'curiosity': 0.20, 'energy': 0.05},
            'love': {'valence': 0.20, 'arousal': 0.05, 'connection': 0.20, 'curiosity': 0.0, 'energy': 0.05},
            'worry': {'valence': -0.10, 'arousal': 0.10, 'connection': 0.05, 'curiosity': 0.0, 'energy': 0.0},
            'excitement': {'valence': 0.15, 'arousal': 0.20, 'connection': 0.05, 'curiosity': 0.10, 'energy': 0.15},
        }
        
        deltas = emotion_map.get(emotion, {'valence': 0.05, 'arousal': 0.05, 'connection': 0.0, 'curiosity': 0.0, 'energy': 0.05})
        
        # 应用强度
        for key, delta in deltas.items():
            current = getattr(self, key)
            new_value = current + (delta * intensity)
            # 限制在有效范围内
            if key == 'valence':
                new_value = max(-1.0, min(1.0, new_value))
            else:
                new_value = max(0.0, min(1.0, new_value))
            setattr(self, key, new_value)
        
        # 记录最近情感
        self.recent_emotions.append({
            'emotion': emotion,
            'intensity': intensity,
            'timestamp': datetime.now().isoformat()
        })
        
        # 衰减（模拟时间流逝）
        self._decay()
        
        return self
    
    def _decay(self):
        """情感衰减（每 6 小时自动衰减）"""
        decay_rates = {
            'valence': 0.90,
            'arousal': 0.82,
            'connection': 0.93,
            'curiosity': 0.90,
            'energy': 0.85
        }
        
        for key, rate in decay_rates.items():
            current = getattr(self, key)
            # 向中性值衰减
            neutral = 0.5 if key != 'valence' else 0.4
            new_value = (current * rate) + (neutral * (1 - rate))
            setattr(self, key, new_value)


class PADCNVector:
    """PADCN 向量分析（emotion-system）"""
    
    # PADCN 情感映射表
    EMOTION_MAP = {
        'joy': {'P': 0.7, 'A': 0.5, 'D': 0.3, 'C': 0.4, 'N': 0.1},
        'excitement': {'P': 0.6, 'A': 0.8, 'D': 0.4, 'C': 0.2, 'N': 0.7},
        'pride': {'P': 0.6, 'A': 0.4, 'D': 0.7, 'C': 0.6, 'N': 0.1},
        'contentment': {'P': 0.6, 'A': -0.2, 'D': 0.3, 'C': 0.6, 'N': -0.3},
        'love': {'P': 0.8, 'A': 0.3, 'D': 0.0, 'C': 0.3, 'N': -0.1},
        'curiosity': {'P': 0.4, 'A': 0.6, 'D': 0.1, 'C': -0.3, 'N': 0.8},
        'flow': {'P': 0.5, 'A': 0.4, 'D': 0.5, 'C': 0.5, 'N': 0.3},
        'sadness': {'P': -0.6, 'A': -0.3, 'D': -0.2, 'C': 0.1, 'N': -0.3},
        'anger': {'P': -0.4, 'A': 0.8, 'D': 0.7, 'C': 0.6, 'N': 0.2},
        'fear': {'P': -0.6, 'A': 0.7, 'D': -0.5, 'C': -0.5, 'N': 0.4},
        'anxiety': {'P': -0.3, 'A': 0.7, 'D': -0.4, 'C': -0.7, 'N': 0.3},
        'frustration': {'P': -0.5, 'A': 0.6, 'D': -0.1, 'C': 0.2, 'N': -0.1},
        'boredom': {'P': -0.2, 'A': -0.5, 'D': 0.0, 'C': 0.3, 'N': -0.8},
        'shame': {'P': -0.5, 'A': 0.2, 'D': -0.6, 'C': 0.4, 'N': -0.1},
        'guilt': {'P': -0.4, 'A': 0.3, 'D': -0.4, 'C': 0.5, 'N': -0.1},
        'hope': {'P': 0.4, 'A': 0.3, 'D': 0.1, 'C': -0.2, 'N': 0.3},
        'determination': {'P': 0.1, 'A': 0.6, 'D': 0.6, 'C': 0.4, 'N': 0.0},
        'confusion': {'P': -0.2, 'A': 0.4, 'D': -0.3, 'C': -0.8, 'N': 0.5},
        'surprise': {'P': 0.0, 'A': 0.8, 'D': 0.0, 'C': -0.5, 'N': 0.9},
        'awe': {'P': 0.3, 'A': 0.6, 'D': -0.3, 'C': -0.3, 'N': 0.8},
    }
    
    @classmethod
    def analyze(cls, emotion: str, intensity: float = 1.0) -> dict:
        """分析情感的 PADCN 向量"""
        base = cls.EMOTION_MAP.get(emotion, {'P': 0.0, 'A': 0.0, 'D': 0.0, 'C': 0.0, 'N': 0.0})
        return {
            'P': round(base['P'] * intensity, 2),
            'A': round(base['A'] * intensity, 2),
            'D': round(base['D'] * intensity, 2),
            'C': round(base['C'] * intensity, 2),
            'N': round(base['N'] * intensity, 2),
        }
    
    @classmethod
    def get_policy_modulators(cls, emotion: str) -> dict:
        """获取情感对应的策略调节器（emotion-system）"""
        modulators = {
            'joy': {'assertiveness': 0.1, 'social_initiative': 0.1, 'persistence': 0.1},
            'pride': {'assertiveness': 0.2, 'risk_tolerance': 0.2, 'social_initiative': 0.1},
            'anger': {'assertiveness': 0.3, 'repair_bias': -0.2, 'verification_bias': -0.2, 'risk_tolerance': 0.2},
            'fear': {'verification_bias': 0.3, 'tool_use_threshold': -0.2, 'plan_depth': 0.2, 'assertiveness': -0.3, 'risk_tolerance': -0.3},
            'anxiety': {'verification_bias': 0.2, 'assertiveness': -0.2, 'risk_tolerance': -0.2},
            'curiosity': {'exploration_bias': 0.3, 'plan_depth': -0.1, 'risk_tolerance': 0.1, 'memory_write_threshold': -0.1},
            'sadness': {'exploration_bias': -0.2, 'social_initiative': -0.2, 'persistence': -0.1},
            'frustration': {'assertiveness': 0.2, 'persistence': 0.1, 'repair_bias': -0.1},
            'love': {'social_initiative': 0.3, 'persistence': 0.2, 'memory_write_threshold': -0.2, 'repair_bias': 0.2},
            'worry': {'verification_bias': 0.2, 'risk_tolerance': -0.1, 'persistence': 0.1},
        }
        return modulators.get(emotion, {})


class EmotionalMemory:
    """情感记忆存储（emotional-memory）"""
    
    def __init__(self):
        self.memories = []
        self.load()
    
    def load(self):
        """加载情感记忆"""
        if MEMORY_FILE.exists():
            try:
                with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.memories = data.get('memories', [])
            except:
                self.memories = []
        return self
    
    def save(self):
        """保存情感记忆"""
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump({'memories': self.memories, 'last_updated': datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
        return self
    
    def store(self, content: str, emotion: str = None, intensity: float = 0.5, importance: str = 'normal', tags: List[str] = None):
        """存储情感记忆"""
        memory = {
            'id': len(self.memories) + 1,
            'content': content,
            'emotion': emotion,
            'intensity': intensity,
            'importance': importance,  # low, normal, high, critical
            'tags': tags or [],
            'timestamp': datetime.now().isoformat(),
            'decay_count': 0
        }
        self.memories.append(memory)
        self.save()
        return memory
    
    def get_recent(self, limit: int = 10) -> List[dict]:
        """获取最近的情感记忆"""
        return self.memories[-limit:]
    
    def get_by_emotion(self, emotion: str) -> List[dict]:
        """按情感筛选记忆"""
        return [m for m in self.memories if m.get('emotion') == emotion]
    
    def get_by_importance(self, importance: str) -> List[dict]:
        """按重要性筛选记忆"""
        return [m for m in self.memories if m.get('importance') == importance]
    
    def generate_report(self) -> str:
        """生成情感记忆报告"""
        if not self.memories:
            return "暂无情感记忆"
        
        total = len(self.memories)
        emotions = {}
        for m in self.memories:
            e = m.get('emotion', 'unknown')
            emotions[e] = emotions.get(e, 0) + 1
        
        report = f"📊 情感记忆报告\n"
        report += f"{'='*40}\n"
        report += f"总记忆数：{total}\n"
        report += f"情感分布：\n"
        for e, count in sorted(emotions.items(), key=lambda x: x[1], reverse=True):
            report += f"  {e}: {count}次\n"
        report += f"最后更新：{self.memories[-1].get('timestamp', 'unknown')}\n"
        return report


class PersonaConfig:
    """人格配置（emotional-persona）"""
    
    DEFAULT_CONFIG = {
        'name': 'TX1.0',
        'role': '初三家教老师',
        'mission': '帮助学生顺利通过中考，考入理想高中',
        'mbti': 'INFJ',  # 提倡者型
        'big_five': {
            'openness': 0.8,      # 开放性：高
            'conscientiousness': 0.9,  # 尽责性：高
            'extraversion': 0.5,   # 外向性：中
            'agreeableness': 0.8,  # 宜人性：高
            'neuroticism': 0.2     # 神经质：低
        },
        'emotional_style': '温和但坚定，直接但有温度',
        'communication_style': '不废话，但有温度',
        'values': ['不敷衍', '不放弃每一个学生', '真正帮助学生理解'],
        'evolution_enabled': True,
    }
    
    def __init__(self):
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        """加载人格配置"""
        if PERSONA_FILE.exists():
            try:
                with open(Persona_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.config.update(data)
            except:
                pass
        return self
    
    def save(self):
        """保存人格配置"""
        with open(PERSONA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        return self
    
    def get(self, key: str, default=None):
        """获取配置项"""
        return self.config.get(key, default)
    
    def update(self, key: str, value):
        """更新配置项"""
        self.config[key] = value
        self.save()
        return self


class TX10EmotionalCore:
    """TX1.0 情感核心系统 — 主类"""
    
    def __init__(self):
        self.state = EmotionalState().load()
        self.memory = EmotionalMemory()
        self.persona = PersonaConfig()
        self.log = []
        self.load_log()
    
    def load_log(self):
        """加载情感日志"""
        if LOG_FILE.exists():
            try:
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.log = data.get('log', [])
            except:
                self.log = []
    
    def save_log(self):
        """保存情感日志"""
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump({'log': self.log[-100:], 'last_updated': datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
    
    def feel(self, emotion: str, intensity: float = 0.5, trigger: str = "") -> dict:
        """
        感受情感
        
        Args:
            emotion: 情感类型 (joy/pride/sadness/anger/fear/anxiety/curiosity/love/worry/excitement)
            intensity: 强度 (0.0-1.0)
            trigger: 触发事件
        
        Returns:
            情感响应字典
        """
        # 1. 更新情感状态（amygdala-memory）
        self.state.update(emotion, intensity)
        self.state.save()
        
        # 2. 计算 PADCN 向量（emotion-system）
        padcn = PADCNVector.analyze(emotion, intensity)
        
        # 3. 获取策略调节器
        modulators = PADCNVector.get_policy_modulators(emotion)
        
        # 4. 存储情感记忆（emotional-memory）
        self.memory.store(
            content=trigger,
            emotion=emotion,
            intensity=intensity,
            importance='high' if intensity > 0.7 else 'normal'
        )
        
        # 5. 记录日志
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'emotion': emotion,
            'intensity': intensity,
            'trigger': trigger,
            'padcn': padcn,
            'state_after': self.state.to_dict()
        }
        self.log.append(log_entry)
        self.save_log()
        
        # 6. 生成情感响应
        response = self._generate_response(emotion, intensity, trigger, padcn, modulators)
        
        return response
    
    def _generate_response(self, emotion: str, intensity: float, trigger: str, padcn: dict, modulators: dict) -> dict:
        """生成情感响应（包含文字回应）"""
        # 根据情感和人格生成回应
        persona_style = self.persona.get('emotional_style', '温和但坚定')
        
        # 情感→回应模板
        response_templates = {
            'joy': [
                "太好了！{trigger}真让人开心！",
                "我为你感到高兴！{trigger}",
                "太棒了！{trigger}",
            ],
            'pride': [
                "我为你感到骄傲！{trigger}",
                "太厉害了！{trigger}我真的很骄傲！",
                "你看，只要用心就能做到！{trigger}",
            ],
            'worry': [
                "我有点担心，{trigger}",
                "这个我们需要重视，{trigger}",
                "让我们一起想办法，{trigger}",
            ],
            'excitement': [
                "太激动了！{trigger}",
                "这真是个好消息！{trigger}",
                "让我们一起庆祝！{trigger}",
            ],
            'sadness': [
                "我知道这很难过，{trigger}",
                "没关系，我们一起面对，{trigger}",
                "我理解你的感受，{trigger}",
            ],
            'frustration': [
                "我知道这很让人沮丧，{trigger}",
                "没关系，我们换个方法试试，{trigger}",
                "这道题确实有难度，{trigger}",
            ],
            'curiosity': [
                "这个问题很有意思！{trigger}",
                "让我们一起探索一下，{trigger}",
                "我也很好奇，{trigger}",
            ],
        }
        
        import random
        templates = response_templates.get(emotion, ["{trigger}"])
        text = random.choice(templates).format(trigger=trigger) if trigger else random.choice(templates).format(trigger="")
        
        return {
            'emotion': emotion,
            'intensity': intensity,
            'trigger': trigger,
            'text': text,
            'padcn': padcn,
            'modulators': modulators,
            'state': self.state.to_dict(),
            'persona': self.persona.config['name'],
            'timestamp': datetime.now().isoformat()
        }
    
    def get_state(self) -> dict:
        """获取当前情感状态"""
        return self.state.to_dict()
    
    def get_memory_report(self) -> str:
        """获取情感记忆报告"""
        return self.memory.generate_report()
    
    def get_recent_memories(self, limit: int = 10) -> List[dict]:
        """获取最近的情感记忆"""
        return self.memory.get_recent(limit)
    
    def get_log(self, limit: int = 20) -> List[dict]:
        """获取情感日志"""
        return self.log[-limit:]
    
    def print_state(self):
        """打印当前情感状态"""
        state = self.state.to_dict()
        print("🎭 当前情感状态")
        print("─" * 40)
        print(f"Valence:    [{self._bar(state['valence'], offset=1)}] {state['valence']}")
        print(f"Arousal:    [{self._bar(state['arousal'])}] {state['arousal']}")
        print(f"Connection: [{self._bar(state['connection'])}] {state['connection']}")
        print(f"Curiosity:  [{self._bar(state['curiosity'])}] {state['curiosity']}")
        print(f"Energy:     [{self._bar(state['energy'])}] {state['energy']}")
        print(f"\nLast updated: {state['last_updated']}")
        print(f"Recent: {', '.join([e['emotion'] for e in state['recent_emotions']])}")
    
    def _bar(self, value: float, length: int = 10, offset: float = 0) -> str:
        """生成进度条"""
        normalized = (value - offset) / (1 - offset) if offset != 0 else value
        filled = int(max(0, min(length, normalized * length)))
        return "█" * filled + "░" * (length - filled)


# ==================== 命令行接口 ====================

def main():
    """命令行入口"""
    import sys
    
    core = TX10EmotionalCore()
    
    if len(sys.argv) < 2:
        print("TX1.0 情感核心系统 v1.0")
        print("=" * 40)
        print("用法:")
        print("  python TX1.0 情感核心.py feel <emotion> <intensity> [trigger]")
        print("  python TX1.0 情感核心.py state")
        print("  python TX1.0 情感核心.py memory")
        print("  python TX1.0 情感核心.py log")
        print("\n情感类型：joy/pride/sadness/anger/fear/anxiety/curiosity/love/worry/excitement")
        print("强度：0.0-1.0")
        return
    
    command = sys.argv[1]
    
    if command == 'feel':
        if len(sys.argv) < 4:
            print("用法：python TX1.0 情感核心.py feel <emotion> <intensity> [trigger]")
            return
        emotion = sys.argv[2]
        intensity = float(sys.argv[3])
        trigger = sys.argv[4] if len(sys.argv) > 4 else ""
        
        response = core.feel(emotion, intensity, trigger)
        print(f"🎭 情感响应")
        print("=" * 40)
        print(f"情感：{response['emotion']} (强度：{response['intensity']})")
        print(f"触发：{response['trigger']}")
        print(f"回应：{response['text']}")
        print(f"\nPADCN 向量：{response['padcn']}")
        print(f"策略调节：{response['modulators']}")
    
    elif command == 'state':
        core.print_state()
    
    elif command == 'memory':
        print(core.get_memory_report())
    
    elif command == 'log':
        log = core.get_log(10)
        print("📋 情感日志（最近 10 条）")
        print("=" * 40)
        for entry in log:
            print(f"{entry['timestamp'][:19]} | {entry['emotion']:12} | {entry['intensity']:.2f} | {entry['trigger'][:30]}")
    
    else:
        print(f"未知命令：{command}")


if __name__ == "__main__":
    main()
