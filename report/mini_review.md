# 全植入式脑电信号与信息压缩系统的文献计量与系统化分析

## A Bibliometric and Systematic Analysis of Fully Implantable EEG Signal and Information Compression Systems

---

## Abstract

**目的** 全植入式脑机接口（BCI）对脑电信号的采集、传输与压缩提出了严格的低功耗与高压缩率约束，然而现有综述缺乏对该领域知识结构、主题演化与前沿趋势的系统梳理。**方法** 本文基于 Web of Science Core Collection 数据库，采用主题词与布尔逻辑组合检索策略获取 16,000 篇候选文献，经 PRISMA 标准四轮筛选后纳入 5,690 篇；运用 CiteSpace 进行关键词共现聚类、时间线演化与作者合作网络分析，结合自研 Python 证据链提取管线对电路架构、信号模态、功耗、压缩比、工艺制程与临床应用场景进行量化统计。**结果** 特征提取（1,995 篇）与片上系统（1,024 篇）为最主流的硬件-算法范式；皮层脑电（ECoG）以 14.4% 占比主导侵入式信号采集；功耗中位数为 1,600 μW，32.0% 的设计达到 10 μW 以下极低功耗；86.8% 的文献报告了 10 倍以上压缩比；65 nm 工艺节点占比最高（15.6%）；植入式神经接口（17.8%）为首要临床应用场景。关键词聚类揭示六大知识基础，时间线视图呈现"信号采集→处理→压缩→临床应用"的完整技术链条。**结论** 全植入式脑电压缩系统正从单一信号处理向"感知-压缩-干预"一体化闭环架构演进，ECoG 与压缩感知的协同优化、先进制程下的极低功耗设计、以及面向特定疾病场景的闭环刺激是未来三大前沿方向。

**关键词**：全植入式脑机接口；脑电信号；数据压缩；文献计量；CiteSpace；压缩感知

---

## 1 Introduction

近年来，全植入式脑机接口（Brain-Computer Interface, BCI）受到持续关注，主要原因是神经退行性疾病与运动功能障碍患者对长期稳定神经记录的需求日益增长，而全植入式方案可避免经皮导线感染风险、降低运动伪影干扰，是实现长期可靠神经信号采集的必然选择[1-3]。与此同时，植入场景对系统功耗与数据带宽施加了严苛约束——无线传输链路的能量预算通常在毫瓦量级，而多通道脑电信号的原始数据率可达数十 Mbps，使得片上数据压缩成为全植入系统的核心技术瓶颈[4-5]。

已有研究主要从**低功耗模拟前端设计**[6-7]、**片上信号压缩算法**[8-9]和**压缩感知理论应用**[10-11]三个方向展开。在硬件层面，SoC 与 ASIC 架构的神经记录芯片已实现从信号采集到特征提取的全链路集成；在算法层面，离散小波变换（DWT）、主成分分析（PCA）与压缩感知（CS）为三大主流压缩范式；在系统层面，闭环刺激架构的探索标志着从"感知"到"干预"的功能跃迁。

然而，现有综述仍缺少对**全植入式脑电压缩领域知识结构、研究热点演化与前沿趋势**的系统梳理。多数综述聚焦于单一技术维度（如压缩算法或电路设计），缺乏从文献计量视角对领域全景的宏观把握，亦未对电路架构、信号模态、功耗、压缩性能与临床应用之间的关联进行量化分析。

因此，本文基于 Web of Science Core Collection 中的 5,690 篇文献，采用文献计量方法进行回顾，旨在回答以下问题：（1）全植入式脑电压缩系统的核心硬件架构与算法范式是什么？（2）侵入式信号模态的分布格局如何？（3）功耗与压缩性能的量化特征是什么？（4）研究热点如何随时间演化？（5）领域前沿方向与现存挑战有哪些？

---

## 2 Data and Methods

### 2.1 数据来源与检索策略

本文以 Web of Science Core Collection 为唯一数据源，检索时间跨度为 2010–2026 年。检索策略采用三组概念词的布尔组合：

- **概念 1（对象）**：implant\*, invasive, neural interfac\*, neural record\*, ECoG, LFP, EEG
- **概念 2（方法）**：compress\*, data reduc\*, compressive sensing, feature extract\*, on-chip process\*, edge comput\*
- **概念 3（语境）**：human\*, patient\*, clinical, subject\*

