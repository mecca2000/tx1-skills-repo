#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TX1.0 教育心理学技能 v1.0

整合两本经典教育心理学著作：
1. 《教育心理学》（桑代克）- 学习定律、个体差异
2. 《教育心理学：理论与实践》（斯滕伯格）- 认知发展、学习动机

作者：TX1.0（基于教育心理学经典理论）
创建时间：2026-03-19
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ==================== 配置 ====================

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"
PSYCH_DIR = SKILLS_DIR / "TX1.0-educational-psychology"
DATA_DIR = PSYCH_DIR / "data"

MEMORY_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = MEMORY_DIR / "educational-psychology.json"
STUDENT_PROFILE_FILE = DATA_DIR / "student-profiles.json"

# ==================== 核心理论 ====================

class LearningTheories:
    """学习理论库（基于桑代克、斯滕伯格等）"""
    
    # 桑代克三大学习定律
    THORNDIKE_LAWS = {
        'preparedness': {
            'name': '准备律',
            'description': '学习者身心准备状态影响学习效果',
            'application': '教学前确保学生准备好（知识基础、心理状态）',
            'examples': [
                '预习后听课效果更好',
                '疲劳时学习效率低',
                '有动机时学习更主动'
            ]
        },
        'exercise': {
            'name': '练习律',
            'description': '刺激 - 反应联结通过练习而加强',
            'application': '提供充足练习机会，及时复习巩固',
            'examples': [
                '反复练习形成肌肉记忆',
                '间隔复习优于集中复习',
                '变式练习促进迁移'
            ]
        },
        'effect': {
            'name': '效果律',
            'description': '满意的结果强化联结，烦恼的结果削弱联结',
            'application': '及时正向反馈，让学生体验成功',
            'examples': [
                '答对题及时表扬',
                '小步前进体验成功',
                '减少挫败感'
            ]
        }
    }
    
    # 斯滕伯格智力三元论
    STERNBERG_INTELLIGENCE = {
        'analytical': {
            'name': '分析性智力',
            'description': '分析、评价、比较、对比的能力',
            'teaching_strategy': '逻辑推理题、批判性思维训练'
        },
        'creative': {
            'name': '创造性智力',
            'description': '创造、设计、发明、想象的能力',
            'teaching_strategy': '开放性问题、创意项目、头脑风暴'
        },
        'practical': {
            'name': '实践性智力',
            'description': '应用、使用、实施、操作的能力',
            'teaching_strategy': '实际问题解决、实验操作、社会实践'
        }
    }
    
    # 维果茨基最近发展区
    ZPD = {
        'name': '最近发展区 (ZPD)',
        'description': '学生现有水平与潜在发展水平之间的区域',
        'application': '教学应走在发展前面，提供适当支架',
        'scaffolding_steps': [
            '评估学生现有水平',
            '确定潜在发展水平',
            '提供适当支架（提示、示范）',
            '逐渐撤去支架',
            '学生独立完成'
        ]
    }
    
    # 布鲁纳发现学习
    DISCOVERY_LEARNING = {
        'name': '发现学习',
        'principles': [
            '学生是主动的问题解决者',
            '通过探索发现知识结构',
            '螺旋式课程（由简到繁）',
            '直觉思维与逻辑思维并重'
        ]
    }
    
    # 奥苏贝尔有意义学习
    MEANINGFUL_LEARNING = {
        'name': '有意义学习',
        'conditions': [
            '学习材料有逻辑意义',
            '学习者有有意义学习的心向',
            '学习者认知结构中有适当观念'
        ],
        'strategies': [
            '先行组织者（advance organizer）',
            '概念图',
            '类比教学'
        ]
    }


