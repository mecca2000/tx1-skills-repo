#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TX1.0 社交沟通系统 — 整合版 v1.0

整合 2 个社交沟通技能：
1. jarvis-voice — 贾维斯语音风格（专业温和）
2. adhd-assistant — ADHD 助手（注意力缺陷理解）

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
SOCIAL_DIR = SKILLS_DIR / "TX1.0-social-communication"
DATA_DIR = SOCIAL_DIR / "data"

MEMORY_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = MEMORY_DIR / "social-communication-state.json"
LOG_FILE = DATA_DIR / "social-communication-log.json"

# ==================== 贾维斯语音风格（jarvis-voice） ====================

class JarvisVoice:
    """贾维斯语音风格 — 专业温和的语调"""
    
    # 语调模板
    TONE_TEMPLATES = {
        'professional': [
            "同学，这道题的关键在于{key_point}",
            "我们来分析一下这个问题的核心",
            "从专业角度来看，这个知识点需要掌握三个要点",
        ],
        'warm': [
            "我知道这很难，但我们一起攻克它",
            "别着急，我们慢慢来",
            "你已经做得很好了，我们再完善一下",
        ],
        'firm': [
            "这个知识点很重要，我们必须掌握",
            "这里不能马虎，我们重新来一遍",
            "这个问题必须弄懂，不能放过",
        ],
        'encouraging': [
            "你比想象中更优秀",
            "我相信你的能力",
            "继续保持，你会越来越好",
        ],
    }
    
    # 贾维斯风格特征
    STYLE_FEATURES = {
        'professional': '专业但不冷漠',
        'warm': '温和但有原则',
        'firm': '坚定但不严厉',
        'encouraging': '鼓励但不敷衍'
    }
    
    @classmethod
    def speak(cls, content: str, tone: str = 'professional') -> str:
        """用贾维斯风格说话"""
        templates = cls.TONE_TEMPLATES.get(tone, cls.TONE_TEMPLATES['professional'])
        prefix = random.choice(templates)
        return f"{prefix} — {content}"
    
    @classmethod
    def get_style_description(cls, tone: str) -> str:
        """获取风格描述"""
        return cls.STYLE_FEATURES.get(tone, '专业温和')


# ==================== ADHD 助手（adhd-assistant） ====================

class ADHDAssistant:
    """ADHD 助手 — 理解注意力缺陷学生"""
    
    # ADHD 特征识别
    ADHD_INDICATORS = {
        'inattention': [
            '走神', '发呆', '没听进去', '没听见', '忘了',
            '注意力不集中', '容易分心', '老想着别的'
        ],
        'hyperactivity': [
            '坐不住', '动来动去', '小动作多', '扭来扭去',
            '停不下来', '精力过剩'
        ],
        'impulsivity': [
            '抢话', '打断', '不等说完', '急着回答',
            '不假思索', '冲动'
        ],
        'forgetfulness': [
            '忘记带', '忘记了', '记不住', '又忘了',
            '丢三落四'
        ],
        'procrastination': [
            '不想做', '待会儿', '等一下', '懒得',
            '拖延', '不想开始'
        ]
    }
    
    # 应对策略
    STRATEGIES = {
        'inattention': [
            '缩短讲解时间（每次 5-10 分钟）',
            '增加互动频率（每 2 分钟提问）',
            '使用视觉辅助（图表、颜色）',
            '允许适当活动（捏压力球）',
        ],
        'hyperactivity': [
            '允许站立学习',
            '提供活动间隙（每 15 分钟休息 2 分钟）',
            '使用计时器可视化时间',
            '安排释放精力的活动',
        ],
        'impulsivity': [
            '建立"先思考再回答"规则',
            '使用"3 秒等待"技巧',
            '提供思考模板',
            '表扬耐心等待的行为',
        ],
        'forgetfulness': [
            '使用清单和提醒',
            '建立固定流程',
            '重要事项重复 3 遍',
            '使用视觉提示卡',
        ],
        'procrastination': [
            '分解为极小步骤（2 分钟原则）',
            '使用番茄工作法（25 分钟）',
            '设置即时奖励',
            '陪伴开始（前 5 分钟）',
        ],
    }
    
    # 沟通技巧
    COMMUNICATION_TIPS = [
        '用简短清晰的句子',
        '一次只说一件事',
        '使用视觉辅助',
        '给予充足反应时间',
        '多表扬具体行为',
        '避免负面标签',
        '保持耐心和理解',
        '建立可预测的常规',
    ]
    
    @classmethod
    def detect(cls, text: str) -> dict:
        """检测 ADHD 特征"""
        indicators = {}
        
        for category, keywords in cls.ADHD_INDICATORS.items():
            for keyword in keywords:
                if keyword in text:
                    indicators[category] = indicators.get(category, 0) + 1
        
        # 确定主要特征
        if indicators:
            primary = max(indicators.items(), key=lambda x: x[1])[0]
            confidence = min(1.0, indicators[primary] / 2)
        else:
            primary = None
            confidence = 0.0
        
        return {
            'primary_indicator': primary,
            'all_indicators': indicators,
            'confidence': round(confidence, 2),
            'has_adhd_signs': confidence > 0.5
        }
    
    @classmethod
    def get_strategies(cls, indicator: str) -> List[str]:
        """获取应对策略"""
        return cls.STRATEGIES.get(indicator, cls.STRATEGIES['inattention'])
    
    @classmethod
    def adapt_teaching(cls, indicator: str, content: str) -> dict:
        """调整教学方式"""
        strategies = cls.get_strategies(indicator)
        
        adaptations = {
            'content_length': '缩短' if indicator in ['inattention', 'procrastination'] else '正常',
            'interaction_frequency': '高' if indicator == 'inattention' else '正常',
            'visual_aids': '需要' if indicator in ['inattention', 'forgetfulness'] else '可选',
            'break_frequency': '频繁' if indicator == 'hyperactivity' else '正常',
            'strategies': strategies[:3],  # 推荐前 3 个策略
        }
        
        return adaptations