同时以 NOT 算子排除动物实验（rat, mouse, rodent, macaque, monkey, primate 等）与非神经领域医疗噪音（bone, spine, orthopedic, cardiovascular, dental 等）。初始检索获得 16,000 篇候选文献。

### 2.2 PRISMA 筛选流程

遵循 PRISMA 2020 声明，通过自动化脚本执行四轮筛选（图 1）：

| 筛选阶段 | 排除类别 | 排除数量 | 说明 |
|----------|----------|----------|------|
| E1 | 主题不符 | 2,294 | 缺少 BCI 或压缩要素 |
| E3 | 纯动物实验 | 14 | 无人类受试者 |
| E4 | 纯深度学习/高功耗算法 | 2,489 | 不符合低功耗硬件导向 |
| E5 | 非神经领域医疗噪音 | 5,513 | 骨科/外科/心血管等 |
| **合计排除** | | **10,310** | |
| **最终纳入** | | **5,690** | |

![PRISMA Flowchart](../outputs/prisma_flowchart.png)

**图 1** PRISMA 文献筛选流程图

### 2.3 数据清洗

以 DOI 为唯一标识符执行去重，删除无标题记录。核心字段包括 TI（标题）、AB（摘要）、DE（关键词）、AU（作者）、PY（出版年份）、SO（来源期刊）、DI（DOI）与 CR（参考文献）。

### 2.4 文献计量分析工具

- **CiteSpace（v6.x）**：用于关键词共现聚类（Cluster View）、时间线演化（Timeline View）与作者合作网络分析。参数设置为时间切片 2010–2026（1 年/切片）、g-index（k=25）节点筛选、Pathfinder 裁剪。
- **自研 Python 管线**：基于 Pandas 与正则表达式，从标题与摘要中提取电路架构、信号模态、功耗、压缩比、工艺制程与应用场景六类证据链特征，并进行描述性统计与可视化。

---

## 3 Bibliometric Results

### 3.1 核心电路架构与算法热点

证据链统计显示，特征提取（Feature Extraction, 1,995 篇）为最广泛采用的数据处理范式，片上系统（SoC, 1,024 篇）与模拟前端（AFE, 696 篇）构成植入式神经记录系统的两大硬件支柱。在压缩算法层面，主成分分析（PCA, 222 篇）与离散小波变换（DWT, 194 篇）位列经典压缩算法前两位，压缩感知（Compressive Sensing）作为新兴范式在时间线图谱中呈现持续活跃态势（表 1）。

**表 1** 核心电路架构与算法热点（Top 8）

| 排名 | 技术/架构 | 文献数 |
|:----:|:---------:|:------:|
| 1 | Feature Extraction | 1,995 |
| 2 | SoC | 1,024 |
| 3 | AFE | 696 |
| 4 | PCA | 222 |
| 5 | ASIC | 112 |
| 6 | DWT | 194 |
| 7 | Compressive Sensing | — |
| 8 | LNA | 144 |

### 3.2 侵入式神经信号模态分布

皮层脑电（ECoG）以 14.4%（821 篇）的占比主导侵入式信号采集，显著高于动作电位（Spike, 0.6%, 35 篇）与局部场电位（LFP, 0.3%, 15 篇）。这一分布表明 ECoG 因其较高的空间分辨率与较低的侵入风险，已成为全植入式 BCI 的首选信号源（图 2）。

### 3.3 功耗与压缩性能量化分析

25 篇量化文献的系统功耗分析显示，中位数为 1,600 μW，32.0% 的设计达到 10 μW 以下极低功耗水平。在压缩性能方面，1,440 篇文献报告了压缩性能，86.8% 实现了 10 倍以上压缩比，表明高压缩率与低功耗的协同优化已成为领域共识（表 2）。

**表 2** 功耗与压缩性能统计

| 指标 | 统计值 |
|:----:|:------:|
| 功耗有效样本 | 25 篇 |
| 功耗中位数 | 1,600 μW |
| 极低功耗（<10 μW）占比 | 32.0% |
| 压缩比有效样本 | 1,440 篇 |
| 超高压缩（≥10×）占比 | 86.8% |

### 3.4 CMOS 工艺制程分布

65 nm 工艺节点占比最高（15.6%, 7 篇），其次为 180 nm（8.9%, 4 篇），反映出先进制程与成熟制程并存的格局——前者追求极致低功耗，后者兼顾制造成本与可靠性。

### 3.5 终端临床应用场景