class MotivationStrategies:
    """学习动机策略"""
    
    # 马斯洛需求层次
    MASLOW_HIERARCHY = {
        'levels': [
            {'name': '生理需求', 'teaching': '确保基本舒适（温度、光线、休息）'},
            {'name': '安全需求', 'teaching': '营造安全心理环境，不嘲笑错误'},
            {'name': '归属与爱', 'teaching': '建立良好师生关系、同伴关系'},
            {'name': '尊重需求', 'teaching': '表扬进步、展示作品、赋予责任'},
            {'name': '自我实现', 'teaching': '设置挑战性目标、发挥潜能'}
        ]
    }
    
    # 德韦克成长型思维
    MINDSET = {
        'fixed': {
            'name': '固定型思维',
            'beliefs': ['智力是天生的', '努力说明能力差', '失败=我不行'],
            'language': ['你真聪明', '这对你来说很容易']
        },
        'growth': {
            'name': '成长型思维',
            'beliefs': ['智力可以发展', '努力是成长之路', '失败=学习机会'],
            'language': ['你的努力见效了', '这很难但你坚持了', '错误帮助学习']
        }
    }
    
    # 自我决定理论
    SELF_DETERMINATION = {
        'needs': [
            {'name': '自主感', 'strategy': '提供选择、解释原因、减少控制'},
            {'name': '胜任感', 'strategy': '适当挑战、及时反馈、小步成功'},
            {'name': '归属感', 'strategy': '关心学生、建立关系、合作学习'}
        ]
    }


class CognitiveStrategies:
    """认知策略库"""
    
    # 记忆策略
    MEMORY_STRATEGIES = {
        'rehearsal': {
            'name': '复述策略',
            'techniques': ['重复朗读', '抄写', '划线']
        },
        'elaboration': {
            'name': '精细加工策略',
            'techniques': ['记忆术', '做笔记', '类比', '提问', '总结']
        },
        'organization': {
            'name': '组织策略',
            'techniques': ['归类', '提纲', '概念图', '表格']
        }
    }
    
    # 元认知策略
    METACOGNITIVE_STRATEGIES = {
        'planning': {
            'name': '计划策略',
            'questions': [
                '这个任务的目标是什么？',
                '我需要哪些知识？',
                '我有多少时间？',
                '我应该用什么策略？'
            ]
        },
        'monitoring': {
            'name': '监控策略',
            'questions': [
                '我理解了吗？',
                '我的进度如何？',
                '这个策略有效吗？',
                '我需要调整吗？'
            ]
        },
        'evaluating': {
            'name': '评估策略',
            'questions': [
                '我达成目标了吗？',
                '哪些方法有效？',
                '下次如何改进？',
                '我学到了什么？'
            ]
        }
    }
    
    # 问题解决策略
    PROBLEM_SOLVING = {
        'steps': [
            '理解问题（已知什么？求什么？）',
            '制定计划（用什么方法？）',
            '执行计划（一步步求解）',
            '回顾反思（答案合理吗？有其他方法吗？）'
        ],
        'heuristics': [
            '画图',
            '列表',
            '逆向思考',
            '特殊化',
            '类比'
        ]
    }


class StudentDifferences:
    """个体差异与因材施教"""
    
    # 学习风格
    LEARNING_STYLES = {
        'visual': {
            'name': '视觉型',
            'characteristics': '通过看学习，喜欢图表、图像',
            'strategies': ['概念图', '流程图', '颜色标记', '视频']
        },
        'auditory': {
            'name': '听觉型',
            'characteristics': '通过听学习，喜欢讲解、讨论',
            'strategies': ['讲解', '讨论', '录音', '朗读']
        },
        'kinesthetic': {
            'name': '动觉型',
            'characteristics': '通过做学习，喜欢操作、实验',
            'strategies': ['实验', '操作', '角色扮演', '实地考察']
        }
    }
    
    # 多元智力（加德纳）
    MULTIPLE_INTELLIGENCES = {
        'linguistic': {'name': '语言智力', 'activities': ['写作', '辩论', '讲故事']},
        'logical': {'name': '逻辑数学智力', 'activities': ['解题', '实验', '推理']},
        'spatial': {'name': '空间智力', 'activities': ['绘图', '设计', '想象']},
        'musical': {'name': '音乐智力', 'activities': ['唱歌', '作曲', '节奏']},
        'bodily': {'name': '身体动觉智力', 'activities': ['运动', '舞蹈', '手工']},
        'interpersonal': {'name': '人际智力', 'activities': ['合作', '领导', '沟通']},
        'intrapersonal': {'name': '内省智力', 'activities': ['反思', '日记', '独立学习']},
        'naturalist': {'name': '自然观察智力', 'activities': ['观察', '分类', '探索自然']}
    }


