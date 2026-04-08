# 全植入式脑电信号与信息压缩系统研究内容与核心目标

\## 一、研究内容分析

本项目旨在**系统呈现全植入式情景下的脑电信号与信息压缩系统设计**，通过对相关技术框架与方法的调研，完成以下核心内容研究：

1. 调研脑电信号采集电路基本框架，明晰脑电信号采集的基本原理与经典电路架构；
2. 调研基于脑电信号特征的信息压缩技术，梳理压缩算法与信号特征的适配逻辑。

\## 二、核心研究目标

基于 Web of Science 数据库中**全植入式情景下脑电信号与信息压缩系统**相关文献数据，围绕其在医学领域的应用开展系统性文献计量分析，重点回答以下核心问题：

1. **发文趋势与阶段特征**
分析 2020–2025 年间，基于脑机接口（BCI）与信号处理采集电路相关研究的发文年度趋势，总结各阶段发展特征与演进规律。
2. **全植入场景瓶颈与解决方案**
剖析全植入场景下脑电信号采样存在的固有局限，归纳该场景下信号采集、传输与压缩环节的技术破局路径。
3. **研究热点识别与演化**
通过关键词共现分析与关键词演化分析，识别领域核心研究热点，揭示热点变迁趋势与研究重心转移规律。
4. **高被引文献与技术演进**
梳理代表性高被引文献及其关键研究成果，总结全植入式脑电信号处理与信息压缩的技术发展路径、方法演进脉络。
5. **现存问题与未来方向**
基于文献证据链，提炼当前研究存在的主要问题与不足，科学研判并总结领域未来可能的发展方向。

\## 三、配置文件
config/query.yaml
query:
object:

* "bci interface"
* "circuit"
* "signal acquisition"
method:
* "signal processing"
* "digital signal processing"
time\_window: \[2020, 2025]

\## 四、布尔检索式

Refine results for "brain computer interface" (Topic) AND "signal processing" OR "digital signal processing" OR "signal acquisition" (Title) AND 2020-01-01/2026-01-01 (Publication Date) and System Information Circuit (OR – Search within topic) and Signal Processing (OR – Search within topic) and Signal Acquisition (OR – Search within topic) and Brain-computer Interface Bci (OR – Search within topic) and Brain-computer Interface (OR – Search within topic) and Digital Signal Processing (OR – Search within topic) and Circuit (OR – Search within topic)
## 项目结构
项目采用模块化结构设计，将数据、代码与文档分离，提升可维护性与可复现性：
data/：存放原始数据及筛选结果（CSV）
src/：存放筛选与数据处理脚本（如 stage1、stage2）
reports/：存放方法文档与分析报告
outputs/：存放图像结果（如 PRISMA 流程图）
config/：配置文件（如 query.yaml）
README.md：项目整体说明