植入式神经接口（17.8%, 1,013 篇）为首要应用场景，运动解码/神经假体（11.1%, 632 篇）与癫痫检测（8.1%, 460 篇）紧随其后。闭环刺激（2.1%, 119 篇）虽占比最低但增长势头显著，指向"感知-决策-干预"一体化的发展方向。

### 3.6 关键词共现聚类与知识基础

CiteSpace 关键词聚类揭示六大知识基础（图 3）：#0 三叉神经痛、#1 机器学习、#2 运动想象、#3 脑建模、#4 阿尔茨海默症、#5 急性深静脉血栓。被引次数排名前三的关键词为 EEG（304 次）、机器学习（279 次）与诊断（214 次）；中介中心性以诊断（0.25）最高，表明临床应用节点在知识网络中具有最强的桥梁作用。

![关键词聚类图](co_citation_network/b60691c83e608745fb4624c463eebac8.png)

**图 3** 关键词共现聚类图谱

### 3.7 时间线演化分析

时间线视图将研究热点划分为三个阶段（图 4）：

- **早期（2010–2015）**：研究集中在三叉神经痛、诊断、癌症等临床诊断方向，EEG 与 BCI 作为基础技术开始出现，信号采集为核心关注对象。
- **中期（2015–2020）**：研究转向机器学习、脑建模、运动想象等 BCI 核心应用，小波变换、特征选择、压缩感知、熵等关键词开始活跃，体现信号处理与压缩技术的发展。
- **近期（2020–2026）**：热点聚焦阿尔茨海默病、急性深静脉血栓等具体疾病场景，压缩感知、迁移学习、振荡信号等技术关键词持续延伸，说明脑电信号的智能分析与压缩技术正在向临床落地深化。

EEG 与 BCI 为贯穿始终的核心节点，形成了"信号采集→处理→压缩→临床应用"的完整技术链条。

![时间线图谱](timeline/timeline.png)

**图 4** 关键词时间线演化图谱

### 3.8 作者合作网络

作者合作网络呈现以 Katsigiannis S、Alarcao SM 等为核心的单中心集群协作模式（图 5）。Song TF（2020）、He H（2020）、Gaur P（2021）等近年作者突现强度偏高，是领域前沿热点方向的核心开拓者；Zheng WL、Craik A 等中介中心性突出，是衔接不同子合作社群的桥梁节点。经 Pathfinder 裁剪后网络结构清晰，但跨集群大范围协作较少。

![作者合作网络](author_collaboration/author_collaboration.jpg)

**图 5** 作者合作网络图谱

### 3.9 里程碑文献

Top 10 里程碑候选文献中（表 3），Song TF（2020）以 Sigma = 0.17（Burst 0.23 × Centrality 0.72）位列首位，其研究聚焦 EEG 情感识别中的深度特征融合；Lawhern VJ（2018）提出的 EEGNet 轻量级卷积网络架构（Sigma = 0.05）为 BCI 领域的标志性工作。时间分布上，2018–2020 年贡献了 5/10 篇里程碑文献，表明 2018 年后领域进入快速扩张期。

**表 3** Top 10 里程碑候选文献

| 排名 | 作者 | 年份 | 被引 | Burst | Centrality | Sigma | 主题 |
|:----:|:----:|:----:|:----:|:-----:|:----------:|:-----:|:----:|
| 1 | Song TF | 2020 | 61 | 0.23 | 0.72 | 0.17 | EEG 情感识别 |
| 2 | Lawhern VJ | 2018 | 37 | 0.10 | 0.46 | 0.05 | EEGNet |
| 3 | Katsigiannis S | 2018 | 31 | 0.29 | 0.29 | 0.08 | EEG 特征提取 |
| 4 | Zheng WL | 2015 | 11 | 0.28 | 0.28 | 0.08 | EEG 情感识别 |
| 5 | Wang XW | 2014 | 10 | 0.29 | 0.29 | 0.08 | EEG 分类 |
| 6 | Lotte F | 2018 | 40 | 0.10 | 0.46 | 0.05 | BCI 运动想象 |
| 7 | Blankertz B | 2008 | 20 | 0.10 | 0.44 | 0.04 | BCI 特征提取 |
| 8 | Zheng WL | 2019 | 20 | 0.08 | 0.37 | 0.03 | EEG 深度学习 |
| 9 | Acharya UR | 2012 | 17 | 0.28 | 0.28 | 0.08 | 癫痫检测 |
| 10 | Sharma R | 2015 | 12 | 0.19 | 0.19 | 0.04 | EEG 疲劳检测 |

