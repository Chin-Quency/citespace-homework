<img width="711" height="80" alt="image" src="https://github.com/user-attachments/assets/5b664337-2c2a-41fb-a065-ea89afd3ae4c" /># 全植入式脑电信号与信息压缩系统：文献计量与系统化分析

> 本项目旨在系统呈现全植入式情景下的脑电信号与信息压缩系统设计。通过对 Web of Science 数据库中相关文献的深度挖掘与文献计量分析，明晰脑电信号采集的基本原理与经典电路架构，梳理压缩算法与信号特征的适配逻辑，为全植入式脑机接口（BCI）的未来发展提供理论支撑与技术演进脉络。

---

## 一、研究内容与核心目标

本项目重点围绕"医学领域的全植入应用"开展研究，旨在回答以下五个核心问题：

1. **发文趋势与阶段特征**：分析 2020–2025 年间 BCI 与信号采集电路相关研究的年度发文趋势，总结各阶段演进规律。
2. **场景瓶颈与解决方案**：剖析全植入场景下信号采样存在的固有局限，归纳采集、传输与压缩环节的技术破局路径。
3. **研究热点识别与演化**：通过关键词共现与演化分析，识别领域核心热点及研究重心的转移规律。
4. **高被引文献与技术演进**：梳理代表性高被引文献，总结全植入式信号处理与信息压缩的技术发展脉络。
5. **现存问题与未来方向**：基于文献证据链，提炼当前研究的痛点，研判未来的科学发展方向。

---

## 二、PRISMA 文献筛选流程

本项目严格遵循 PRISMA 标准进行文献筛选，确保数据来源的透明性与可重复性。

![PRISMA Flowchart](outputs/prisma_flowchart.png)

| 阶段 | 数量 | 说明 |
|------|------|------|
| **Identification** | 16,000 | Web of Science 数据库检索 |
| **Screening** | 16,000 | 自动化脚本初筛 |
| **Excluded** | 10,310 | 不符合纳入标准 |
| - E1 主题不符 | 2,294 | 缺乏硬件及压缩要素 |
| - E3 纯动物实验 | 14 | 无人类受试者 |
| - E4 纯深度学习/高功耗算法 | 2,489 | 不符合低功耗硬件导向 |
| - E5 非神经领域医疗噪音 | 5,513 | 骨科/外科/心血管等无关文献 |
| **Included** | 5,690 | 纳入 CiteSpace / VOSviewer 分析 |

---

## 三、检索策略

### 配置文件 (`config/query.yaml`)

