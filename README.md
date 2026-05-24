# 🧠 全植入式脑电信号与信息压缩系统：文献计量与系统化分析

> **项目简介**
> 本项目旨在系统呈现全植入式情景下的脑电信号与信息压缩系统设计。通过对 Web of Science 数据库中相关文献的深度挖掘与文献计量分析，明晰脑电信号采集的基本原理与经典电路架构，梳理压缩算法与信号特征的适配逻辑，为全植入式脑机接口（BCI）的未来发展提供理论支撑与技术演进脉络。

---

## 🎯 研究内容与核心目标

本项目重点围绕“医学领域的全植入应用”开展研究，旨在回答以下五个核心问题：

1. **发文趋势与阶段特征**：分析 2020–2025 年间 BCI 与信号采集电路相关研究的年度发文趋势，总结各阶段演进规律。
2. **场景瓶颈与解决方案**：剖析全植入场景下信号采样存在的固有局限，归纳采集、传输与压缩环节的技术破局路径。
3. **研究热点识别与演化**：通过关键词共现与演化分析，识别领域核心热点及研究重心的转移规律。
4. **高被引文献与技术演进**：梳理代表性高被引文献，总结全植入式信号处理与信息压缩的技术发展脉络。
5. **现存问题与未来方向**：基于文献证据链，提炼当前研究的痛点，研判未来的科学发展方向。

---

## 📊 PRISMA 文献筛选流程

本项目严格遵循 PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) 标准进行文献筛选，确保数据来源的透明性与可重复性。

*(图片命名为 `prisma_flowchart.png` 并放置于 `outputs/` 目录下)*

**筛选阶段说明：**

1. **识别 (Identification)**
通过 Web of Science 数据库检索获得初始记录：$n = 16,000$ 篇。
2. **初筛 (Screening)**
进入自动化脚本初筛的记录：$n = 16,000$ 篇。
因不符合纳入标准被排除的记录总数：$n = 4,797$ 篇。
* 排除原因 1 (E1: 主题不符/缺乏硬件及压缩要素)：$n = 2,294$ 篇。
* 排除原因 2 (E3: 纯动物实验)：$n = 14$ 篇。
* 排除原因 3 (E4: 纯深度学习/高功耗算法)：$n = 2,489$ 篇。


3. **纳入 (Included)**
最终纳入用于 CiteSpace / VOSviewer 文献计量学分析的文献总量：$n = 11,203$ 篇。

---

## 🔍 检索策略与配置

### 配置文件 (`config/query.yaml`)

项目的基础检索配置参数如下：

```yaml
query:
  object:
    # 对应检索式中的植入式系统与神经信号模态
    - "implant*"
    - "invasive"
    - "neural interfac*"
    - "neural record*"
    - "ECoG"
    - "LFP"
    - "EEG"
  method:
    # 对应检索式中的片上数据处理与压缩技术
    - "compress*"
    - "data reduc*"
    - "compressive sensing"
    - "feature extract*"
    - "on-chip process*"
    - "edge comput*"
  context:
    # 对应检索式中的人类/临床研究限制条件
    - "human*"
    - "patient*"
    - "clinical"
    - "subject*"
  exclusion:
    # 对应检索式中 NOT 排除的动物实验与非相关模型
    - "rat"
    - "rats"
    - "mouse"
    - "mice"
    - "rodent*"
    - "macaque*"
    - "monkey*"
    - "primate*"
    - "animal model*"
    - "feline"
    - "canine"
    - "pig"
    - "porcine"
  time_window: [2010, 2025]

```

###  高级布尔检索式 (WoS)

为了精准定位“全植入、人类研究、硬件/压缩处理”并排除干扰项，采用如下检索表达式：

```text
(TS=(implant* OR invasive OR "neural interfac*" OR "neural record*" OR ECoG OR LFP OR EEG) 
AND TS=(compress* OR "data reduc*" OR "compressive sensing" OR "feature extract*" OR "on-chip process*" OR "edge comput*") 
AND TS=(human* OR patient* OR clinical OR subject*) 
AND PY=(2010-2026)) 
NOT TS=(rat OR rats OR mouse OR mice OR rodent* OR macaque* OR monkey* OR primate* OR "animal model*" OR feline OR canine OR pig OR porcine)

```

---

## 📈 共被引分析

### 最高被引文献统计(Top 5)：

