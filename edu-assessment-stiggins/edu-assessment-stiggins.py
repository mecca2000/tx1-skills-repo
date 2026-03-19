#!/usr/bin/env python3
"""
斯蒂金斯课堂评估技能
来源：《促进学习的课堂评估》
核心理念：评估为了学习
"""

def summary():
    print("📚 斯蒂金斯课堂评估理论")
    print("=" * 50)
    print("核心理念:")
    print("  • 评估为了学习 (Assessment FOR Learning)")
    print("  • 而非评估学习结果 (Assessment OF Learning)")
    print("\n7 项原则:")
    print("  1. 明确学习目标")
    print("  2. 设计有效评估")
    print("  3. 提供及时反馈")
    print("  4. 学生自我评估")
    print("  5. 学生同伴评估")
    print("  6. 记录学习进步")
    print("  7. 调整教学策略")

def formative_assessment(topic):
    print(f"📊 设计'{topic}'的形成性评估")
    print("=" * 50)
    print("评估方式:")
    print("  • 课堂提问")
    print("  • 小测验")
    print("  • 学习日志")
    print("  • 概念图")
    print("  • 同伴互评")
    print("\n反馈要点:")
    print("  • 及时（当天反馈）")
    print("  • 具体（指出具体问题）")
    print("  • 建设性（提供改进建议）")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        summary()
    elif sys.argv[1] == "formative" and len(sys.argv) > 2:
        formative_assessment(" ".join(sys.argv[2:]))
    else:
        summary()