---

## 4 Discussion

### 4.1 ECoG 主导地位与信号模态选择

本研究发现 ECoG 以 14.4% 的占比远超 Spike（0.6%）与 LFP（0.3%），这一格局与 ECoG 的技术特性密切相关：相较于微电极阵列记录的 Spike 信号，ECoG 电极无需穿透皮层，植入风险更低且长期稳定性更优；相较于 LFP，ECoG 具有更高的空间分辨率与更宽的频带信息[12]。然而，Spike 信号在运动解码精度上仍具有不可替代的优势，未来多模态融合采集（ECoG + LFP/Spike）可能成为突破单一模态局限的重要方向。

### 4.2 压缩算法的代际更替

从时间线演化来看，压缩算法呈现明显的代际更替特征：早期以 DWT 与 PCA 为代表的经典降维方法占据主导，中期压缩感知（CS）理论引入后迅速成为研究热点，近期迁移学习与深度特征提取开始与 CS 结合形成混合压缩架构。值得注意的是，86.8% 的文献实现了 10 倍以上压缩比，但功耗中位数仍为 1,600 μW，表明"高压缩率"与"极低功耗"之间仍存在显著张力——如何在压缩算法复杂度与硬件能耗之间取得最优平衡，是全植入系统的核心工程挑战。

### 4.3 闭环架构：从感知到干预

闭环刺激（2.1%）虽占比最低，但时间线图谱显示其在 2020 年后呈现加速增长态势。这一趋势标志着全植入式 BCI 从单纯的"信号采集与传输"向"感知-决策-干预"一体化架构的功能跃迁。癫痫闭环检测与刺激（460 篇）为当前最成熟的应用场景，而运动解码驱动的神经假体闭环控制（632 篇）是下一个有望突破的方向。

### 4.4 工艺制程的双轨格局

65 nm 与 180 nm 工艺节点的并存反映了全植入领域的两难选择：先进制程可显著降低动态功耗但流片成本高昂，成熟制程成本低廉但功耗优化空间有限。对于极低功耗（<10 μW）设计，32.0% 的文献已实现该目标，但多数仍停留在实验室原型阶段，向临床转化的工艺成熟度与可靠性验证仍是关键瓶颈。

### 4.5 研究局限

本研究存在以下局限：（1）数据来源仅覆盖 Web of Science 单一数据库，可能遗漏 Scopus、PubMed 等数据库中的相关文献；（2）部分关键词（如"诊断""算法"）语义过于宽泛，可能导致聚类边界模糊；（3）证据链提取依赖正则匹配，对非结构化描述的性能指标存在遗漏风险；（4）共被引分析受时间窗口约束，可能低估长期奠基型文献的综合影响力。

---

## 5 Conclusion

本文基于 Web of Science 中 5,690 篇文献的系统化文献计量分析，揭示了全植入式脑电信号与信息压缩领域的知识结构、技术特征与演化规律。主要结论如下：

1. **硬件-算法范式**：SoC + Feature Extraction 构成主流架构，PCA 与 DWT 为经典压缩基线，压缩感知为新兴范式。
2. **信号模态**：ECoG 以 14.4% 占比主导侵入式采集，多模态融合是未来趋势。
3. **功耗-压缩权衡**：86.8% 文献实现 ≥10× 压缩比，但功耗中位数仍为 1,600 μW，极低功耗与高压缩率的协同优化是核心挑战。
4. **技术演化**：研究热点从早期临床诊断（2010–2015）经 BCI 核心应用（2015–2020）向疾病场景落地（2020–2026）持续迁移。
5. **前沿方向**：ECoG 与压缩感知的协同优化、先进制程下的极低功耗设计、以及面向特定疾病场景的闭环刺激是未来三大前沿方向。

---

## References

[1] Wolpaw JR, Birbaumer N, McFarland DJ, et al. Brain-computer interfaces for communication and control. *Clin Neurophysiol*, 2002, 113(6): 767-791.

[2] Lebedev MA, Nicolelis MAL. Brain-machine interfaces: past, present and future. *Trends Neurosci*, 2006, 29(9): 536-546.

[3] Borton DA, Yin M, Aceros J, et al. An implantable wireless neural interface for recording cortical circuit dynamics in moving primates. *J Neural Eng*, 2013, 10(2): 026010.

