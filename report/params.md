# 项目参数配置文件 (Params.md) - BCI 全植入系统专题

## 一、 项目基础信息 (Basic Information)

| 参数项 | 内容描述 |
| :--- | :--- |
| **项目名称 (CN)** | 全植入式脑机接口系统中的脑电信号采集与压缩技术研究综述 |
| **项目名称 (EN)** | A Survey on EEG Signal Acquisition and Information Compression for Fully Implantable Brain-Computer Interface Systems |
| **研究范式** | 系统综述 (Systematic Review) / 可复现文献处理流程 |
| **研究重点** | 关注**低功耗、小体积、高压缩比**的硬件电路与片上信号处理/压缩算法 |
| **主检索数据库** | Web of Science (WoS) Core Collection |
| **计划扩展库** | IEEE Xplore, PubMed, Scopus |

## 二、 检索参数 (Search Parameters)

### 2.1 总体检索逻辑
检索表达式架构：`(植入式/神经接口限定) AND (硬件电路限定) AND (信号压缩/处理限定) NOT (排除词)`

### 2.2 核心检索词库 (Keywords Dictionary)

* **维度一：植入式与信号模态 (Implantable & Modality)**
    * *CN*: 全植入式、侵入式、皮层脑电、局部场电位、神经记录
    * *EN*: Fully Implantable, Invasive, ECoG, LFP, Neural Recording, Neural Interface
* **维度二：硬件底层与电路 (Hardware & Circuit)**
    * *CN*: 模拟前端、专用集成电路、片上系统、模数转换器、低功耗
    * *EN*: Analog Front-End (AFE), ASIC, SoC, CMOS, SAR ADC, Low-power, Ultra-low-power
* **维度三：信号处理与压缩 (Processing & Compression)**
    * *CN*: 数据压缩、特征提取、压缩感知、带宽缩减
    * *EN*: Data Compression, Feature Extraction, Compressive Sensing, Bandwidth Reduction, On-chip Processing

### 2.3 排除词参数 (Exclusion Terms)
* **纯软件黑盒/高功耗算法**：Deep Learning, CNN, Transformer (不符合植入式严苛的低功耗限制)
* **非相关干扰领域**：Network Traffic, Image Compression