* **Koelstra S, 2012**, IEEE T AFFECT COMPUT, V3, P18, DOI: 10.1109/T-AFFC.2011.15 **(183 次)**
* **Wolpaw JR, 2002**, CLIN NEUROPHYSIOL, V113, P767, DOI: 10.1016/S1388-2457(02)00057-3 **(174 次)**
* **Delorme A, 2004**, J NEUROSCI METH, V134, P9, DOI: 10.1016/j.jneumeth.2003.10.009 **(164 次)**
* **Ramoser H, 2000**, IEEE T REHABIL ENG, V8, P441, DOI: 10.1109/86.895946 **(158 次)**
* **Goldberger AL, 2000**, CIRCULATION, V101, pE215, DOI: 10.1161/01.CIR.101.23.e215 **(155 次)**

---

## 📂 项目目录结构

项目采用模块化结构设计，实现数据、代码与文档的彻底解耦，提升项目的可维护性与可复现性。

```text
📦 Citespace-homework
 ┣ 📂 data/          # 存放原始数据及各阶段筛选结果（CSV/TXT）
 ┣ 📂 src/           # 存放筛选逻辑与数据处理脚本 (如 stage1_clean.py, stage2_analyze.py)
 ┣ 📂 reports/       # 存放方法文档、过程记录与最终分析报告
 ┣ 📂 outputs/       # 存放生成的图像结果（如 PRISMA 流程图、图谱可视化）
 ┣ 📂 config/        # 存放配置文件（如 query.yaml）
 ┗ 📜 README.md      # 项目整体说明文档

```

---

## 👥 团队成员与分工

本项目由跨学科团队协作完成，具体分工如下：

| 姓名 | 负责角色 | 核心工作内容与具体交付物细则 (M1-M3 全周期) |
| --- | --- | --- |
| **曹亦宸** | 组长/数据获取/代码实现| 统筹项目进度，定义检索策略，实现检索与筛选代码 |
| **薛逢利** | 数据分析/文献写作 | **TODO: 把你们完成了什么东西写在这里...**|
| **刘沅鑫** | 数据分析/文献写作 | **TODO: 把你们完成了什么东西写在这里...** |
| **杨行行** | 数据分析/文献写作 | **TODO: 把你们完成了什么东西写在这里...**|
| **宁健涛** | 数据分析/文献写作| **TODO: 把你们完成了什么东西写在这里...** |


## 🛠️ 核心技术栈与工具链 (Tech Stack)

* **数据来源**：Web of Science core collection (保障全字段覆盖率与高信度学术源)
* **数据清洗与分析**：Python 3.12, Pandas (提供高效的向量化去重与缺失值处理)
* **可视化引擎**：Matplotlib，Citespace
* **知识图谱 (M2规划)**：Citespace (网络拓扑构建与共现图谱渲染)
* **工程协同**：Git & GitHub Desktop (全流程版本控制)

---

## 🚀 快速复现指南 (Quick Start)

本项目秉持"完全开源、一键复现"原则，任何研究人员均可通过以下步骤复现本项目的 M1 数据清洗与可视化分析结果：

**1. 克隆本仓库到本地**
```bash
git clone [https://github.com/Chin-Quency/citespace-homework.git](https://github.com/Chin-Quency/citespace-homework.git)
cd citespace-homework/src

```

**2. 安装 Python 依赖环境**

```bash
pip install -r requirements.txt

```

**3. 运行自动化质检与可视化流水线**

```bash
python citespace.py
python filter.py
python evidence_chain.py
python evidence_analyze.py

# 【可选】共被引矩阵分析（需要的时间较长）
python extract_citation.py
python co_citation.py

```

> **注**：运行成功后，最新的趋势与研究方向总结，以及字段缺失率报告将自动生成并保存在 `outputs/` 目录下。

---

## 📅 项目核心里程碑 (Milestones)

* **[x] M1 阶段：数据与检索方案验证（第 4 周）**
首先完成原始数据的结构化解析与基于 PRISMA 标准的严格清洗初筛，随后对核心文献的硬件架构与压缩算法指标进行深度特征提取与多维量化统计，构建出坚实的学术证据链；在此基础上，系统还提供可选的深度引文分析模块，通过解析全字段引用关系并引入动态阈值降噪，精准生成核心共被引矩阵与相似度网络边表，为最终渲染可视化图谱并揭示该领域的技术演进脉络奠定了完整、高质量的数据基础。
* **[ ] M2 阶段：计量分析与图谱产出（第 10 周）**

  >**TODO: 把你们完成了什么其他东西写在这里...** (请在此处继续补充)
* **[ ] M3 阶段：终稿与项目归档（第 15 周）**
整合前期计量证据链，提交终版学术综述（Mini Review）稿件。代码整理与注释归档，确保所有网络图谱 100% 可复现。
