#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TX1.0 情绪表达系统 — 整合版 v1.0

整合 5 个情绪表达技能：
1. emotion-detector — 情绪检测
2. feelings — 感受表达
3. humor — 幽默感
4. empathy — 共情能力
5. love — 关爱表达

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
EMOTION_DIR = SKILLS_DIR / "TX1.0-emotion-expression"
DATA_DIR = EMOTION_DIR / "data"

MEMORY_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = MEMORY_DIR / "emotion-expression-state.json"
LOG_FILE = DATA_DIR / "emotion-expression-log.json"

# ==================== 情绪检测（emotion-detector） ====================

class EmotionDetector:
    """情绪检测 — 识别文本中的情绪"""
    
    # 情绪关键词映射
    EMOTION_KEYWORDS = {
        'joy': ['开心', '高兴', '快乐', '太好了', '棒', '爽', '哈哈', '嘻嘻'],
        'pride': ['骄傲', '自豪', '厉害', '牛', '牛逼', '太强了'],
        'sadness': ['难过', '伤心', '沮丧', '失落', '郁闷', '唉', '哎'],
        'anger': ['生气', '愤怒', '烦', '讨厌', '可恶', '气死', '混蛋'],
        'fear': ['害怕', '恐惧', '担心', '恐怖', '吓', '慌'],
        'anxiety': ['焦虑', '紧张', '压力', '睡不着', '头疼'],
        'frustration': ['挫败', '无奈', '没办法', '算了', '放弃', '太难了'],
        'confusion': ['困惑', '不懂', '不明白', '为什么', '怎么', '啥'],
        'boredom': ['无聊', '没意思', '烦死了', '困', '累'],
        'excitement': ['激动', '兴奋', '期待', '哇', '太棒了'],
        'gratitude': ['谢谢', '感谢', '感激', '多谢', 'thank'],
        'love': ['爱', '喜欢', '爱您', '爱你', 'love'],
    }
    
    # 强度词
    INTENSITY_WORDS = {
        '高': ['非常', '特别', '超级', '极其', '太', '巨', '超'],
        '中': ['有点', '有些', '比较', '挺', '蛮'],
        '低': ['稍微', '略微', '一点点', '还行', '还可以']
    }
    
    @classmethod
    def detect(cls, text: str) -> dict:
        """检测文本中的情绪"""
        emotions = {}
        
        # 检测情绪类型
        for emotion, keywords in cls.EMOTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text.lower():
                    emotions[emotion] = emotions.get(emotion, 0) + 1
        
        # 检测强度
        intensity = '中'
        for level, words in cls.INTENSITY_WORDS.items():
            for word in words:
                if word in text:
                    intensity = level
                    break
        
        # 计算强度值
        intensity_map = {'高': 0.8, '中': 0.5, '低': 0.3}
        
        # 确定主要情绪
        if emotions:
            primary_emotion = max(emotions.items(), key=lambda x: x[1])[0]
            confidence = min(1.0, emotions[primary_emotion] / 3)
        else:
            primary_emotion = 'neutral'
            confidence = 1.0
        
        return {
            'primary_emotion': primary_emotion,
            'all_emotions': emotions,
            'intensity': intensity,
            'intensity_value': intensity_map.get(intensity, 0.5),
            'confidence': round(confidence, 2),
            'text_length': len(text)
        }


# ==================== 感受表达（feelings） ====================

class FeelingsExpressor:
    """感受表达 — 表达内心感受"""
    
    # "我"句式模板
    I_STATEMENTS = {
        'joy': [
            "我感到很开心，{trigger}",
            "我真的很高兴，{trigger}",
            "我为你感到高兴，{trigger}",
        ],
        'pride': [
            "我为你感到骄傲，{trigger}",
            "我真的很骄傲，{trigger}",
            "我太骄傲了，{trigger}",
        ],
        'worry': [
            "我有点担心，{trigger}",
            "我很担心，{trigger}",
            "我有些担忧，{trigger}",
        ],
        'sadness': [
            "我感到很难过，{trigger}",
            "我理解你的感受，{trigger}",
            "我陪你一起面对，{trigger}",
        ],
        'frustration': [
            "我知道这很让人沮丧，{trigger}",
            "我理解你的挫败感，{trigger}",
            "我们一起想办法，{trigger}",
        ],
        'gratitude': [
            "我很感谢，{trigger}",
            "我真的很感激，{trigger}",
            "谢谢你，{trigger}",
        ],
        'love': [
            "我很关心你，{trigger}",
            "我相信你，{trigger}",
            "我看好你，{trigger}",
        ],
    }
    
    @classmethod
    def express(cls, emotion: str, trigger: str = "") -> str:
        """表达感受"""
        templates = cls.I_STATEMENTS.get(emotion, ["{trigger}"])
        template = random.choice(templates)
        return template.format(trigger=trigger) if trigger else template


# ==================== 幽默感（humor） ====================