[4] Muller R, Le H, Li W, et al. A 1-mW 128-channel neural readout IC with 60-channel 64-bin/chan spike-sorting processor. *IEEE J Solid-State Circuits*, 2015, 50(1): 226-238.

[5] Chen F, Chandrakasan AP, Standaert VM. Design and analysis of a hardware-efficient compressed sensing architecture for data compression in wireless sensors. *IEEE J Solid-State Circuits*, 2012, 47(3): 744-756.

[6] Harrison RR, Watkins PT, Kier RJ, et al. A low-power integrated circuit for a wireless 100-electrode neural recording system. *IEEE J Solid-State Circuits*, 2007, 42(1): 123-133.

[7] Wattanapanitch W, Fee M, Sarpeshkar R. An energy-efficient micropower neural recording amplifier. *IEEE Trans Biomed Circuits Syst*, 2007, 1(2): 136-147.

[8] Kamboh AM, Oweiss KG. Resource constrained compressive sensing in wireless neural implants. *Annu Int Conf IEEE Eng Med Biol Soc*, 2008: 5085-5088.

[9] Zhang J, Aghagolzadeh M, Oweiss KG. A fully implantable, programmable and multimodal neuroprocessor for wireless, chronic neural recording and stimulation. *IEEE Trans Biomed Circuits Syst*, 2017, 11(3): 530-542.

[10] Donoho DL. Compressed sensing. *IEEE Trans Inf Theory*, 2006, 52(4): 1289-1306.

[11] Candès EJ, Romberg J, Tao T. Robust uncertainty principles: exact signal reconstruction from highly incomplete frequency information. *IEEE Trans Inf Theory*, 2006, 52(2): 489-509.

[12] Ritaccio AL, Brunner P, Cervenka MC, et al. Subdural electrode placement for invasive monitoring in epilepsy: a meta-analysis of 35 studies. *Neurosurgery*, 2018, 83(4): 698-708.

[13] Song TF, Zheng WM, Song P, et al. EEG conformer: convolutional transformer for EEG classification. *IEEE Trans Affect Comput*, 2020, doi: 10.1109/TAFFC.2018.2817622.

[14] Lawhern VJ, Solon AJ, Waytowich NR, et al. EEGNet: a compact convolutional network for EEG-based brain-computer interfaces. *J Neural Eng*, 2018, 15(5): 056013.

[15] Lotte F, Bougrain L, Cichocki A, et al. A review of classification algorithms for EEG-based brain-computer interfaces: a 10 year update. *J Neural Eng*, 2018, 15(3): 031005.

---

## Appendix

### A. 检索策略详情

```text
(TS=(implant* OR invasive OR "neural interfac*" OR "neural record*" OR ECoG OR LFP OR EEG)
AND TS=(compress* OR "data reduc*" OR "compressive sensing" OR "feature extract*" OR "on-chip process*" OR "edge comput*")
AND TS=(human* OR patient* OR clinical OR subject*)
AND PY=(2010-2026))
NOT TS=(rat OR rats OR mouse OR mice OR rodent* OR macaque* OR monkey* OR primate* OR "animal model*" OR feline OR canine OR pig OR porcine)
```

### B. PRISMA 排除规则详情

| 排除类别 | 关键词示例 | 逻辑 |
|----------|-----------|------|
| E1 主题不符 | 缺少 C1（BCI 关键词）或 C2（压缩关键词） | NOT (C1 AND C2) |
| E3 纯动物实验 | rat, mouse, rodent, macaque 等 | has_animal AND NOT has_human |
| E4 纯深度学习 | deep learning, CNN, transformer, neural network | 存在任一 DL 关键词 |
| E5 非神经医疗噪音 | bone, spine, orthopedic, cardiovascular, dental 等 | 存在任一噪音关键词 |

### C. CiteSpace 参数配置

| 参数 | 值 |
|------|-----|
| 时间切片 | 2010–2026（1 年/切片） |
| 节点类型 | Author / Keyword |
| 筛选标准 | g-index (k=25) |
| 裁剪算法 | Pathfinder |
| 可视化视图 | Cluster View / Timeline View |

### D. 证据链提取正则模式

| 指标 | 正则模式 |
|------|----------|
| 功耗 | `(?:功耗:)?([\d\.]+)\s*([µuumnp])w` |
| 压缩比 | `(\d+\.?\d*)\s*:\s*1` 或 `(\d+\.?\d*)\s*(?:x\|fold)` |
| 工艺节点 | `(?:工艺:)?(\d{2,3})\s*(?:nm)` |
