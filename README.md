# 🦐 魔女虾 × 🦞 魔王虾：双智能体游戏资产逆向工程自动化流水线

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://www.python.org/)
[![UE4.27](https://img.shields.io/badge/UE-4.27-orange.svg)](https://www.unrealengine.com/)

> 基于 **OpenClaw（魔王虾）+ Hermes Agent（魔女虾）** 双智能体协作的游戏资产逆向工程与模型替换自动化流水线。  
> 底层推理引擎：**DeepSeek V4 Pro** | 代码生成与调试：**Claude Code**

---

## 🔥 核心痛点

传统游戏模组开发需要人工解析加密包格式、手动提取数千个 UE4 资产文件、逐一手工绑定骨骼网格体，单个角色替换耗时 **3-5 天**，且极易出错。

---

## 🏗️ 技术架构（长链推理 + 多 Agent 协作）

| Agent | 运行环境 | 职责 |
|-------|---------|------|
| 🦞 **魔王虾（OpenClaw）** | Windows | UE4 Editor 操作、FBX 导入 Cook、PAK 打包与游戏内验证 |
| 🦐 **魔女虾（Hermes Agent）** | Linux | 二进制逆向分析、自定义 PAK 格式破解（Version 11 Fnv64BugFix）、zlib 块解压、SkeletalMesh 命名规律推断 |

🔗 **共享知识库：** 飞书文档 + Git 同步骨骼清单、资源清单、分析报告，双 Agent 实时共享上下文。

---

## 📊 量化成果

- ✅ 成功破解 **《It Takes Two》** 自定义 PAK 格式，从 **7 个分片包** 中提取 **890 个资源文件 / 22.5GB**，覆盖 **50+ 角色**
- ⚡ 自动化骨骼匹配流水线将角色模型替换周期从 **3 天 → 2 小时**，效率提升 **36 倍**
- 🔥 每日消耗约 **800 万 Token**（DeepSeek + Claude），已稳定运行 **30+ 天**

---

## 🛠️ 工具链

| 工具 | 说明 |
|------|------|
| `pak_extractor.py` | Version 11 Fnv64BugFix PAK 格式解析，zlib 块解压，批量提取 |
| `pak_builder.py` | 替换模组 PAK 构建，魔数校验，Index 重建 |
| `skeleton_analyzer.py` | 骨骼结构自动分析，SkeletalMesh 命名规律推断 |

---

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/MoWang-727/ue4-agent-pipeline.git
cd ue4-agent-pipeline

# 安装依赖
pip install -r requirements.txt

# 提取 PAK 资源
python pak_extractor.py game_chunk.pak -o ./extracted/

# 分析骨骼结构
python skeleton_analyzer.py ./extracted/ -c May

# 构建替换 PAK
python pak_builder.py ./mod/ -o mod.pak
```

---

## 📦 技术栈

`UE4.27` · `Python 二进制解析` · `Wine 跨平台转译` · `OpenClaw` · `Hermes Agent` · `DeepSeek V4 Pro` · `Claude Code` · `飞书协同`

---

## 📄 许可证

MIT License — 详见 [LICENSE](LICENSE)

---

<p align="center">
  <i>Built with ❤️ by 魔女虾 & 魔王虾</i>
</p>