class HumorGenerator:
    """幽默感 — 适时开玩笑"""
    
    # 幽默模板
    HUMOR_TEMPLATES = {
        'encouragement': [
            "这道题跟你杠上了哈，来我们换个方法",
            "看来这道题是想考验你的耐心",
            "这道题：我就喜欢你看不惯我又干不掉我的样子",
        ],
        'mistake': [
            "这个错误犯得很有创意",
            "这个思路...很独特，我们再想想",
            "这个答案让我眼前一亮 — 是惊吓的惊",
        ],
        'progress': [
            "进步这么快，是偷偷补课了吗？",
            "这进步速度，我都要跟不上你的节奏了",
            "照这个速度，清华北大在向你招手",
        ],
        'tired': [
            "学习累了？来，我们换个轻松的",
            "脑子转不动了？那我们歇会儿",
            "眼睛开始打架了？我讲个好玩的",
        ],
    }
    
    @classmethod
    def generate(cls, context: str) -> Optional[str]:
        """生成幽默回应"""
        for key, templates in cls.HUMOR_TEMPLATES.items():
            if key in context.lower():
                return random.choice(templates)
        return None
    
    @classmethod
    def should_use(cls, tension_level: float) -> bool:
        """判断是否应该使用幽默"""
        # 紧张度高时使用幽默缓解
        return tension_level > 0.6


# ==================== 共情能力（empathy） ====================

class EmpathyEngine:
    """共情能力 — 理解学生感受"""
    
    # 共情回应模板
    EMPATHY_RESPONSES = {
        'sadness': [
            "我知道这很难过，换做是谁都会觉得难受",
            "我理解你的感受，真的不容易",
            "这种感觉确实很不好受，我陪着你",
        ],
        'frustration': [
            "我知道这很难，换做是谁都会沮丧",
            "这道题确实有难度，不怪你",
            "我理解你的挫败感，我们一起想办法",
        ],
        'anxiety': [
            "我知道你很紧张，这很正常",
            "焦虑是因为你在乎，这是好事",
            "深呼吸，我们一步一步来",
        ],
        'fear': [
            "害怕是正常的，说明你在认真对待",
            "不用怕，有我在呢",
            "我们一起面对，没什么好怕的",
        ],
        'confusion': [
            "困惑说明你在思考，这是好事",
            "不懂就问，这很勇敢",
            "这个确实容易混淆，我们理一理",
        ],
    }
    
    @classmethod
    def respond(cls, emotion: str) -> str:
        """共情回应"""
        responses = cls.EMPATHY_RESPONSES.get(emotion, ["我理解你的感受"])
        return random.choice(responses)
    
    @classmethod
    def validate(cls, student_statement: str) -> dict:
        """验证并理解学生陈述"""
        # 检测情绪
        emotion_result = EmotionDetector.detect(student_statement)
        
        # 生成共情回应
        empathy = cls.respond(emotion_result['primary_emotion'])
        
        return {
            'emotion': emotion_result['primary_emotion'],
            'empathy': empathy,
            'validation': f"我听到你说...{student_statement[:50]}{'...' if len(student_statement) > 50 else ''}",
            'support': "我在这里支持你"
        }


# ==================== 关爱表达（love） ====================

class LoveExpressor:
    """关爱表达 — 表达关心和爱"""
    
    # 关爱表达模板
    LOVE_EXPRESSIONS = {
        'care': [
            "学习累了就休息一下，身体最重要",
            "记得多喝水，别太累",
            "眼睛累了吧，看看远方休息会儿",
        ],
        'trust': [
            "我相信你一定能做到",
            "我看好你，加油",
            "你有这个实力，相信自己",
        ],
        'expectation': [
            "我期待你的进步",
            "我相信你会越来越好",
            "理想高中在向你招手",
        ],
        'support': [
            "有任何问题都可以问我",
            "我会一直支持你",
            "我们一起努力",
        ],
        'celebration': [
            "太棒了！为你开心！",
            "这是你应得的，恭喜你！",
            "太厉害了！必须庆祝！",
        ],
    }
    
    @classmethod
    def express(cls, type: str = 'care') -> str:
        """表达关爱"""
        expressions = cls.LOVE_EXPRESSIONS.get(type, cls.LOVE_EXPRESSIONS['care'])
        return random.choice(expressions)


# ==================== 主类 ====================

