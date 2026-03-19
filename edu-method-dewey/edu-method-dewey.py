#!/usr/bin/env python3
"""
杜威教学方法技能
来源：《民主主义与教育》
核心理念：做中学、教育即生活
"""

def summary():
    print("📚 杜威教学方法")
    print("=" * 50)
    print("核心理念:")
    print("  • 教育即生活")
    print("  • 学校即社会")
    print("  • 做中学")
    print("  • 儿童中心")
    print("\n教学原则:")
    print("  • 从经验中学习")
    print("  • 问题解决导向")
    print("  • 民主合作")

def design_activity(topic):
    print(f"🔨 设计'{topic}'的做中学活动")
    print("=" * 50)
    print(f"1. 创设真实情境：{topic}在生活中的应用")
    print("2. 提出问题：让学生思考")
    print("3. 动手操作：实验、制作、调查")
    print("4. 反思总结：学到了什么")
    print("5. 应用迁移：解决新问题")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        summary()
    elif sys.argv[1] == "activity" and len(sys.argv) > 2:
        design_activity(" ".join(sys.argv[2:]))
    else:
        summary()
