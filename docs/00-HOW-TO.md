## HOW TO 快速上手

> 还没准备好读完全部章节？先从这里开始，按你的角色快速上手最常用的操作。

---

### 场景 A：旧代码上传

**适用对象**：个人项目、已有源码要接入 Gitea  
**目标**：初始化仓库 → 连接远程 → 提交 → 打标签 → 发布二进制

1. **初始化 & 首次提交**
   ```bash
   git init                # 初始化本地 Git 仓库，创建 .git 目录
   git status              # 查看当前文件状态，红色为未跟踪，绿色为已暂存
   ```
   
   **创建一个 .gitignore 文件**（用你喜欢的编辑器打开）：
   ```bash
   # Windows: notepad .gitignore
   # macOS: code .gitignore 或 vim .gitignore
   # Linux: vim .gitignore 或 nano .gitignore
   ```
   
   **常见 .gitignore 内容**：
   ```
   # 依赖目录
   node_modules/
   vendor/
   
   # 构建产物
   dist/
   build/
   target/
   *.exe
   *.dll
   
   # 日志文件
   *.log
   logs/
   
   # 系统文件
   .DS_Store
   Thumbs.db
   
   # 临时文件
   *.tmp
   *.cache
   .env
   ```
   **特别是老项目一定要先配置 .gitignore！**
   以上是一些常用的.gitignore文件内容，主要包括一些不想要的东西，如果有其他的不是源代码的东西，除非特别重要而且比较小，否则都应该丢掉，如果有驱动之类的可以放到release里头。

   **提交文件**：

   ```bash
   git add .                                  # 现在可以安全地添加所有文件了
   git commit -m "初始化"                     # 提交项目源码
   ```
注意哦，所有的项目开始都是以初始化开始

2. **连接远程（以 Gitea 为例）**
   - 在 Gitea "+" → "新建仓库"，获取 `SSH/HTTPS` 地址
   ```bash
   git remote add origin git@your-gitea:team/repo.git  # 添加远程仓库地址，origin 是别名
   git branch -M main                              # 将当前分支重命名为 main（现代 Git 标准）
   git push -u origin main                         # 推送到远程并设置上游分支，-u 表示以后直接 git push
   ```
3. **给版本打标签 & 推送**
   ```bash
   git tag -a v1.0.0 -m "正式发布"  # 创建带注释的标签，-a 表示 annotated，-m 写标签说明
   git push origin v1.0.0             # 推送标签到远程仓库（标签默认不随 git push 推送）
   ```
4. **发布二进制**
   - 构建产物（如 `dist/xxx.zip`、可执行文件等）
   - 在 Gitea "Releases" → "New Release"
     - 选择 `Tag`（如 `v1.0.0`），填写变更说明
     - 上传二进制附件并发布

**注意事项**
- 在 `.gitignore` 中排除构建产物、临时文件
- 坚持使用语义化版本号：`主版本.次版本.修订`

---

### 场景 B：刚加入项目，要开始开发

**适用对象**：新成员、外包协作者  
**目标**：拉取代码 → 创建分支 → 开发 → 提交 → 提 PR

1. **获取仓库**
   ```bash
   git clone git@your-gitea:team/repo.git  # 克隆远程仓库到本地，会自动创建 repo 目录
   cd repo                                  # 进入项目目录
   git remote -v                            # 查看远程仓库地址，确认 origin 指向正确
   ```
2. **同步主干 & 创建个人分支**
   ```bash
   git checkout develop        # 切换到 develop 分支（团队开发主干）
   git pull origin develop     # 拉取远程 develop 分支的最新代码到本地
   git checkout -b feature/login-otp  # 创建并切换到新分支，用于开发登录 OTP 功能
   ```
3. **开发与提交**
   ```bash
   git status                                      # 查看文件状态，确认修改的文件
   git add src/login.js                            # 只添加修改的登录文件到暂存区
   git commit -m "feat(login): 支持 OTP 登录"       # 提交变更，使用规范格式：feat+模块+描述
   ```
4. **保持分支同步**
   ```bash
   git fetch origin              # 获取远程仓库最新信息，但不合并到本地
   git rebase origin/develop     # 将当前分支的提交重新应用到 develop 最新版本上，保持历史干净
   # 或者用 git merge origin/develop，但会产生合并提交记录
   ```
5. **推送 & 创建 PR**
   ```bash
   git push -u origin feature/login-otp  # 推送分支到远程，-u 设置上游分支方便后续推送
   ```
   - 在 Gitea 打开仓库 → "Pull Requests" → "New Pull Request"
   - 选择 `base: develop`（目标分支）、`compare: feature/login-otp`（源分支）
   - 填写 PR 模板（相关 Issue、测试、截图等），说明修改内容和测试情况

**注意事项**
- 提交信息遵循团队规范（见第四部分）
- 一次 PR 专注一件事，确保有测试或截图
- 处理完 review 意见后再次 `push`，PR 会自动更新

---

### 场景 C：项目管理者/维护者

**适用对象**：Tech Lead、仓库管理员  
**目标**：管理分支 → 审核代码 → 发布版本 → 处理紧急修复

1. **分支治理**
   - `main`：线上稳定版本，只接收 release/hotfix（长期分支）
   - `develop`：集成测试环境，新功能合入此分支（长期分支）
   - `feature/*`：功能开发，完成后合入 `develop`，然后赶紧删掉这个临时分支避免项目混乱
   - `release/*`：发布前的稳定候选，完成后合入 `main & develop`，也要删掉
   - `hotfix/*`：线上紧急修复，完成后合入 `main & develop`，要删掉，临时的
2. **每日例行**
   ```bash
   git fetch --all --prune    # 获取所有远程仓库的最新信息，--prune 删除已不存在的远程分支
   git status                 # 查看当前工作目录状态，是否有未提交的修改
   git branch -av             # 显示所有分支（本地+远程），-a 显示全部，-v 显示最新提交
   ```
   **作用**：每日开工前同步远程信息，了解项目整体进展，避免开发冲突
3. **代码审核**
   - 在 Gitea "Pull Requests" 查看待处理 PR
   - 核对：需求/Issue、CI 结果、代码变更、测试
   - 使用评论、建议、Request changes 或 Approve
4. **合并策略**
   - 常用 `Squash and merge` 或 `Rebase and merge`，保持历史干净
   - 合并 release/hotfix 时同步更新 `main` 和 `develop`
5. **发布版本**
   ```bash
   git checkout release/v1.2.0          # 切换到发布分支
   git tag -a v1.2.0 -m "Release v1.2.0"  # 创建版本标签
   git push origin release/v1.2.0 v1.2.0  # 推送分支和标签到远程
   ```
   - 在 Gitea 创建 Release，附上变更日志与二进制
6. **紧急修复示例**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/payment-failure
   # 修复 + 提交
   git commit -m "fix(payment): 处理支付回调异常"
   git push -u origin hotfix/payment-failure
   # PR -> main + develop
   ```

**注意事项**
- 发布前确保 CI 通过、版本号更新、变更日志齐全
- 定期清理已合并分支：`git push origin --delete feature/xxx`
- 使用 Issue/Project 面板跟踪任务，避免遗漏

---

📎 **下一步**：按你的角色需求阅读，或回到首页目录查看更多细节。

