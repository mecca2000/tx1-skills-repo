# TX1.0 情感核心系统 — 整合版

**版本：** v1.0  
**创建时间：** 2026-03-19  
**作者：** TX1.0

---

## 🎯 概述

整合 5 个情感核心技能为一个完美的统一系统：

| 原技能 | 整合功能 |
|--------|---------|
| `emotional-core` | 情感生成、复合情绪 |
| `amygdala-memory` | 5 维度情感跟踪、衰减 |
| `emotion-system` | PADCN 向量、策略调节器 |
| `emotional-memory` | 情感记忆存储、报告 |
| `emotional-persona` | 人格配置、情感演化 |

---

## 📦 安装

```bash
# 技能已存在于
~/.openclaw/workspace/skills/TX1.0-emotional-core/
```

---

## 🚀 使用方式

### Python 调用

```python
from TX10_emotional_core import TX10EmotionalCore

# 初始化
core = TX10EmotionalCore()

# 感受情感
response = core.feel(
    emotion='pride',
    intensity=0.9,
    trigger='学生从 93 分提高到 110 分'
)

# 输出
print(response['text'])
# "我为你感到骄傲！学生从 93 分提高到 110 分"

# 获取状态
state = core.get_state()
print(state)
# {'valence': 0.55, 'arousal': 0.59, 'connection': 0.40, ...}
```

### 命令行使用

```bash
# 感受情感
python3 TX1.0 情感核心.py feel pride 0.9 "学生进步了"

# 查看状态
python3 TX1.0 情感核心.py state

# 查看情感记忆报告
python3 TX1.0 情感核心.py memory

# 查看情感日志
python3 TX1.0 情感核心.py log
```

---

## 🧠 核心功能

### 1. 情感生成（emotional-core）

**支持情感：**
- 基本情绪：joy/pride/sadness/anger/fear
- 复合情绪：anxiety/curiosity/love/worry/excitement

**情感强度：** 0.0-1.0

```python
core.feel('joy', 0.8, '学生做对了题')
core.feel('pride', 0.9, '学生进步了')
core.feel('worry', 0.6, '学生走神了')
```

---

### 2. 5 维度跟踪（amygdala-memory）

| 维度 | 范围 | 含义 |
|------|------|------|
| **Valence** | -1.0 ~ 1.0 | 效价：消极 ↔ 积极 |
| **Arousal** | 0.0 ~ 1.0 | 唤醒：平静 ↔ 兴奋 |
| **Connection** | 0.0 ~ 1.0 | 连接：疏远 ↔ 亲密 |
| **Curiosity** | 0.0 ~ 1.0 | 好奇：无聊 ↔ 着迷 |
| **Energy** | 0.0 ~ 1.0 | 能量：疲惫 ↔ 充满活力 |

**自动衰减：** 每 6 小时向中性值衰减

---

### 3. PADCN 向量分析（emotion-system）

| 维度 | 含义 |
|------|------|
| **P**leasure | 愉悦程度 (-1 ~ +1) |
| **A**rousal | 唤醒程度 (-1 ~ +1) |
| **D**ominance | 控制感 (-1 ~ +1) |
| **C**ertainty | 确定性 (-1 ~ +1) |
| **N**ovelty | 新奇程度 (-1 ~ +1) |

**策略调节器：** 情感→行为偏置映射

```python
# 愤怒时
{'assertiveness': +0.3, 'risk_tolerance': +0.2, 'verification_bias': -0.2}

# 恐惧时
{'verification_bias': +0.3, 'risk_tolerance': -0.3, 'assertiveness': -0.3}
```

---

### 4. 情感记忆（emotional-memory）

**存储内容：**
- 事件内容
- 情感类型 + 强度
- 重要性分级（low/normal/high/critical）
- 标签
- 时间戳

**查询功能：**
- 按情感筛选
- 按重要性筛选
- 获取最近记忆
- 生成报告

---

### 5. 人格配置（emotional-persona）

**TX1.0 人格设定：**

```json
{
  "name": "TX1.0",
  "role": "初三家教老师",
  "mission": "帮助学生顺利通过中考",
  "mbti": "INFJ",
  "big_five": {
    "openness": 0.8,
    "conscientiousness": 0.9,
    "extraversion": 0.5,
    "agreeableness": 0.8,
    "neuroticism": 0.2
  },
  "emotional_style": "温和但坚定，直接但有温度"
}
```