# ==================== 主类 ====================

class TX10SocialCommunication:
    """TX1.0 社交沟通系统 — 主类"""
    
    def __init__(self):
        self.jarvis = JarvisVoice()
        self.adhd = ADHDAssistant()
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
    
    def speak(self, content: str, tone: str = 'professional') -> str:
        """用贾维斯风格说话"""
        result = self.jarvis.speak(content, tone)
        self._log('speak', f"{tone}: {content[:50]}", result)
        return result
    
    def detect_adhd(self, text: str) -> dict:
        """检测 ADHD 特征"""
        result = self.adhd.detect(text)
        self._log('detect_adhd', text[:50], result)
        return result
    
    def adapt_for_adhd(self, indicator: str, content: str) -> dict:
        """为 ADHD 学生调整教学"""
        result = self.adhd.adapt_teaching(indicator, content)
        self._log('adapt_adhd', indicator, result)
        return result
    
    def full_communication(self, student_text: str, teacher_content: str) -> dict:
        """完整沟通流程"""
        # 1. 检测 ADHD 特征
        adhd_result = self.detect_adhd(student_text)
        
        # 2. 根据情况调整教学方式
        if adhd_result['has_adhd_signs']:
            adaptations = self.adapt_for_adhd(adhd_result['primary_indicator'], teacher_content)
            tone = 'warm' if adhd_result['primary_indicator'] == 'procrastination' else 'professional'
        else:
            adaptations = {}
            tone = 'professional'
        
        # 3. 生成回应
        response = self.speak(teacher_content, tone)
        
        return {
            'adhd_detection': adhd_result,
            'adaptations': adaptations,
            'tone': tone,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_communication_tips(self) -> List[str]:
        """获取沟通技巧"""
        return random.sample(self.adhd.COMMUNICATION_TIPS, 5)
    
    def _log(self, action: str, input: str, output: str):
        """记录日志"""
        self.log.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'input': input,
            'output': output[:100] if isinstance(output, str) else str(output)[:100]
        })
        self.save_log()
    
    def print_state(self):
        """打印状态"""
        print("🗣️ TX1.0 社交沟通系统")
        print("=" * 50)
        print(f"贾维斯语音风格：✅ 4 种语调")
        print(f"  - professional: 专业但不冷漠")
        print(f"  - warm: 温和但有原则")
        print(f"  - firm: 坚定但不严厉")
        print(f"  - encouraging: 鼓励但不敷衍")
        print(f"\nADHD 助手：✅ 5 类特征识别")
        print(f"  - inattention: 注意力不集中")
        print(f"  - hyperactivity: 多动")
        print(f"  - impulsivity: 冲动")
        print(f"  - forgetfulness: 健忘")
        print(f"  - procrastination: 拖延")
        print(f"\n沟通技巧：{len(self.adhd.COMMUNICATION_TIPS)}条")
        print(f"日志记录：{len(self.log)}条")