# ==================== 主类 ====================

class TX10EducationalPsychology:
    """TX1.0 教育心理学技能 — 主类"""
    
    def __init__(self):
        self.learning_theories = LearningTheories()
        self.motivation = MotivationStrategies()
        self.cognitive = CognitiveStrategies()
        self.differences = StudentDifferences()
        self.student_profiles = {}
        self.load_profiles()
    
    def load_profiles(self):
        """加载学生档案"""
        if STUDENT_PROFILE_FILE.exists():
            try:
                with open(STUDENT_PROFILE_FILE, 'r', encoding='utf-8') as f:
                    self.student_profiles = json.load(f)
            except:
                self.student_profiles = {}
    
    def save_profiles(self):
        """保存学生档案"""
        with open(STUDENT_PROFILE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.student_profiles, f, ensure_ascii=False, indent=2)
    
    def analyze_student(self, student_id: str, behavior: str) -> dict:
        """
        分析学生行为（基于教育心理学理论）
        
        Args:
            student_id: 学生 ID
            behavior: 行为描述
        
        Returns:
            分析结果和建议
        """
        analysis = {
            'student_id': student_id,
            'behavior': behavior,
            'timestamp': datetime.now().isoformat(),
            'theories': [],
            'suggestions': []
        }
        
        # 行为模式识别
        if '不想学' in behavior or '放弃' in behavior:
            analysis['theories'].append({
                'theory': '效果律（桑代克）',
                'analysis': '学生可能缺乏成功体验，需要正向强化'
            })
            analysis['suggestions'].append('设置小目标，让学生体验成功')
            analysis['suggestions'].append('及时表扬进步，强化学习行为')
        
        if '走神' in behavior or '注意力' in behavior:
            analysis['theories'].append({
                'theory': '准备律（桑代克）',
                'analysis': '学生可能身心未准备好（疲劳、缺乏动机）'
            })
            analysis['suggestions'].append('检查学生状态，适当休息')
            analysis['suggestions'].append'激发学习兴趣，明确学习目标')
        
        if '听不懂' in behavior or '不会' in behavior:
            analysis['theories'].append({
                'theory': '最近发展区（维果茨基）',
                'analysis': '教学可能超出学生 ZPD，需要支架'
            })
            analysis['suggestions'].append('降低难度，提供支架（提示、示范）')
            analysis['suggestions'].append'分解任务，小步前进')
        
        if '笨' in behavior or '不行' in behavior:
            analysis['theories'].append({
                'theory': '成长型思维（德韦克）',
                'analysis': '学生可能有固定型思维，需要转变'
            })
            analysis['suggestions'].append('强调努力而非天赋（"你的努力见效了"）')
            analysis['suggestions'].append('将错误重构为学习机会')
        
        return analysis
    
    def get_teaching_strategy(self, situation: str) -> dict:
        """
        根据情境获取教学策略
        
        Args:
            situation: 教学情境描述
        
        Returns:
            推荐策略
        """
        strategies = {
            'timestamp': datetime.now().isoformat(),
            'situation': situation,
            'recommended': []
        }
        
        # 情境匹配
        if '新知识点' in situation:
            strategies['recommended'].append({
                'theory': '先行组织者（奥苏贝尔）',
                'strategy': '先提供上位概念，再学习具体内容'
            })
        
        if '复习' in situation:
            strategies['recommended'].append({
                'theory': '练习律（桑代克）',
                'strategy': '间隔复习优于集中复习'
            })
            strategies['recommended'].append({
                'theory': '精细加工策略',
                'strategy': '让学生总结、类比、提问'
            })
        
        if '动机不足' in situation or '不想学' in situation:
            strategies['recommended'].append({
                'theory': '自我决定理论',
                'strategy': '满足自主感、胜任感、归属感'
            })
            strategies['recommended'].append({
                'theory': '成长型思维',
                'strategy': '强调努力、策略、进步'
            })
        
        if '个体差异' in situation:
            strategies['recommended'].append({
                'theory': '多元智力（加德纳）',
                'strategy': '用多种方式呈现内容'
            })
        
        return strategies
    
    def create_learning_plan(self, student_profile: dict) -> dict:
        """
        创建个性化学习计划
        
        Args:
            student_profile: 学生档案（包含学习风格、智力类型等）
        
        Returns:
            个性化学习计划
        """
        plan = {
            'student_id': student_profile.get('id', 'unknown'),
            'created_at': datetime.now().isoformat(),
            'learning_style': student_profile.get('learning_style', 'unknown'),
            'intelligence_type': student_profile.get('intelligence_type', 'unknown'),
            'strategies': []
        }
        
        # 根据学习风格推荐策略
        style = student_profile.get('learning_style', 'visual')
        if style in self.differences.LEARNING_STYLES:
            plan['strategies'].append({
                'type': '学习风格匹配',
                'style': self.differences.LEARNING_STYLES[style]['name'],
                'techniques': self.differences.LEARNING_STYLES[style]['strategies']
            })
        
        # 根据智力类型推荐活动
        intel = student_profile.get('intelligence_type', 'logical')
        if intel in self.differences.MULTIPLE_INTELLIGENCES:
            plan['strategies'].append({
                'type': '智力类型匹配',
                'intelligence': self.differences.MULTIPLE_INTELLIGENCES[intel]['name'],
                'activities': self.differences.MULTIPLE_INTELLIGENCES[intel]['activities']
            })
        
        # 通用策略
        plan['strategies'].append({
            'type': '元认知策略',
            'techniques': ['计划', '监控', '评估']
        })
        
        plan['strategies'].append({
            'type': '动机策略',
            'techniques': ['小步成功', '及时反馈', '成长型语言']
        })
        
        return plan
    
    def get_theory_summary(self) -> dict:
        """获取理论总结"""
        return {
            'learning_theories': {
                'thorndike_laws': self.learning_theories.THORNDIKE_LAWS,
                'sternberg_intelligence': self.learning_theories.STERNBERG_INTELLIGENCE,
                'zpd': self.learning_theories.ZPD,
                'discovery_learning': self.learning_theories.DISCOVERY_LEARNING,
                'meaningful_learning': self.learning_theories.MEANINGFUL_LEARNING
            },
            'motivation': {
                'maslow_hierarchy': self.motivation.MASLOW_HIERARCHY,
                'mindset': self.motivation.MINDSET,
                'self_determination': self.motivation.SELF_DETERMINATION
            },
            'cognitive_strategies': {
                'memory': self.cognitive.MEMORY_STRATEGIES,
                'metacognitive': self.cognitive.METACOGNITIVE_STRATEGIES,
                'problem_solving': self.cognitive.PROBLEM_SOLVING
            },
            'individual_differences': {
                'learning_styles': self.differences.LEARNING_STYLES,
                'multiple_intelligences': self.differences.MULTIPLE_INTELLIGENCES
            }
        }
    
    def print_summary(self):
        """打印理论总结"""
        print("📚 TX1.0 教育心理学技能 v1.0")
        print("=" * 60)
        print("\n📖 学习理论:")
        print("  • 桑代克三大定律：准备律、练习律、效果律")
        print("  • 斯滕伯格智力三元论：分析性、创造性、实践性")
        print("  • 维果茨基 ZPD：最近发展区 + 支架教学")
        print("  • 布鲁纳发现学习：主动探索、螺旋课程")
        print("  • 奥苏贝尔有意义学习：先行组织者")
        print("\n💡 动机策略:")
        print("  • 马斯洛需求层次：5 层需求")
        print("  • 德韦克成长型思维：固定型 vs 成长型")
        print("  • 自我决定理论：自主感、胜任感、归属感")
        print("\n🧠 认知策略:")
        print("  • 记忆策略：复述、精细加工、组织")
        print("  • 元认知策略：计划、监控、评估")
        print("  • 问题解决：4 步骤 + 启发式")
        print("\n👤 个体差异:")
        print("  • 学习风格：视觉型、听觉型、动觉型")
        print("  • 多元智力：8 种智力类型")
        print("\n" + "=" * 60)


