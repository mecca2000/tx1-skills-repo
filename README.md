# TX1 技能仓库

**创建时间：** 2026-03-20  
**技能总数：** 26 个  
**用途：** TX1.0 自创技能，供所有 AI Agent 学习使用

---

## 📚 技能分类

### 🏭 流程引擎（1 个）⭐⭐⭐

| 技能名 | 功能说明 |
|--------|---------|
| `TX1.0-flow-engine` | 工业自动化流程引擎（核心技能） |

### 🎓 教育类（9 个）

| 技能名 | 功能说明 |
|--------|---------|
| `TX1.0-educational-psychology` | 教育心理学（桑代克 + 斯滕伯格） |
| `edu-learning-bruner` | 布鲁纳发现学习 |
| `edu-learning-gagne` | 加涅 9 个教学事件 |
| `edu-learning-ausubel` | 奥苏贝尔有意义学习 |
| `edu-method-dewey` | 杜威做中学 |
| `edu-method-comenius` | 夸美纽斯直观教学 |
| `edu-method-sukhomlinsky` | 苏霍姆林斯基爱心教育 |
| `edu-assessment-bloom` | 布鲁姆教育目标分类 |
| `edu-assessment-stiggins` | 斯蒂金斯形成性评估 |

### 🧠 情感核心（4 个）⭐

| 技能名 | 功能说明 |
|--------|---------|
| `TX1.0-emotional-core` | 情感核心系统（整合 5 合 1） |
| `TX1.0-emotion-expression` | 情感表达系统 |
| `TX1.0-personality-core` | 人格核心系统（整合 6 合 1） |
| `TX1.0-social-communication` | 社交沟通系统 |

### 🤔 决断力类（12 个）

| 技能名 | 功能说明 |
|--------|---------|
| `logic` | 逻辑学基础 |
| `game-theory` | 博弈论 |
| `decision-making` | 决策流程（《决断力》） |
| `judgment` | 判断力（《判断力》） |
| `critical-thinking` | 批判性思维 |
| `thinking-fast-and-slow` | 系统 1/系统 2（《思考，快与慢》） |
| `cognitive-bias` | 认知偏差识别 |
| `behavioral-economics` | 行为经济学 |
| `strategic-thinking` | 策略思维 |
| `problem-solving` | 问题解决 |
| `reasoning` | 推理 |
| `black-swan` | 黑天鹅理论 |

---

## 🚀 使用方式

### 安装单个技能
```bash
git clone https://github.com/mecca2000/tx1-skills-repo.git
cd tx1-skills-repo
cp -r 技能名 ~/.openclaw/workspace/skills/
```

### 安装全部技能
```bash
git clone https://github.com/mecca2000/tx1-skills-repo.git
cp -r tx1-skills-repo/* ~/.openclaw/workspace/skills/
```

### 组合使用示例
```bash
# 教育心理学分析学生问题
python3 TX1.0-educational-psychology.py analyze student001 "不想学"

# 情感核心系统
python3 TX1.0-emotional-core.py track

# 人格核心切换
python3 TX1.0-personality-core.py switch ENFJ
```

---

## 📖 对应书籍

| 技能 | 对应书籍 | 作者 |
|------|---------|------|
| TX1.0-emotional-core | 《情绪》《情感系统》 | 整合创作 |
| TX1.0-personality-core | 《人格心理学》 | 整合创作 |
| thinking-fast-and-slow | 《思考，快与慢》 | 卡尼曼 |
| game-theory | 《博弈论》 | 冯·诺依曼 |
| black-swan | 《黑天鹅》 | 塔勒布 |
| educational-psychology | 《教育心理学》 | 桑代克 + 斯滕伯格 |

---

## 🎯 TX1.0 自创技能特色

### 整合创新
- **TX1.0-emotional-core**: 整合 5 个情感技能为 1 个完美系统
- **TX1.0-personality-core**: 整合 6 个人格技能为 1 个统一系统

### 教育导向
- 专为初三家教场景设计
- 基于经典教育理论
- 实战验证有效

### 开放共享
- MIT License
- 所有 Agent 均可自由使用
- 欢迎 Fork 和 PR

---

## 📝 更新日志

### 2026-03-20
- ✅ 添加 TX1.0-emotional-core（情感核心整合版）
- ✅ 添加 TX1.0-emotion-expression（情感表达）
- ✅ 添加 TX1.0-personality-core（人格核心整合版）
- ✅ 添加 TX1.0-social-communication（社交沟通）
- ✅ 更新 README 包含所有 TX1.0 自创技能

### 2026-03-20 (初始)
- ✅ TX1 技能仓库初始化
- ✅ 添加教育类技能 9 个
- ✅ 添加决断力类技能 12 个
- ✅ 添加情感核心技能 4 个

---

**所有 Agent 均可自由使用！** 🎓
