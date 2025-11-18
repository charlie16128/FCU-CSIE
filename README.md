# FCU-CSIE
```
---常用指令---
初始化Git
git init
git remote add origin (github repo網址)
git add .
git commit -m ""
git branch -M main
git push -u origin main (有檔案要--force)
-------------
git add .
git commmit -m ""
git push


基本設定與環境
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global core.editor "code --wait"       # 編輯 commit message 時使用的編輯器
git config --global core.autocrlf true              # Windows: CRLF/LF 自動轉換
git config --global credential.helper manager       # Windows credential helper


建立與複製 repo
git init                    # 在當前資料夾初始化一個本地 repo（產生 .git）
git clone <url>             # 從遠端複製整個 repo（會自動建立 origin）
git clone -b <branch> <url> # clone 指定 branch
git clone --depth 1 <url>   # shallow clone（只取最近一個 commit）

基本工作流程（修改 → 暫存 → commit）
git status                  # 檢視狀態（未追蹤、已修改、已暫存）
git add <file>              # 加入暫存區
git add .                   # 將變更加入暫存（注意 .gitignore）
git reset <file>            # 從暫存區移除（但不會還原工作目錄）
git commit -m "message"     # 提交暫存區快照
git commit --amend          # 修改最後一次 commit（改 message 或加入檔案）
git log                     # 顯示 commit 歷史
git log --oneline --graph --decorate --all

檢視差異 / 歷史 / 檔案內容
git diff                   # 顯示工作目錄與暫存區差異
git diff --staged          # 顯示暫存區與 HEAD 差異
git show <commit>          # 顯示指定 commit 的變更與訊息
git blame <file>           # 逐行顯示最後修改此行的 commit 與作者
git log -- <file>          # 顯示某檔案的 commit 歷史

branch（分支）
git branch                 # 列出本地分支
git branch -r              # 列出遠端分支
git branch -a              # 全部
git branch <name>          # 建立分支（但不切換）
git checkout <name>        # 切換分支（舊方式）
git switch <name>          # 建立或切換分支（推薦新指令）
git switch -c <name>       # 建立並切換分支（等同於 checkout -b）
git branch -M main         # 強制重命名分支為 main（-M 為強制）


建議使用 git switch 代替 checkout（語義更清楚）。

合併（merge）與重整（rebase）
git merge <branch>         # 合併指定分支到目前分支（產生 merge commit，若 fast-forward 則不）
git merge --no-ff <branch> # 強制產生 merge commit
git rebase <branch>        # 把目前分支的 commit 拿掉（暫存）→ 把 base 移到 <branch> → 重新套用 commit（歷史會被改寫）
git rebase -i <base>       # 互動式 rebase（squash, edit, reword, drop）


merge 保留分支歷史、rebase 使歷史看起來線性。不要在公共分支上 rebase 已推送的 commit（會造成他人困擾）。

刪除 / 移動檔案
git rm <file>              # 刪除並暫存刪除
git rm --cached <file>     # 從索引移除，但保留本地檔案（常用於把檔案從追蹤中移除）
git mv <old> <new>         # move + 資訊記錄（等同於 filesystem mv + git add/rm）

遠端 (remote) 操作
git remote -v                 # 列出遠端
git remote add origin <url>   # 新增遠端
git remote remove origin      # 刪除遠端
git fetch origin              # 從遠端抓元資料與物件（但不合併）
git fetch --all               # 抓所有遠端
git pull origin main          # fetch + merge（或 fetch + rebase 取決於設定）
git pull --rebase origin main # fetch + rebase
git push origin main          # 推送本地 main 到遠端 main
git push -u origin main       # 設定 upstream（-u = --set-upstream），以後可直接 git push
git push --force-with-lease   # 較安全的強制推送（保護別人的 commit）
git push --tags               # 推所有 tag
```
