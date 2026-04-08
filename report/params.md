# 项目参数配置文件 (Params.md) - BCI 全植入系统专题

## 一、 项目基础信息 (Basic Information)

| 参数项 | 内容描述 |
| :--- | :--- |
| **项目名称 (CN)** | 全植入式脑机接口系统中的脑电信号采集与压缩技术研究综述 |
| **项目名称 (EN)** | A Survey on EEG Signal Acquisition and Information Compression for Fully Implantable Brain-Computer Interface Systems |
| **研究范式** | 系统综述 (Systematic Review) / 可复现文献处理流程 |
| **研究重点** | 关注**低功耗、小体积、高压缩比**的硬件电路与前端信号处理算法 |
| **已实际检索数据库** | Web of Science (WoS) |
| **计划扩展数据库** | IEEE Xplore, PubMed, Scopus |

---

## 二、 检索参数 (Search Parameters)

### 2.1 总体检索逻辑
**检索表达式**：`方法词 (Method)` **AND** `任务词 (Task)` **AND** `限制词 (Context/Constraint)` **NOT** `排除词 (Exclusion)`

---

### 2.2 方法词参数 (Method Terms)
> **策略说明**：侧重底层硬件架构与高效信号处理逻辑。

*   **中文术语**：
    *   `集成电路` / `专用集成电路 (ASIC)` / `FPGA`
    *   `模拟前端 (AFE)` / `逐次逼近寄存器 (SAR) ADC`
    *   `压缩感知 (CS)` / `特征提取` / `尖峰检测 (Spike Sorting)`
*   **英文术语**：
    *   `Integrated Circuit` / `ASIC` / `FPGA` / `On-chip`
    *   `Analog Front-End (AFE)` / `SAR ADC` / `Chopper-stabilized`
    *   `Compressive Sensing` / `Data Compression` / `Feature Extraction`

---

### 2.3 任务词参数 (Task Terms)
> **策略说明**：限定于脑电信号 (EEG/Neural) 的获取与处理任务。

*   **中文术语**：
    *   `脑电采集` / `信号采集` / `神经信号处理`
    *   `信息压缩` / `数据压缩` / `低带宽传输`
*   **英文术语**：
    *   `EEG Acquisition` / `Neural Recording` / `Signal Processing`
    *   `Information Compression` / `Data Reduction` / `Bandwidth Constraints`

---

### 2.4 限制词与场景词 (Context/Constraint Terms)
> **策略说明**：体现全植入式系统的严苛环境要求。

*   **中文术语**：
    *   `全植入式` / `植入式` / `低功耗` / `超低功耗`
*   **英文术语**：
    *   `Fully Implantable` / `Implantable BCI` / `Low-power` / `Ultra-low-power (ULP)`
    *   `Energy-efficient` / `Resource-constrained`

---

### 2.5 排除词参数 (Exclusion Terms)
> **策略说明**：剔除非硬件相关的纯算法研究及干扰领域。

*   **排除项**：
    *   `深度学习 (Deep Learning)` / `CNN` / `Transformer`（此类算法通常功耗过高，不符合全植入前端要求）
    *   `交通流` / `网络流量` / `桥梁荷载`
    *   `非人实验` / `动物 (Animal/Rat/Monkey)`（仅当其电路架构无通用参考价值时排除）

---

## 三、 筛选与分析准则 (Screening Criteria)

### 3.1 纳入标准 (Inclusion)
1.  **硬件实现**：讨论了具体的电路拓扑（如 ADC 架构、放大器设计）。
2.  **能效比**：给出了明确的功耗数值（$\mu W$ 或 $mW$）。
3.  **压缩指标**：讨论了压缩比 (CR) 及其对信号保真度（信息完整性）的影响。

### 3.2 排除标准 (Exclusion)
1.  **离线算法**：仅在 PC 端运行的复杂深度学习模型，未考虑硬件部署可行性。
2.  **侵入性不符**：纯非植入式（如消费级便携 EEG 头戴设备），且不涉及低功耗架构改进。

---
