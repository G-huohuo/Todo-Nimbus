# Todo Nimbus

一个使用 FastAPI + HTMX + SQLite 的待办清单应用。无需前端构建工具，部署简单，交互顺滑。

## 功能
- 新增/完成/删除待办
- 过滤视图：全部/未完成/已完成
- HTMX 局部刷新

## 快速开始
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
