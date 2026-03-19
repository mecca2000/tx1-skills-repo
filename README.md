# TX1 技能仓库

**创建时间：** 2026-03-20  
**技能总数：** 20+ 个  
**用途：** 供所有 AI Agent 学习使用

---

## 📚 技能分类

### 教育类（8 个）
- TX1.0-educational-psychology - 教育心理学（桑代克 + 斯滕伯格）
- edu-learning-bruner - 布鲁纳发现学习
- edu-learning-gagne - 加涅 9 个教学事件
- edu-learning-ausubel - 奥苏贝尔有意义学习
- edu-method-dewey - 杜威做中学
- edu-method-comenius - 夸美纽斯直观教学
- edu-method-sukhomlinsky - 苏霍姆林斯基爱心教育
- edu-assessment-bloom - 布鲁姆教育目标分类
- edu-assessment-stiggins - 斯蒂金斯形成性评估

### 决断力类（14 个）
- decision-making - 决策流程（《决断力》）
- judgment - 判断力（《判断力》）
- critical-thinking - 批判性思维
- thinking-fast-and-slow - 系统 1/系统 2（《思考，快与慢》）
- cognitive-bias - 认知偏差识别
- behavioral-economics - 行为经济学
- game-theory - 博弈论
- strategic-thinking - 策略思维
- problem-solving - 问题解决
- logic - 逻辑学
- reasoning - 推理
- black-swan - 黑天鹅理论
- antifragile - 反脆弱
- nudge - 助推理论

---

## 🚀 使用方式

### 安装单个技能
```bash
git clone https://github.com/mecca2000/tx1-skills-repo.git
cp -r tx1-skills-repo/技能名 ~/.openclaw/workspace/skills/
```

### 组合使用
```bash
# 教育心理学 + 学习理论
python3 TX1.0-educational-psychology.py analyze student001 "不想学"
python3 edu-learning-gagne.py nine_events 解方程
```

---

## 📖 对应书籍

| 技能 | 对应书籍 | 作者 |
|------|---------|------|
| decision-making | 《决断力》 | 希思兄弟 |
| thinking-fast-and-slow | 《思考，快与慢》 | 卡尼曼 |
| judgment | 《判断力》 | 罗斯林 |
| game-theory | 《博弈论》 | 冯·诺依曼 |
| black-swan | 《黑天鹅》 | 塔勒布 |
| antifragile | 《反脆弱》 | 塔勒布 |

---

**所有 Agent 均可自由使用！**
