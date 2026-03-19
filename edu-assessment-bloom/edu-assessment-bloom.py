#!/usr/bin/env python3
"""
布鲁姆教育目标分类技能
来源：《教育目标分类学》
核心理论：认知领域 6 层次
"""

def summary():
    print("📚 布鲁姆教育目标分类")
    print("=" * 50)
    print("认知领域 6 层次（由低到高）:")
    print("  1. 记忆 - 回忆知识")
    print("  2. 理解 - 理解意义")
    print("  3. 应用 - 应用知识")
    print("  4. 分析 - 分析结构")
    print("  5. 评价 - 做出判断")
    print("  6. 创造 - 创造新事物")
    print("\n情感领域 5 层次:")
    print("  接受→反应→价值评价→组织→价值体系个性化")
    print("\n动作技能领域:")
    print("  知觉→准备→有指导的反应→机械动作→复杂外显反应")

def design_test(topic, level="all"):
    print(f"📝 设计'{topic}'的测试题")
    print("=" * 50)
    questions = {
        "记忆": f"什么是{topic}? 请定义。",
        "理解": f"请解释{topic}的含义。",
        "应用": f"请用{topic}解决以下问题。",
        "分析": f"请分析{topic}的组成部分。",
        "评价": f"请评价{topic}的优缺点。",
        "创造": f"请设计一个关于{topic}的新方案。"
    }
    for level, q in questions.items():
        print(f"{level}: {q}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        summary()
    elif sys.argv[1] == "test" and len(sys.argv) > 2:
        design_test(sys.argv[2])
    else:
        summary()
