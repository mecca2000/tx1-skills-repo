#!/usr/bin/env python3
"""
布鲁纳发现学习技能
来源：《教育过程》
"""

def summary():
    print("📚 布鲁纳发现学习理论")
    print("=" * 50)
    print("核心观点:")
    print("  • 学生是主动的问题解决者")
    print("  • 通过探索发现知识结构")
    print("  • 螺旋式课程（由简到繁重复学习）")
    print("\n教学应用:")
    print("  • 设计探究活动")
    print("  • 提供发现机会")
    print("  • 强调学科基本结构")

def discover(topic):
    print(f"🔍 设计'{topic}'的发现学习活动")
    print("=" * 50)
    print(f"1. 提出问题：关于{topic}，你发现了什么？")
    print("2. 提供材料：让学生操作、观察")
    print("3. 引导发现：不直接告诉答案")
    print("4. 总结结构：帮助学生发现规律")

def spiral(subject):
    print(f"📐 设计'{subject}'的螺旋课程")
    print("=" * 50)
    print("年级 1-2: 基础概念（直观）")
    print("年级 3-4: 深入理解（具体操作）")
    print("年级 5-6: 抽象概括（形式运算）")
    print("年级 7+: 高级应用（综合创新）")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        summary()
    elif sys.argv[1] == "discover" and len(sys.argv) > 2:
        discover(sys.argv[2])
    elif sys.argv[1] == "spiral" and len(sys.argv) > 2:
        spiral(sys.argv[2])
    else:
        summary()