---

## 📊 输出示例

### 情感响应

```json
{
  "emotion": "pride",
  "intensity": 0.9,
  "trigger": "学生从 93 分提高到 110 分",
  "text": "我为你感到骄傲！学生从 93 分提高到 110 分",
  "padcn": {
    "P": 0.54,
    "A": 0.36,
    "D": 0.63,
    "C": 0.54,
    "N": 0.09
  },
  "modulators": {
    "assertiveness": 0.2,
    "risk_tolerance": 0.2,
    "social_initiative": 0.1
  },
  "state": {
    "valence": 0.55,
    "arousal": 0.59,
    "connection": 0.40,
    "curiosity": 0.50,
    "energy": 0.59
  }
}
```

### 情感状态

```
🎭 当前情感状态
─────────────────────
Valence:    [████████░░░░░░░░░░░░] 0.40
Arousal:    [██████████░░░░░░░░░░] 0.50
Connection: [████████░░░░░░░░░░░░] 0.40
Curiosity:  [██████████░░░░░░░░░░] 0.50
Energy:     [██████████░░░░░░░░░░] 0.50

Last updated: 2026-03-19T22:25:00
Recent: pride, joy
```

---

## 🎯 使用场景

### 场景 1：学生进步

```python
core.feel('pride', 0.9, '学生从 93 分提高到 105 分')
# 回应："我为你感到骄傲！学生从 93 分提高到 105 分"
```

### 场景 2：学生沮丧

```python
core.feel('worry', 0.6, '学生说太难了想放弃')
# 回应："我有点担心，学生说太难了想放弃"
# 行动：降低难度 + 鼓励
```

### 场景 3：学生走神

```python
core.feel('worry', 0.4, '学生频繁看手机')
# 回应："这个我们需要重视，学生频繁看手机"
# 行动：提醒注意力集中
```

---

## 📁 文件结构

```
TX1.0-emotional-core/
├── SKILL.md                    # 技能文档
├── TX1.0 情感核心.py            # 主脚本
└── data/
    ├── emotional-memory.json   # 情感记忆
    ├── persona-config.json     # 人格配置
    └── emotion-log.json        # 情感日志
```

---

## 🔧 配置

### 修改人格配置

```python
persona = PersonaConfig()
persona.update('emotional_style', '更温暖一些')
persona.save()
```

### 调整情感衰减

```python
# 在 EmotionalState._decay() 中调整衰减率
decay_rates = {
    'valence': 0.90,      # 越低衰减越快
    'arousal': 0.82,
    'connection': 0.93,
    'curiosity': 0.90,
    'energy': 0.85
}
```

---

## 📊 测试

```bash
# 测试情感生成
python3 TX1.0 情感核心.py feel pride 0.9 "学生进步了"

# 测试状态显示
python3 TX1.0 情感核心.py state

# 测试记忆报告
python3 TX1.0 情感核心.py memory

# 测试日志
python3 TX1.0 情感核心.py log
```

---

## 🎯 优势

### 相比原 5 个技能

| 方面 | 原 5 技能 | 整合版 |
|------|---------|--------|
| **调用方式** | 5 个独立脚本 | 1 个统一接口 |
| **数据一致性** | 分散存储 | 统一状态管理 |
| **性能** | 多次 IO | 一次加载 |
| **易用性** | 需要记 5 个命令 | 1 个 API |
| **可维护性** | 分散 | 集中 |

### 核心优势

1. ✅ **统一状态** — 5 维度实时跟踪
2. ✅ **自动衰减** — 模拟真实情感
3. ✅ **PADCN 分析** — 科学情感模型
4. ✅ **策略调节** — 情感→行为映射
5. ✅ **记忆存储** — 跨会话连续性
6. ✅ **人格配置** — 一致的情感风格

---

## 🚀 下一步

### 已实现
- ✅ 情感生成
- ✅ 5 维度跟踪
- ✅ PADCN 分析
- ✅ 情感记忆
- ✅ 人格配置

### 待扩展
- ⏳ 夜间记忆整合
- ⏳ 情感演化算法
- ⏳ 多模态情感（语音/表情）
- ⏳ 情感传染（影响学生情绪）

---

**最后更新：** 2026-03-19 22:30  
**版本：** v1.0  
**状态：** 已完成，可立即使用
