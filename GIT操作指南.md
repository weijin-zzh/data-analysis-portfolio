# GitHub 操作指南

> 北华大学大数据专业数据分析项目集 - Git使用教程

---

## 目录

1. [推送流程 (Push)](#一推送流程-push)
2. [拉取流程 (Pull)](#二拉取流程-pull)
3. [完整工作流](#三完整工作流)
4. [常见问题解决](#四常见问题解决)
5. [配置建议](#五配置建议)

---

## 一、推送流程 (Push)

将本地代码上传到GitHub仓库

### 完整步骤

```bash
# 1. 进入项目目录
cd C:\Users\zzh14\Desktop\数据分析项目集

# 2. 初始化Git仓库（首次使用）
git init

# 3. 配置用户信息（仓库级，避免污染全局配置）
git config user.name "你的GitHub用户名"
git config user.email "你的GitHub邮箱"

# 4. 添加文件到暂存区
git add .                # 添加所有文件
git add analysis.py      # 添加单个文件

# 5. 提交到本地仓库
git commit -m "提交说明：描述本次修改内容"

# 6. 添加远程仓库（首次使用）
git remote add origin https://github.com/用户名/仓库名.git

# 7. 推送到远程仓库
git push -u origin master    # 首次推送，-u建立追踪关系
git push                     # 后续推送可省略参数
```

### 常用命令

| 命令 | 说明 |
|------|------|
| `git status` | 查看当前状态 |
| `git diff` | 查看修改内容 |
| `git log` | 查看提交历史 |
| `git add .` | 添加所有修改 |
| `git commit -m "msg"` | 提交并添加说明 |
| `git push origin master` | 推送到远程主分支 |

---

## 二、拉取流程 (Pull)

从GitHub仓库下载最新代码到本地

### 完整步骤

```bash
# 1. 进入项目目录
cd C:\Users\zzh14\Desktop\数据分析项目集

# 2. 拉取最新代码
git pull origin master

# 3. 查看更新内容
git log --oneline -5    # 查看最近5次提交
```

### 拉取冲突处理

如果本地修改与远程冲突：
```bash
# 1. 先保存本地修改
git stash

# 2. 拉取远程代码
git pull origin master

# 3. 恢复本地修改并解决冲突
git stash pop

# 4. 手动编辑冲突文件，然后重新提交
git add .
git commit -m "解决冲突"
git push
```

---

## 三、完整工作流

```bash
# === 日常开发流程 ===

# 1. 开始工作前，先拉取最新代码
git pull origin master

# 2. 进行代码修改
# ... 编辑文件 ...

# 3. 查看修改状态
git status

# 4. 提交修改
git add .
git commit -m "修复了XXX问题，添加了XXX功能"

# 5. 推送到远程
git push

# === 查看远程仓库信息 ===
git remote -v    # 查看远程仓库URL
git branch -a    # 查看所有分支
```

---

## 四、常见问题解决

### 问题1：推送失败 - 认证问题
```bash
# 错误：Username for 'https://github.com': 
# 解决方案：使用GitHub个人访问令牌(Token)
# 在GitHub设置 → Developer settings → Personal access tokens 生成
```

### 问题2：推送失败 - 权限不足
```bash
# 错误：remote: Permission to XXX denied to YYY.
# 解决方案：检查远程URL是否正确
git remote set-url origin https://正确的仓库URL.git
```

### 问题3：拉取冲突
```bash
# 错误：Automatic merge failed; fix conflicts and then commit.
# 解决方案：手动编辑冲突文件，搜索 <<<<<<< HEAD 标记
git add .
git commit -m "解决合并冲突"
git push
```

### 问题4：PowerShell命令分隔
```bash
# ❌ 错误（PowerShell不支持&&）
cd project && git status

# ✅ 正确（使用;分隔）
cd project; git status
```

---

## 五、配置建议

### 设置.gitignore（避免提交不必要的文件）
```bash
# 在项目根目录创建 .gitignore 文件
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.log" >> .gitignore
echo ".idea/" >> .gitignore
```

### 查看配置信息
```bash
git config --list          # 查看所有配置
git config user.name       # 查看用户名
git config user.email      # 查看邮箱
```

---

## 总结

| 操作 | 命令 |
|------|------|
| 初始化仓库 | `git init` |
| 添加暂存 | `git add .` |
| 提交 | `git commit -m "msg"` |
| 推送 | `git push origin master` |
| 拉取 | `git pull origin master` |
| 查看状态 | `git status` |

**核心流程**：`修改 → 添加 → 提交 → 推送`，工作前先`拉取`最新代码！

---

**文档版本**：v1.0  
**创建日期**：2026年6月  
**适用项目**：数据分析项目集