```yaml
query:
  object:
    - "implant*"
    - "invasive"
    - "neural interfac*"
    - "neural record*"
    - "ECoG"
    - "LFP"
    - "EEG"
  method:
    - "compress*"
    - "data reduc*"
    - "compressive sensing"
    - "feature extract*"
    - "on-chip process*"
    - "edge comput*"
  context:
    - "human*"
    - "patient*"
    - "clinical"
    - "subject*"
  exclusion:
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

### 高级布尔检索式 (WoS)

```text
(TS=(implant* OR invasive OR "neural interfac*" OR "neural record*" OR ECoG OR LFP OR EEG)
AND TS=(compress* OR "data reduc*" OR "compressive sensing" OR "feature extract*" OR "on-chip process*" OR "edge comput*")
AND TS=(human* OR patient* OR clinical OR subject*)
AND PY=(2010-2026))
NOT TS=(rat OR rats OR mouse OR mice OR rodent* OR macaque* OR monkey* OR primate* OR "animal model*" OR feline OR canine OR pig OR porcine)
```

---

## 四、核心计量发现

对 5,690 篇纳入文献的系统化计量分析揭示了以下核心发现：

**(1) 电路架构层面**，片上系统（SoC, 1,024 篇）与模拟前端（AFE, 696 篇）构成植入式神经记录系统的两大硬件支柱，特征提取（Feature Extraction, 1,995 篇）为最广泛采用的数据处理范式，离散小波变换（DWT）与主成分分析（PCA）分别以 194 篇和 222 篇位列经典压缩算法前两位。

**(2) 信号模态层面**，皮层脑电（ECoG）以 14.4% 的占比（821 篇）主导侵入式信号采集，显著高于动作电位（Spike, 0.6%）与局部场电位（LFP, 0.3%），表明 ECoG 因其较高的空间分辨率与较低的侵入风险，成为全植入式 BCI 的首选信号源。

**(3) 功耗与压缩层面**，25 篇量化文献中功耗中位数为 1,600 uW，32.0% 的设计达到 10 uW 以下极低功耗；1,440 篇文献报告了压缩性能，86.8% 实现了 10 倍以上压缩比，表明高压缩率与低功耗的协同优化已成为领域共识。

**(4) 工艺制程层面**，65 nm 工艺节点占比最高（15.6%），其次为 180 nm（8.9%），反映出先进制程与成熟制程并存的格局——前者追求极致低功耗，后者兼顾制造成本与可靠性。

**(5) 临床应用层面**，植入式神经接口（17.8%）为首要应用场景，运动解码/神经假体（11.1%）与癫痫检测（8.1%）紧随其后，闭环刺激（2.1%）虽占比最低但增长势头显著，指向"感知-决策-干预"一体化的发展方向。

**(6) 知识演化层面**，CiteSpace 关键词聚类揭示六大知识基础（#0 三叉神经痛、#1 机器学习、#2 运动想象、#3 脑建模、#4 阿尔茨海默症、#5 急性深静脉血栓），时间线视图呈现"信号采集 → 处理 → 压缩 → 临床应用"的完整技术链条，EEG 与 BCI 为贯穿始终的核心节点。

---

## 五、共被引分析

### 最高被引文献 (Top 5)

| 排名 | 文献 | 被引次数 |
|------|------|----------|
| 1 | Koelstra S, 2012, IEEE T AFFECT COMPUT, V3, P18 | 183 |
| 2 | Wolpaw JR, 2002, CLIN NEUROPHYSIOL, V113, P767 | 174 |
| 3 | Delorme A, 2004, J NEUROSCI METH, V134, P9 | 164 |
| 4 | Ramoser H, 2000, IEEE T REHABIL ENG, V8, P441 | 158 |
| 5 | Goldberger AL, 2000, CIRCULATION, V101, pE215 | 155 |

---

## 六、项目目录结构

```
citespace-homework/
├── config/              # 配置文件 (query.yaml)
├── data/                # 原始数据及筛选结果 (CSV/TXT)
├── src/                 # 数据处理脚本
│   ├── run_pipeline.py  # 一键流水线入口
│   ├── citespace.py     # 数据加载与字段统计
│   ├── filter.py        # PRISMA 筛选
│   ├── evidence_chain.py      # 证据链特征提取
│   ├── evidence_analyze.py    # 证据链统计分析
│   ├── extract_citations.py   # 引文边表提取
│   ├── co_citation.py         # 共被引矩阵分析
│   └── draw_prisma.py         # PRISMA 流程图绘制
├── outputs/             # 输出结果 (图表/CSV/TXT)
├── report/              # 分析报告与可视化图谱
│   ├── author_collaboration/   # 作者合作网络
│   ├── co_citation_network/    # 关键词聚类
│   └── timeline/               # 时间线图谱
└── README.md
```

---

## 七、快速复现指南

```bash
# 1. 克隆仓库
git clone https://github.com/Chin-Quency/citespace-homework.git
cd citespace-homework

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行主流水线
python src/run_pipeline.py

# 4. 运行完整流水线（含共被引分析，耗时较长）
python src/run_pipeline.py --with-co-citation
```

运行成功后，筛选结果、证据链统计与字段缺失率报告将自动保存在 `outputs/` 目录下。

---

## 八、技术栈

| 类别 | 工具 |
|------|------|
| 数据来源 | Web of Science Core Collection |
| 数据清洗与分析 | Python 3.12, Pandas |
| 可视化 | Matplotlib, CiteSpace |
| 知识图谱 | CiteSpace (网络拓扑与共现图谱) |
| 工程协同 | Git & GitHub |

---

## 九、团队成员与分工

| 姓名 | 角色 | 核心工作内容 |
|------|------|-------------|
| **曹亦宸** | 组长 / 数据获取 / 代码实现 | 统筹项目进度，定义检索策略，实现检索与筛选代码, ppt制作 |
| **薛逢利** | 数据分析 | 作者合作网络,ppt制作,数据检索与筛选 |
| **刘沅鑫** | 数据分析 | 关键词时间线,文献耦合与合作网络实现 |
| **杨行行** | 数据分析 | Top10论文列表,文献耦合与合作网络实现 |
| **宁健涛** | 数据分析 | 关键词聚类图,共被引网络建模 |



---

## 十、项目里程碑

- **[x] M1：数据与检索方案验证（第 4 周）**
  完成原始数据结构化解析与 PRISMA 标准清洗初筛，对核心文献的硬件架构与压缩算法指标进行深度特征提取与多维量化统计，构建学术证据链；提供可选的深度引文分析模块，生成共被引矩阵与相似度网络边表。

- **[ ] M2：计量分析与图谱产出（第 10 周）**
  TODO

- **[ ] M3：终稿与项目归档（第 15 周）**
  整合前期计量证据链，提交终版学术综述（Mini Review）稿件。代码整理与注释归档，确保所有网络图谱 100% 可复现。
