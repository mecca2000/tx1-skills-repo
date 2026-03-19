#!/usr/bin/env python3
"""
苏霍姆林斯基教学方法技能
来源：《给教师的建议》
核心理念：爱心教育、全面发展
"""

def summary():
    print("📚 苏霍姆林斯基教学方法")
    print("=" * 50)
    print("核心理念:")
    print("  • 爱心教育")
    print("  • 全面发展")
    print("  • 尊重学生")
    print("  • 相信每个孩子")
    print("\n教学建议:")
    print("  • 多表扬少批评")
    print("  • 发现每个孩子的闪光点")
    print("  • 让每个孩子体验成功")

def encourage(student_behavior):
    print(f"💝 鼓励策略：'{student_behavior}'")
    print("=" * 50)
    print("鼓励话术:")
    print("  • '我看到你的努力了'")
    print("  • '你比昨天进步了'")
    print("  • '这个想法很有创意'")
    print("  • '我相信你能做到'")
    print("\n注意事项:")
    print("  • 表扬具体行为而非天赋")
    print("  • 真诚而非敷衍")
    print("  • 关注过程而非结果")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        summary()
    elif sys.argv[1] == "encourage" and len(sys.argv) > 2:
        encourage(" ".join(sys.argv[2:]))
    else:
        summary()