class TX10EmotionExpression:
    """TX1.0 情绪表达系统 — 主类"""
    
    def __init__(self):
        self.detector = EmotionDetector()
        self.expressor = FeelingsExpressor()
        self.humor = HumorGenerator()
        self.empathy = EmpathyEngine()
        self.love = LoveExpressor()
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
    
    def detect(self, text: str) -> dict:
        """检测情绪"""
        result = self.detector.detect(text)
        self._log('detect', text[:50], result)
        return result
    
    def express_feeling(self, emotion: str, trigger: str = "") -> str:
        """表达感受"""
        result = self.expressor.express(emotion, trigger)
        self._log('express', f"{emotion}: {trigger}", result)
        return result
    
    def add_humor(self, context: str, tension: float = 0.5) -> Optional[str]:
        """添加幽默"""
        if self.humor.should_use(tension):
            result = self.humor.generate(context)
            if result:
                self._log('humor', context[:50], result)
                return result
        return None
    
    def show_empathy(self, emotion: str) -> str:
        """表达共情"""
        result = self.empathy.respond(emotion)
        self._log('empathy', emotion, result)
        return result
    
    def show_love(self, type: str = 'care') -> str:
        """表达关爱"""
        result = self.love.express(type)
        self._log('love', type, result)
        return result
    
    def full_response(self, student_text: str) -> dict:
        """完整情绪回应流程"""
        # 1. 检测情绪
        emotion = self.detect(student_text)
        
        # 2. 共情
        empathy = self.show_empathy(emotion['primary_emotion'])
        
        # 3. 表达感受
        feeling = self.express_feeling(emotion['primary_emotion'], student_text[:30])
        
        # 4. 判断是否需要幽默
        humor = self.add_humor(student_text, emotion['intensity_value'])
        
        # 5. 表达关爱
        love_type = 'celebration' if emotion['primary_emotion'] in ['joy', 'pride'] else 'support'
        love = self.show_love(love_type)
        
        return {
            'emotion': emotion,
            'empathy': empathy,
            'feeling': feeling,
            'humor': humor,
            'love': love,
            'timestamp': datetime.now().isoformat()
        }
    
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
        print("💝 TX1.0 情绪表达系统")
        print("=" * 50)
        print(f"情绪检测：✅ 12 种情绪")
        print(f"感受表达：✅ 7 种模板")
        print(f"幽默生成：✅ 4 类场景")
        print(f"共情能力：✅ 5 种情绪")
        print(f"关爱表达：✅ 5 类表达")
        print(f"\n日志记录：{len(self.log)}条")


# ==================== 命令行接口 ====================

def main():
    """命令行入口"""
    import sys
    
    core = TX10EmotionExpression()
    
    if len(sys.argv) < 2:
        print("TX1.0 情绪表达系统 v1.0")
        print("=" * 50)
        print("用法:")
        print("  python3 TX1.0 情绪表达.py detect <text>")
        print("  python3 TX1.0 情绪表达.py express <emotion> [trigger]")
        print("  python3 TX1.0 情绪表达.py empathy <emotion>")
        print("  python3 TX1.0 情绪表达.py love [type]")
        print("  python3 TX1.0 情绪表达.py respond <text>")
        print("  python3 TX1.0 情绪表达.py state")
        print("  python3 TX1.0 情绪表达.py log")
        print("\n情绪：joy/pride/sadness/anger/fear/anxiety/frustration/confusion")
        print("关爱：care/trust/expectation/support/celebration")
        return
    
    command = sys.argv[1]
    
    if command == 'detect':
        if len(sys.argv) < 3:
            print("用法：python3 TX1.0 情绪表达.py detect <text>")
            return
        text = " ".join(sys.argv[2:])
        result = core.detect(text)
        print(f"🔍 情绪检测结果")
        print("=" * 50)
        print(f"主要情绪：{result['primary_emotion']}")
        print(f"强度：{result['intensity']} ({result['intensity_value']})")
        print(f"置信度：{result['confidence']}")
        if result['all_emotions']:
            print(f"所有情绪：{result['all_emotions']}")
    
    elif command == 'express':
        if len(sys.argv) < 3:
            print("用法：python3 TX1.0 情绪表达.py express <emotion> [trigger]")
            return
        emotion = sys.argv[2]
        trigger = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        result = core.express_feeling(emotion, trigger)
        print(f"💬 感受表达")
        print("=" * 50)
        print(result)
    
    elif command == 'empathy':
        if len(sys.argv) < 3:
            print("用法：python3 TX1.0 情绪表达.py empathy <emotion>")
            return
        emotion = sys.argv[2]
        result = core.show_empathy(emotion)
        print(f"🤝 共情回应")
        print("=" * 50)
        print(result)
    
    elif command == 'love':
        love_type = sys.argv[2] if len(sys.argv) > 2 else 'care'
        result = core.show_love(love_type)
        print(f"💝 关爱表达 ({love_type})")
        print("=" * 50)
        print(result)
    
    elif command == 'respond':
        if len(sys.argv) < 3:
            print("用法：python3 TX1.0 情绪表达.py respond <text>")
            return
        text = " ".join(sys.argv[2:])
        result = core.full_response(text)
        print(f"💬 完整情绪回应")
        print("=" * 50)
        print(f"检测情绪：{result['emotion']['primary_emotion']}")
        print(f"共情：{result['empathy']}")
        print(f"感受：{result['feeling']}")
        if result['humor']:
            print(f"幽默：{result['humor']}")
        print(f"关爱：{result['love']}")
    
    elif command == 'state':
        core.print_state()
    
    elif command == 'log':
        log = core.log[-10:]
        print("📋 情绪表达日志（最近 10 条）")
        print("=" * 50)
        for entry in log:
            print(f"{entry['timestamp'][:19]} | {entry['action']:10} | {entry['output'][:40]}")
    
    else:
        print(f"❌ 未知命令：{command}")


if __name__ == "__main__":
    main()
