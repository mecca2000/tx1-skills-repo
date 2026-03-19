#!/usr/bin/env python3
"""
奥苏贝尔有意义学习技能
来源：《教育心理学：认知观》
"""

def summary():
    print("📚 奥苏贝尔有意义学习理论")
    print("=" * 50)
    print("有意义学习三条件:")
    print("  1. 学习材料有逻辑意义")
    print("  2. 学习者有意义学习的心向")
    print("  3. 学习者认知结构中有适当观念")
    print("\n先行组织者:")
    print("  • 上位组织者（概括性更高）")
    print("  • 下位组织者（具体例子）")
    print("  • 并列组织者（类比）")

def organizer(topic):
    print(f"📋 为'{topic}'设计先行组织者")
    print("=" * 50)
    print(f"1. 上位组织者:")
    print(f"   先介绍'函数'的大概念")
    print(f"2. 下位组织者:")
    print(f"   举一次函数、反比例函数的例子")
    print(f"3. 并列组织者:")
    print(f"   类比方程与函数的关系")

def meaningful(subject):
    print(f"🎯 促进'{subject}'的有意义学习")
    print("=" * 50)
    print("策略:")
    print("  1. 激活旧知：'还记得我们学过...'")
    print("  2. 建立联系：'这个和...很像'")
    print("  3. 概念图：画出知识结构")
    print("  4. 类比教学：用熟悉的事物类比")
    print("  5. 避免机械记忆：强调理解")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        summary()
    elif sys.argv[1] == "organizer" and len(sys.argv) > 2:
        organizer(sys.argv[2])
    elif sys.argv[1] == "meaningful" and len(sys.argv) > 2:
        meaningful(sys.argv[2])
    else:
        summary()
