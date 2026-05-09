# UE4 Agent Pipeline — AI 驱动的多 Agent 游戏逆向工程平台

> 🦞 OpenClaw 调度 + 🐎 Hermes Agent 执行 + 🤖 多 Agent 协作 = 游戏逆向全自动化

[![Stars](https://img.shields.io/github/stars/chenyixun710/ue4-agent-pipeline?style=social)](https://github.com/chenyixun710/ue4-agent-pipeline)
[![OpenClaw](https://img.shields.io/badge/orchestrator-OpenClaw-orange)](https://github.com/openclaw/openclaw)
[![Hermes Agent](https://img.shields.io/badge/executor-Hermes%20Agent-purple)](https://github.com/NousResearch/hermes-agent)
[![MiMo V2.5](https://img.shields.io/badge/model-MiMo%20V2.5-green)](https://platform.xiaomimimo.com)

---

## 🎯 一句话

**传统 2-4 周的游戏逆向工程 → AI Agent 驱动 3-6 小时完成，效率提升 100x+**

---

## 🧠 架构：6 步长链推理 + 多 Agent 并行协作

```
                    ┌──────────────────────┐
                    │   OpenClaw 总调度      │
                    │   (MiMo V2.5-Pro)     │
                    │   任务分解 · 编排 · 监控 │
                    └──────┬───────┬───────┘
                           │       │
          ┌────────────────┘       └────────────────┐
          ▼                                         ▼
┌──────────────────┐                      ┌──────────────────┐
│  并行组 A         │                      │  并行组 B         │
│                  │                      │                  │
│ ① 引擎识别       │                      │ ④ 资源提取        │
│   Godot/UE/Unity │                      │   骨骼·网格·材质   │
│        │         │                      │        │         │
│        ▼         │                      │        ▼         │
│ ② 格式破解       │                      │   动画·纹理       │
│   pak/pck 解密   │                      │                  │
└────────┬─────────┘                      └────────┬─────────┘
         │                                         │
         └──────────────┬──────────────────────────┘
                        ▼
              ┌──────────────────┐
              │ ③ 反编译          │
              │ Hermes Agent 驱动 │
              │ ikdasm · Cecil    │
              │ 3MB+ DLL 分析     │
              └────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │ ⑤ Mod 生成        │
              │ Hermes + Aider   │
              │ C++/C# 自动编码   │
              └────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │ ⑥ 验证闭环        │
              │ 编译 · 注入 · 测试 │
              └──────────────────┘
```

| 步骤 | Agent | 引擎 | 输出 |
|------|-------|------|------|
| ① 识别 | 引擎Agent | OpenClaw + 文件指纹 | 引擎类型 + 版本 |
| ② 破解 | 格式Agent | OpenClaw 长链推理 | 解密文件表 |
| ③ 反编译 | 反编译Agent | **Hermes Agent** + ikdasm | IL代码 + 类/方法清单 |
| ④ 提取 | 资源Agent | umodel + QuickBMS | 模型/纹理/动画 |
| ⑤ 生成 | ModAgent | **Hermes Agent** + Aider | C++/C# Mod源码 |
| ⑥ 验证 | 验证Agent | Hermes Agent 终端 | 测试报告 |

---

## 🛠️ 技术栈

| 层 | 技术 |
|---|------|
| 调度引擎 | OpenClaw (MiMo V2.5-Pro) |
| 代码引擎 | Hermes Agent (DeepSeek V4 Pro) |
| 辅助编程 | Aider 0.12.0 |
| 逆向工具 | umodel, QuickBMS, ikdasm, Mono.Cecil, Cheat Engine |
| Mod 框架 | C++ MSVC + ImGui, C# .NET 8 + Cecil |
| 运行环境 | Linux (容器化) + Windows (游戏端) |

---

## 📊 效果数据

| 指标 | 数据 |
|------|------|
| Token 消耗 | 800万 - 1500万 / 天 |
| 效率提升 | 传统 2-4 周 → **3-6 小时** (100x+) |
| 支持引擎 | UE4, UE5, Godot 3/4, Unity |
| 已逆向游戏 | It Takes Two, Pratfall, + 更多 |
| Mod 代码量 | 3000+ 行自动生成 |
| 提取资源 | 骨骼/网格/材质/动画全套 |

---

## 🚀 快速开始

```bash
# 1. 安装
git clone https://github.com/chenyixun710/ue4-agent-pipeline
cd ue4-agent-pipeline
pip install aider-chat

# 2. 配置
export DEEPSEEK_API_KEY=sk-xxx
export MIMO_API_KEY=sk-xxx

# 3. 运行 — 自动完成游戏逆向全流程
hermes agent task "逆向分析 D:/Steam/steamapps/common/YourGame" \
  --skills ue4-pak-extraction,godot-game-modding \
  --model deepseek-v4-pro
```

---

## 📂 实战案例

### 🎮 Pratfall (Godot 4 .NET) — 完整逆向案例

```
Pratfall/
├── Injector/          # Cecil IL 注入器
├── NativeTrainer/     # C++ ImGui 外部覆盖窗
├── 参考文件/          # 8 份深度逆向报告
│   ├── Pratfall 全部内置功能深度反编译报告.txt  (532行)
│   ├── Pratfall 完整道具系统分析.txt            (241行)
│   ├── Harmony 运行时补丁方案.txt
│   └── ...
└── build.bat          # 一键构建
```

**成果：**
- ✅ 11 大游戏系统完整反编译（移动/战斗/物品/外观/自定义模式…）
- ✅ 40+ 道具 ID 完整提取（食物/武器/投掷物/功能道具）
- ✅ 8 功能 Mod：上帝模式·超级跳跃·零重力·三倍速·穿墙·解锁外观·冻结计时·道具生成
- ✅ 零人工代码 — 全部由 Hermes Agent + Aider 自动生成

### 🎮 It Takes Two (UE4) — pak v11 破解

- ✅ pak v11 自定义加密格式破解
- ✅ 角色模型全套提取（骨骼/网格/材质/动画）

---

## 🔗 相关资源

- [OpenClaw 官方](https://github.com/openclaw/openclaw) — AI 调度引擎 (370k⭐)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) — 代码执行 Agent (139k⭐)
- [MiMo 开放平台](https://platform.xiaomimimo.com) — 模型服务

---

## 📄 License

MIT © 2026 Burning.AI
