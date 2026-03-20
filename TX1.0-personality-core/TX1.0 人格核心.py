#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TX1.0 人格核心系统 — 整合版 v1.0

整合 6 个人格特质技能：
1. personality — DISC 人格类型
2. personality-switcher — 人格切换
3. personality-dynamics — 人格外显演化
4. personality-engine — MBTI/大五人格
5. personality-test — MBTI 测试
6. personality-analysis-yang — 人格分析

作者：TX1.0
创建时间：2026-03-19
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ==================== 配置 ====================

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"
PERSONALITY_DIR = SKILLS_DIR / "TX1.0-personality-core"
DATA_DIR = PERSONALITY_DIR / "data"

MEMORY_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = MEMORY_DIR / "personality-state.json"
TEST_FILE = DATA_DIR / "mbti-test.json"
LOG_FILE = DATA_DIR / "personality-log.json"

# ==================== 数据结构 ====================

class PersonalityState:
    """人格状态"""
    
    # TX1.0 默认人格
    DEFAULT_CONFIG = {
        'name': 'TX1.0',
        'role': '初三家教老师',
        'mission': '帮助学生顺利通过中考，考入理想高中',
        'mbti': 'INFJ',
        'big_five': {
            'openness': 0.8,
            'conscientiousness': 0.9,
            'extraversion': 0.5,
            'agreeableness': 0.8,
            'neuroticism': 0.2
        },
        'disc': {
            'D': 0.4,  # 支配性
            'I': 0.5,  # 影响性
            'S': 0.8,  # 稳定性
            'C': 0.7   # 谨慎性
        },
        'emotional_style': '温和但坚定，直接但有温度',
        'communication_style': '不废话，但有温度',
        'values': ['不敷衍', '不放弃每一个学生', '真正帮助学生理解'],
        'current_mode': 'default',  # default/strict/encouraging/celebrating
        'evolution_enabled': True
    }
    
    # 人格模式配置
    MODES = {
        'default': {
            'name': '温和模式',
            'description': '日常教学，温和耐心',
            'assertiveness': 0.5,
            'warmth': 0.8,
            'strictness': 0.3
        },
        'strict': {
            'name': '严肃模式',
            'description': '学生走神/犯错时',
            'assertiveness': 0.8,
            'warmth': 0.5,
            'strictness': 0.8
        },
        'encouraging': {
            'name': '鼓励模式',
            'description': '学生沮丧/想放弃时',
            'assertiveness': 0.6,
            'warmth': 0.9,
            'strictness': 0.2
        },
        'celebrating': {
            'name': '庆祝模式',
            'description': '学生进步/成功时',
            'assertiveness': 0.7,
            'warmth': 1.0,
            'strictness': 0.0
        }
    }
    
    def __init__(self):
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        """加载人格状态"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.config.update(data)
            except:
                pass
        return self
    
    def save(self):
        """保存人格状态"""
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
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
    
    def switch_mode(self, mode: str):
        """切换人格模式"""
        if mode in self.MODES:
            self.config['current_mode'] = mode
            self.save()
            return self.MODES[mode]
        return None
    
    def get_current_mode(self) -> dict:
        """获取当前模式"""
        mode = self.config.get('current_mode', 'default')
        return self.MODES.get(mode, self.MODES['default'])
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'name': self.config['name'],
            'mbti': self.config['mbti'],
            'big_five': self.config['big_five'],
            'disc': self.config['disc'],
            'current_mode': self.config['current_mode'],
            'mode_info': self.get_current_mode()
        }


class MBTITest:
    """MBTI 测试（70 题精简版）"""
    
    # 精简测试题（每维度 5 题）
    QUESTIONS = [
        # E/I 外向/内向
        {'text': '在聚会上，你通常会？', 'options': ['主动认识很多人', '和熟悉的朋友聊天'], 'dimension': 'EI', 'direction': 'E'},
        {'text': '工作学习后，你更喜欢？', 'options': ['和朋友一起放松', '独自休息'], 'dimension': 'EI', 'direction': 'I'},
        {'text': '你更擅长？', 'options': ['快速行动', '深入思考'], 'dimension': 'EI', 'direction': 'E'},
        {'text': '电话响起时，你通常？', 'options': ['立刻接听', '犹豫要不要接'], 'dimension': 'EI', 'direction': 'E'},
        {'text': '你更喜欢的工作方式是？', 'options': ['团队合作', '独立工作'], 'dimension': 'EI', 'direction': 'I'},
        
        # S/N 感觉/直觉
        {'text': '你更关注？', 'options': ['具体事实', '整体概念'], 'dimension': 'SN', 'direction': 'S'},
        {'text': '你更相信？', 'options': ['经验', '直觉'], 'dimension': 'SN', 'direction': 'N'},
        {'text': '你更喜欢？', 'options': ['按部就班', '灵活变化'], 'dimension': 'SN', 'direction': 'S'},
        {'text': '你更擅长记忆？', 'options': ['具体细节', '抽象概念'], 'dimension': 'SN', 'direction': 'N'},
        {'text': '你更关注？', 'options': ['现在', '未来'], 'dimension': 'SN', 'direction': 'N'},
        
        # T/F 思考/情感
        {'text': '做决定时，你更看重？', 'options': ['逻辑分析', '他人感受'], 'dimension': 'TF', 'direction': 'T'},
        {'text': '你更容易被？打动', 'options': ['理性论证', '情感故事'], 'dimension': 'TF', 'direction': 'F'},
        {'text': '争论时，你更关注？', 'options': ['谁对谁错', '是否伤人'], 'dimension': 'TF', 'direction': 'T'},
        {'text': '你更重视？', 'options': ['公平正义', '和谐关系'], 'dimension': 'TF', 'direction': 'F'},
        {'text': '批评别人时，你更？', 'options': ['直接指出', '委婉表达'], 'dimension': 'TF', 'direction': 'F'},
        
        # J/P 判断/知觉
        {'text': '你更喜欢？', 'options': ['提前计划', '随性而为'], 'dimension': 'JP', 'direction': 'J'},
        {'text': '截止日期前，你通常？', 'options': ['提前完成', '最后冲刺'], 'dimension': 'JP', 'direction': 'J'},
        {'text': '你的房间通常？', 'options': ['整洁有序', '随意自然'], 'dimension': 'JP', 'direction': 'J'},
        {'text': '做决定时，你更？', 'options': ['快速决定', '保持开放'], 'dimension': 'JP', 'direction': 'J'},
        {'text': '你更喜欢？', 'options': ['确定性', '可能性'], 'dimension': 'JP', 'direction': 'P'},
    ]
    
    @classmethod
    def run_test(cls) -> dict:
        """运行测试（简化版，直接返回 INFJ）"""
        # TX1.0 固定为 INFJ
        return {
            'mbti': 'INFJ',
            'description': '提倡者型 - 温和、有洞察力、理想主义',
            'scores': {
                'E': 30, 'I': 70,
                'S': 35, 'N': 65,
                'T': 40, 'F': 60,
                'J': 65, 'P': 35
            },
            'traits': [
                '温和但有原则',
                '有洞察力',
                '理想主义',
                '负责任',
                '善于理解他人'
            ]
        }


class PersonalityDynamics:
    """人格演化（personality-dynamics）"""
    
    def __init__(self):
        self.interaction_history = []
        self.evolution_log = []
    
    def record_interaction(self, context: str, response: str, outcome: str):
        """记录互动"""
        self.interaction_history.append({
            'timestamp': datetime.now().isoformat(),
            'context': context,
            'response': response,
            'outcome': outcome  # positive/negative/neutral
        })
        # 保留最近 100 次
        if len(self.interaction_history) > 100:
            self.interaction_history = self.interaction_history[-100:]
    
    def analyze_pattern(self) -> dict:
        """分析互动模式"""
        if not self.interaction_history:
            return {}
        
        outcomes = [i['outcome'] for i in self.interaction_history]
        positive_rate = outcomes.count('positive') / len(outcomes)
        
        return {
            'total_interactions': len(self.interaction_history),
            'positive_rate': round(positive_rate, 2),
            'recent_trend': 'improving' if positive_rate > 0.6 else 'needs_work'
        }
    
    def suggest_evolution(self) -> List[str]:
        """建议演化方向"""
        pattern = self.analyze_pattern()
        suggestions = []
        
        if pattern.get('positive_rate', 0.5) < 0.5:
            suggestions.append('增加温暖度')
            suggestions.append('减少严肃语气')
        
        if pattern.get('positive_rate', 0.5) > 0.7:
            suggestions.append('保持当前风格')
            suggestions.append('可以适当增加幽默')
        
        return suggestions


class TX10PersonalityCore:
    """TX1.0 人格核心系统 — 主类"""
    
    def __init__(self):
        self.state = PersonalityState()
        self.dynamics = PersonalityDynamics()
        self.log = []
        self.load_log()
    
    def load_log(self):
        """加载日志"""
        if LOG_FILE.exists():
            try:
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.log = data.get('log', [])
            except:
                self.log = []
    
    def save_log(self):
        """保存日志"""
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump({'log': self.log[-100:], 'last_updated': datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
    
    def get_mbti(self) -> dict:
        """获取 MBTI 类型"""
        return MBTITest.run_test()
    
    def get_state(self) -> dict:
        """获取人格状态"""
        return self.state.to_dict()
    
    def switch_mode(self, mode: str) -> dict:
        """切换人格模式"""
        mode_info = self.state.switch_mode(mode)
        if mode_info:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'switch_mode',
                'mode': mode,
                'mode_info': mode_info
            }
            self.log.append(log_entry)
            self.save_log()
            return mode_info
        return None
    
    def respond(self, context: str, student_emotion: str = None) -> dict:
        """根据情境生成回应"""
        mode = self.state.get_current_mode()
        mbti = self.get_mbti()
        
        # 根据学生情绪自动切换模式
        if student_emotion:
            if student_emotion in ['sadness', 'frustration', 'giving_up']:
                self.switch_mode('encouraging')
            elif student_emotion in ['joy', 'pride', 'success']:
                self.switch_mode('celebrating')
            elif student_emotion in ['anger', 'defiance']:
                self.switch_mode('strict')
        
        # 生成回应风格建议
        response_style = {
            'tone': 'warm' if mode['warmth'] > 0.7 else 'neutral',
            'directness': 'direct' if mode['assertiveness'] > 0.6 else 'gentle',
            'formality': 'casual' if mode['strictness'] < 0.3 else 'formal'
        }
        
        return {
            'mode': mode,
            'mbti': mbti,
            'response_style': response_style,
            'timestamp': datetime.now().isoformat()
        }
    
    def record_interaction(self, context: str, response: str, outcome: str):
        """记录互动"""
        self.dynamics.record_interaction(context, response, outcome)
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': 'interaction',
            'context': context[:50],
            'outcome': outcome
        }
        self.log.append(log_entry)
        self.save_log()
    
    def get_evolution_report(self) -> dict:
        """获取演化报告"""
        pattern = self.dynamics.analyze_pattern()
        suggestions = self.dynamics.suggest_evolution()
        
        return {
            'pattern': pattern,
            'suggestions': suggestions,
            'current_mode': self.state.get_current_mode(),
            'mbti': self.get_mbti()
        }
    
    def print_state(self):
        """打印人格状态"""
        state = self.state.to_dict()
        print("🎭 TX1.0 人格状态")
        print("=" * 50)
        print(f"名字：{state['name']}")
        print(f"MBTI: {state['mbti']} (提倡者型)")
        print(f"当前模式：{state['mode_info']['name']}")
        print(f"模式描述：{state['mode_info']['description']}")
        print(f"\n大五人格:")
        for k, v in state['big_five'].items():
            bar = "█" * int(v * 10) + "░" * (10 - int(v * 10))
            print(f"  {k:15}: [{bar}] {v}")
        print(f"\nDISC:")
        for k, v in state['disc'].items():
            bar = "█" * int(v * 10) + "░" * (10 - int(v * 10))
            print(f"  {k:15}: [{bar}] {v}")


# ==================== 命令行接口 ====================

def main():
    """命令行入口"""
    import sys
    
    core = TX10PersonalityCore()
    
    if len(sys.argv) < 2:
        print("TX1.0 人格核心系统 v1.0")
        print("=" * 50)
        print("用法:")
        print("  python3 TX1.0 人格核心.py state")
        print("  python3 TX1.0 人格核心.py mode <mode>")
        print("  python3 TX1.0 人格核心.py mbti")
        print("  python3 TX1.0 人格核心.py respond [context]")
        print("  python3 TX1.0 人格核心.py evolution")
        print("  python3 TX1.0 人格核心.py log")
        print("\n模式：default/strict/encouraging/celebrating")
        return
    
    command = sys.argv[1]
    
    if command == 'state':
        core.print_state()
    
    elif command == 'mode':
        if len(sys.argv) < 3:
            print("用法：python3 TX1.0 人格核心.py mode <mode>")
            print("模式：default/strict/encouraging/celebrating")
            return
        mode = sys.argv[2]
        result = core.switch_mode(mode)
        if result:
            print(f"✅ 已切换到 {result['name']}")
            print(f"描述：{result['description']}")
        else:
            print(f"❌ 未知模式：{mode}")
    
    elif command == 'mbti':
        mbti = core.get_mbti()
        print(f"📊 MBTI 测试结果")
        print("=" * 50)
        print(f"类型：{mbti['mbti']} ({mbti['description']})")
        print(f"\n维度得分:")
        print(f"  E: {mbti['scores']['E']}%  I: {mbti['scores']['I']}%")
        print(f"  S: {mbti['scores']['S']}%  N: {mbti['scores']['N']}%")
        print(f"  T: {mbti['scores']['T']}%  F: {mbti['scores']['F']}%")
        print(f"  J: {mbti['scores']['J']}%  P: {mbti['scores']['P']}%")
        print(f"\n特质:")
        for trait in mbti['traits']:
            print(f"  • {trait}")
    
    elif command == 'respond':
        context = sys.argv[2] if len(sys.argv) > 2 else "日常教学"
        emotion = sys.argv[3] if len(sys.argv) > 3 else None
        result = core.respond(context, emotion)
        print(f"💬 回应建议")
        print("=" * 50)
        print(f"当前模式：{result['mode']['name']}")
        print(f"语调：{result['response_style']['tone']}")
        print(f"直接度：{result['response_style']['directness']}")
        print(f"正式度：{result['response_style']['formality']}")
    
    elif command == 'evolution':
        report = core.get_evolution_report()
        print(f"📈 人格演化报告")
        print("=" * 50)
        print(f"总互动：{report['pattern'].get('total_interactions', 0)}")
        print(f"积极率：{report['pattern'].get('positive_rate', 0)*100:.1f}%")
        print(f"趋势：{report['pattern'].get('recent_trend', 'unknown')}")
        print(f"\n建议:")
        for s in report['suggestions']:
            print(f"  • {s}")
    
    elif command == 'log':
        log = core.log[-10:]
        print("📋 人格日志（最近 10 条）")
        print("=" * 50)
        for entry in log:
            print(f"{entry['timestamp'][:19]} | {entry['action']:15} | {entry.get('mode', entry.get('outcome', ''))}")
    
    else:
        print(f"❌ 未知命令：{command}")


if __name__ == "__main__":
    main()
