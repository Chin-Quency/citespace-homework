\# 🧠 全植入式脑电信号与信息压缩系统：文献计量与系统化分析



> \*\*项目简介\*\*

> 本项目旨在系统呈现全植入式情景下的脑电信号与信息压缩系统设计。通过对 Web of Science 数据库中相关文献的深度挖掘与文献计量分析，明晰脑电信号采集的基本原理与经典电路架构，梳理压缩算法与信号特征的适配逻辑，为全植入式脑机接口（BCI）的未来发展提供理论支撑与技术演进脉络。



\---



\## 🎯 一、 研究内容与核心目标



本项目重点围绕“医学领域的全植入应用”开展研究，旨在回答以下五个核心问题：



1\. \*\*发文趋势与阶段特征\*\*：分析 2020–2025 年间 BCI 与信号采集电路相关研究的年度发文趋势，总结各阶段演进规律。

2\. \*\*场景瓶颈与解决方案\*\*：剖析全植入场景下信号采样存在的固有局限，归纳采集、传输与压缩环节的技术破局路径。

3\. \*\*研究热点识别与演化\*\*：通过关键词共现与演化分析，识别领域核心热点及研究重心的转移规律。

4\. \*\*高被引文献与技术演进\*\*：梳理代表性高被引文献，总结全植入式信号处理与信息压缩的技术发展脉络。

5\. \*\*现存问题与未来方向\*\*：基于文献证据链，提炼当前研究的痛点，研判未来的科学发展方向。



\---



\## 📊 二、 PRISMA 文献筛选流程



本项目严格遵循 PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) 标准进行文献筛选，确保数据来源的透明性与可重复性。



\*图片命名为 `prisma\_flowchart.png` 并放置于 `outputs/` 目录下)\*



\*\*筛选阶段说明：\*\*



1. 识别 (Identification)通过 Web of Science 数据库检索获得初始记录：$n = 16,000$ 篇。2. 初筛 (Screening)进入自动化脚本初筛的记录：$n = 16,000$ 篇。因不符合纳入标准被排除的记录总数：$n = 4,797$ 篇。排除原因 1 (E1: 主题不符/缺乏硬件及压缩要素)：$n = 2,294$ 篇。排除原因 2 (E3: 纯动物实验)：$n = 14$ 篇。排除原因 3 (E4: 纯深度学习/高功耗算法)：$n = 2,489$ 篇。3. 纳入 (Included)最终纳入用于 CiteSpace / VOSviewer 文献计量学分析的文献总量：$n = 11,203$ 篇。

\## 🔍 三、 检索策略与配置



\### 3.1 配置文件 (`config/query.yaml`)



项目的基础检索配置参数如下：

query:

&#x20; object:

&#x20;   # 对应检索式中的植入式系统与神经信号模态

&#x20;   - "implant\*"

&#x20;   - "invasive"

&#x20;   - "neural interfac\*"

&#x20;   - "neural record\*"

&#x20;   - "ECoG"

&#x20;   - "LFP"

&#x20;   - "EEG"

&#x20; method:

&#x20;   # 对应检索式中的片上数据处理与压缩技术

&#x20;   - "compress\*"

&#x20;   - "data reduc\*"

&#x20;   - "compressive sensing"

&#x20;   - "feature extract\*"

&#x20;   - "on-chip process\*"

&#x20;   - "edge comput\*"

&#x20; context:

&#x20;   # 对应检索式中的人类/临床研究限制条件

&#x20;   - "human\*"

&#x20;   - "patient\*"

&#x20;   - "clinical"

&#x20;   - "subject\*"

&#x20; exclusion:

&#x20;   # 对应检索式中 NOT 排除的动物实验与非相关模型

&#x20;   - "rat"

&#x20;   - "rats"

&#x20;   - "mouse"

&#x20;   - "mice"

&#x20;   - "rodent\*"

&#x20;   - "macaque\*"

&#x20;   - "monkey\*"

&#x20;   - "primate\*"

&#x20;   - "animal model\*"

&#x20;   - "feline"

&#x20;   - "canine"

&#x20;   - "pig"

&#x20;   - "porcine"

&#x20; time\_window: \[2010, 2025]

\### 3.2 高级布尔检索式 (WoS)



为了精准定位“全植入、人类研究、硬件/压缩处理”并排除干扰项，采用如下检索表达式：



```text

(TS=(implant\* OR invasive OR "neural interfac\*" OR "neural record\*" OR ECoG OR LFP OR EEG) 

AND TS=(compress\* OR "data reduc\*" OR "compressive sensing" OR "feature extract\*" OR "on-chip process\*" OR "edge comput\*") 

AND TS=(human\* OR patient\* OR clinical OR subject\*) 

AND PY=(2010-2026)) 

NOT TS=(rat OR rats OR mouse OR mice OR rodent\* OR macaque\* OR monkey\* OR primate\* OR "animal model\*" OR feline OR canine OR pig OR porcine)



```
\## 四、共被引分析
\### 最高被引文献统计：
Koelstra S, 2012, IEEE T AFFECT COMPUT, V3, P18, DOI 10.1109/T-AFFC.2011.15          183
Wolpaw JR, 2002, CLIN NEUROPHYSIOL, V113, P767, DOI 10.1016/S1388-2457(02)00057-3    174
Delorme A, 2004, J NEUROSCI METH, V134, P9, DOI 10.1016/j.jneumeth.2003.10.009       164
Ramoser H, 2000, IEEE T REHABIL ENG, V8, P441, DOI 10.1109/86.895946                 158
Goldberger AL, 2000, CIRCULATION, V101, pE215, DOI 10.1161/01.CIR.101.23.e215        155





\---



\## 📂 五、 项目目录结构



项目采用模块化结构设计，实现数据、代码与文档的彻底解耦，提升项目的可维护性与可复现性。



```text

📦 Citespace-homework

&#x20;┣ 📂 data/          # 存放原始数据及各阶段筛选结果（CSV/TXT）

&#x20;┣ 📂 src/           # 存放筛选逻辑与数据处理脚本 (如 stage1\_clean.py, stage2\_analyze.py)

&#x20;┣ 📂 reports/       # 存放方法文档、过程记录与最终分析报告

&#x20;┣ 📂 outputs/       # 存放生成的图像结果（如 PRISMA 流程图、图谱可视化）

&#x20;┣ 📂 config/        # 存放配置文件（如 query.yaml）

&#x20;┗ 📜 README.md      # 项目整体说明文档



```



\---



\## 👥 六、 团队成员与分工



本项目由跨学科团队协作完成，具体分工如下：



| 姓名 | 负责角色 | 核心工作内容 |

| --- | --- | --- |

| \*\*\[姓名 A]\*\* | 项目负责人 (PI) | 统筹项目进度，定义检索策略，撰写与把控最终综述报告。 |

| \*\*\[姓名 B]\*\* | 数据工程师 | 负责 WoS 数据导出，编写 `src/` 下的自动化清洗与去重脚本。 |

| \*\*\[姓名 C]\*\* | 文献分析师 | 执行 PRISMA 复筛阶段，负责 CiteSpace/VOSviewer 图谱绘制与热点分析。 |

| \*\*\[姓名 D]\*\* | 硬件/算法专家 | 深度提炼高被引文献中的电路架构与压缩算法机制，构建证据链。 |

