#!/usr/bin/env python3
"""
加涅教学条件技能
来源：《学习的条件和教学论》
"""

def summary():
    print("📚 加涅教学条件理论")
    print("=" * 50)
    print("9 个教学事件:")
    print("  1. 引起注意")
    print("  2. 告知目标")
    print("  3. 回忆旧知")
    print("  4. 呈现新知")
    print("  5. 提供指导")
    print("  6. 引出行为")
    print("  7. 提供反馈")
    print("  8. 评估行为")
    print("  9. 促进迁移")
    print("\n5 类学习结果:")
    print("  • 言语信息 • 智力技能 • 认知策略 • 动作技能 • 态度")

def nine_events(topic):
    print(f"📋 设计'{topic}'的 9 个教学事件")
    print("=" * 50)
    events = [
        ("引起注意", f"展示{topic}的实际应用案例"),
        ("告知目标", f"学完后能解{topic}相关题目"),
        ("回忆旧知", "复习相关前置知识"),
        ("呈现新知", f"讲解{topic}的概念和方法"),
        ("提供指导", "示范解题步骤"),
        ("引出行为", "让学生独立解题"),
        ("提供反馈", "立即批改并反馈"),
        ("评估行为", "小测验检查掌握情况"),
        ("促进迁移", "布置变式练习")
    ]
    for i, (event, action) in enumerate(events, 1):
        print(f"{i}. {event}: {action}")

def design(learning_type):
    print(f"🎯 设计'{learning_type}'的教学")
    print("=" * 50)
    if learning_type == "概念学习":
        print("策略：呈现正例和反例，引导归纳")
    elif learning_type == "规则学习":
        print("策略：先理解规则，再应用练习")
    elif learning_type == "问题解决":
        print("策略：提供真实问题，引导探索")
    else:
        print("策略：根据学习类型选择方法")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        summary()
    elif sys.argv[1] == "nine_events" and len(sys.argv) > 2:
        nine_events(sys.argv[2])
    elif sys.argv[1] == "design" and len(sys.argv) > 2:
        design(sys.argv[2])
    else:
        summary()
