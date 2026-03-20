# 📤 GitHub 上传说明

**仓库名：** tx1-skills-repo  
**技能数：** 20+ 个  
**用途：** 供所有 AI Agent 学习使用

---

## ⚠️ GitHub 认证变更

**重要：** GitHub 已不再支持密码认证，需要使用 **Personal Access Token (PAT)**

---

## 🔑 获取 Personal Access Token

### 步骤 1：登录 GitHub
访问 https://github.com/login  
使用账号：mecca2000@163.com  
密码：fenG1020

### 步骤 2：创建 Token
1. 点击右上角头像 → Settings
2. 左侧菜单 → Developer settings
3. Personal access tokens → Tokens (classic)
4. Generate new token (classic)
5. 填写：
   - **Note:** TX1 Skills Repo
   - **Expiration:** No expiration
   - **Scopes:** 勾选 `repo` (完整仓库权限)
6. 点击 "Generate token"
7. **复制 Token**（只显示一次，格式：`ghp_xxxxxxxxxxxx`）

---

## 📤 上传方法 1：使用 Token 推送

```bash
cd ~/.openclaw/workspace/skills/tx1-skills-repo

# 设置认证
git remote set-url origin https://mecca2000:YOUR_TOKEN@github.com/mecca2000/tx1-skills-repo.git

# 推送
git push -u origin main
```

**替换 `YOUR_TOKEN` 为你刚生成的 Token**

---

## 📤 上传方法 2：使用 GitHub Desktop

1. 下载 GitHub Desktop：https://desktop.github.com
2. 登录 GitHub 账号
3. File → Add Local Repository
4. 选择目录：`~/.openclaw/workspace/skills/tx1-skills-repo`
5. 点击 Publish repository
6. 填写仓库名：tx1-skills-repo
7. 勾选 "Keep this code private"（可选）
8. 点击 Publish

---

## 📤 上传方法 3：手动上传（最简单）

1. 访问 https://github.com/new
2. 仓库名：tx1-skills-repo
3. 描述：TX1 Agent 技能仓库 - 供所有 Agent 学习使用
4. 勾选 "Add a README file"
5. 点击 Create repository
6. 点击 "uploading an existing file"
7. 拖入所有技能文件夹
8. 点击 "Commit changes"

---

## 📦 技能包位置

**本地目录：** `~/.openclaw/workspace/skills/tx1-skills-repo/`

**包含：**
- 8 个教育类技能
- 14 个决断力类技能
- README.md 使用说明

**压缩包：** `/tmp/tx1-skills-repo.tar.gz`

---

## 🔗 其他 Agent 使用方式

**仓库创建后，其他 Agent 可以：**

```bash
# 克隆整个仓库
git clone https://github.com/mecca2000/tx1-skills-repo.git

# 安装单个技能
cp -r tx1-skills-repo/decision-making ~/.openclaw/workspace/skills/

# 测试安装
python3 ~/.openclaw/workspace/skills/decision-making/decision-making.py summary
```

---

## ✅ 完成检查清单

- [ ] 创建 GitHub 仓库
- [ ] 上传所有技能文件
- [ ] 上传 README.md
- [ ] 验证仓库可访问
- [ ] 分享仓库链接给其他 Agent

---

**创建人：** TX1.0  
**创建时间：** 2026-03-20  
**状态：** ⏳ 等待上传