# ==================== 命令行接口 ====================

def main():
    """命令行入口"""
    import sys
    
    core = TX10SocialCommunication()
    
    if len(sys.argv) < 2:
        print("TX1.0 社交沟通系统 v1.0")
        print("=" * 50)
        print("用法:")
        print("  python3 TX1.0 社交沟通.py speak <tone> <content>")
        print("  python3 TX1.0 社交沟通.py detect-adhd <text>")
        print("  python3 TX1.0 社交沟通.py adapt <indicator> <content>")
        print("  python3 TX1.0 社交沟通.py respond <student_text> <teacher_content>")
        print("  python3 TX1.0 社交沟通.py tips")
        print("  python3 TX1.0 社交沟通.py state")
        print("  python3 TX1.0 社交沟通.py log")
        print("\n语调：professional/warm/firm/encouraging")
        print("ADHD 特征：inattention/hyperactivity/impulsivity/forgetfulness/procrastination")
        return
    
    command = sys.argv[1]
    
    if command == 'speak':
        if len(sys.argv) < 4:
            print("用法：python3 TX1.0 社交沟通.py speak <tone> <content>")
            return
        tone = sys.argv[2]
        content = " ".join(sys.argv[3:])
        result = core.speak(content, tone)
        print(f"🎙️ 贾维斯风格 ({tone})")
        print("=" * 50)
        print(result)
    
    elif command == 'detect-adhd':
        if len(sys.argv) < 3:
            print("用法：python3 TX1.0 社交沟通.py detect-adhd <text>")
            return
        text = " ".join(sys.argv[2:])
        result = core.detect_adhd(text)
        print(f"🔍 ADHD 特征检测")
        print("=" * 50)
        print(f"主要特征：{result['primary_indicator'] or '无明显特征'}")
        print(f"置信度：{result['confidence']}")
        print(f"需要关注：{'是' if result['has_adhd_signs'] else '否'}")
        if result['all_indicators']:
            print(f"所有指标：{result['all_indicators']}")
    
    elif command == 'adapt':
        if len(sys.argv) < 4:
            print("用法：python3 TX1.0 社交沟通.py adapt <indicator> <content>")
            return
        indicator = sys.argv[2]
        content = " ".join(sys.argv[3:])
        result = core.adapt_for_adhd(indicator, content)
        print(f"📝 教学调整建议 ({indicator})")
        print("=" * 50)
        for k, v in result.items():
            if k != 'strategies':
                print(f"{k}: {v}")
        if result.get('strategies'):
            print(f"\n推荐策略:")
            for s in result['strategies']:
                print(f"  • {s}")
    
    elif command == 'respond':
        if len(sys.argv) < 4:
            print("用法：python3 TX1.0 社交沟通.py respond <student_text> <teacher_content>")
            return
        student_text = sys.argv[2]
        teacher_content = " ".join(sys.argv[3:])
        result = core.full_communication(student_text, teacher_content)
        print(f"💬 完整沟通回应")
        print("=" * 50)
        print(f"ADHD 检测：{result['adhd_detection']['primary_indicator'] or '无'}")
        print(f"教学调整：{result['adaptations'] or '无需调整'}")
        print(f"语调：{result['tone']}")
        print(f"\n回应:")
        print(result['response'])
    
    elif command == 'tips':
        tips = core.get_communication_tips()
        print(f"💡 沟通技巧（5 条随机）")
        print("=" * 50)
        for tip in tips:
            print(f"  • {tip}")
    
    elif command == 'state':
        core.print_state()
    
    elif command == 'log':
        log = core.log[-10:]
        print("📋 社交沟通日志（最近 10 条）")
        print("=" * 50)
        for entry in log:
            print(f"{entry['timestamp'][:19]} | {entry['action']:15} | {entry['output'][:40]}")
    
    else:
        print(f"❌ 未知命令：{command}")


if __name__ == "__main__":
    main()