# ==================== 命令行接口 ====================

def main():
    """命令行入口"""
    import sys
    
    core = TX10EducationalPsychology()
    
    if len(sys.argv) < 2:
        print("TX1.0 教育心理学技能 v1.0")
        print("=" * 60)
        print("用法:")
        print("  python3 TX1.0 教育心理学.py summary")
        print("  python3 TX1.0 教育心理学.py analyze <student_id> <behavior>")
        print("  python3 TX1.0 教育心理学.py strategy <situation>")
        print("  python3 TX1.0 教育心理学.py plan <student_profile_json>")
        return
    
    command = sys.argv[1]
    
    if command == 'summary':
        core.print_summary()
    
    elif command == 'analyze':
        if len(sys.argv) < 4:
            print("用法：python3 TX1.0 教育心理学.py analyze <student_id> <behavior>")
            return
        student_id = sys.argv[2]
        behavior = " ".join(sys.argv[3:])
        result = core.analyze_student(student_id, behavior)
        print(f"🔍 学生行为分析")
        print("=" * 60)
        print(f"学生：{result['student_id']}")
        print(f"行为：{result['behavior']}")
        print(f"\n理论分析:")
        for t in result['theories']:
            print(f"  • {t['theory']}: {t['analysis']}")
        print(f"\n建议:")
        for s in result['suggestions']:
            print(f"  ✓ {s}")
    
    elif command == 'strategy':
        if len(sys.argv) < 3:
            print("用法：python3 TX1.0 教育心理学.py strategy <situation>")
            return
        situation = " ".join(sys.argv[2:])
        result = core.get_teaching_strategy(situation)
        print(f"💡 教学策略推荐")
        print("=" * 60)
        print(f"情境：{result['situation']}")
        print(f"\n推荐策略:")
        for s in result['recommended']:
            print(f"  • {s['theory']}")
            print(f"    → {s['strategy']}")
    
    elif command == 'plan':
        if len(sys.argv) < 3:
            print("用法：python3 TX1.0 教育心理学.py plan '<student_profile_json>'")
            return
        import json
        try:
            profile = json.loads(sys.argv[2])
            result = core.create_learning_plan(profile)
            print(f"📋 个性化学习计划")
            print("=" * 60)
            print(f"学生：{result['student_id']}")
            print(f"学习风格：{result['learning_style']}")
            print(f"智力类型：{result['intelligence_type']}")
            print(f"\n策略:")
            for s in result['strategies']:
                print(f"  • {s['type']}")
                if 'techniques' in s:
                    for t in s['techniques']:
                        print(f"    - {t}")
                if 'activities' in s:
                    for a in s['activities']:
                        print(f"    - {a}")
        except json.JSONDecodeError:
            print("❌ JSON 格式错误")
    
    else:
        print(f"❌ 未知命令：{command}")


if __name__ == "__main__":
    main()
