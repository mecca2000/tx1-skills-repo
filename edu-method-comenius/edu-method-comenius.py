#!/usr/bin/env python3
"""
夸美纽斯教学方法技能
来源：《大教学论》
核心理念：泛智教育、班级授课制
"""

def summary():
    print("📚 夸美纽斯教学方法")
    print("=" * 50)
    print("核心理念:")
    print("  • 泛智教育（把一切知识教给一切人）")
    print("  • 班级授课制")
    print("  • 直观性原则")
    print("  • 循序渐进")
    print("\n教学原则:")
    print("  • 从具体到抽象")
    print("  • 从简单到复杂")
    print("  • 从已知到未知")

def visual_teaching(topic):
    print(f"👁️ 为'{topic}'设计直观教学")
    print("=" * 50)
    print("直观教具:")
    print("  • 实物展示")
    print("  • 图片图表")
    print("  • 模型演示")
    print("  • 视频动画")
    print("\n步骤:")
    print("  1. 先观察具体事物")
    print("  2. 形成表象")
    print("  3. 抽象概念")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        summary()
    elif sys.argv[1] == "visual" and len(sys.argv) > 2:
        visual_teaching(" ".join(sys.argv[2:]))
    else:
        summary()
