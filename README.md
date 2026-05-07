# 基于 OpenClaw × Hermes Agent 的多智能体游戏资产逆向与自动化流水线

我构建了一套基于 OpenClaw（魔王虾）+ Hermes Agent（魔女虾）双智能体协作的游戏资产逆向工程与模型替换自动化流水线。系统以 DeepSeek V4 Pro 为底层推理引擎，通过 Claude Code 进行代码生成与调试。

## 核心痛点

传统游戏模组开发需要人工解析加密包格式、手动提取数千个 UE4 资产文件、逐一手工绑定骨骼网格体，单个角色替换耗时 3-5 天，且极易出错。

## 技术架构（长链推理 + 多 Agent 协作）

- 🦞 **魔王虾（OpenClaw）：** 负责 Windows 端 UE4 Editor 操作、FBX 导入 Cook、PAK 打包与游戏内验证
- 🦐 **魔女虾（Hermes Agent）：** 负责 Linux 端二进制逆向分析、自定义 PAK 格式破解（Version 11 Fnv64BugFix）、zlib 块解压、SkeletalMesh 命名规律推断
- 🔗 **共享知识库：** 通过飞书文档 + Git 同步骨骼清单、资源清单、分析报告，双 Agent 实时共享上下文

## 量化成果

- 成功破解《It Takes Two》自定义 PAK 格式，从 7 个分片包中提取 890 个资源文件 / 22.5GB，覆盖 50+ 角色
- 自动化骨骼匹配流水线将角色模型替换周期从 3 天压缩至 2 小时，效率提升 36 倍
- 每日消耗约 800 万 Token（含 DeepSeek + Claude），已稳定运行 30+ 天

## 技术栈

UE4.27 | Python 二进制解析 | Wine 跨平台转译 | OpenClaw | Hermes Agent | DeepSeek V4 Pro | Claude Code | 飞书协同

## 安装

```bash
git clone https://github.com/chenyixun710/ue4-agent-pipeline.git
cd ue4-agent-pipeline
```

## 快速开始

```bash
# 提取 PAK 资源
python pak_extractor.py game_chunk.pak -o ./extracted/

# 分析骨骼结构
python skeleton_analyzer.py ./extracted/ -c May

# 构建替换 PAK
python pak_builder.py ./mod/ -o mod.pak
```

## 工具

| 工具 | 说明 |
|------|------|
| `pak_extractor.py` | Version 11 Fnv64BugFix PAK 格式解析，zlib 块解压，批量提取 |
| `pak_builder.py` | 替换模组 PAK 构建，魔数校验，Index 重建 |
| `skeleton_analyzer.py` | 骨骼结构自动分析，SkeletalMesh 命名规律推断 |

## 许可证

MIT
