# 项目参数说明 (Project Parameters)

## 一、项目基础参数

### 1.1 路径配置
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `SRC_DIR` | `src/` | 源代码目录 |
| `DATA_DIR` | `data/` | 原始数据目录 |
| `OUTPUT_DIR` | `outputs/` | 输出结果目录 |
| `REPORT_DIR` | `report/` | 报告文档目录 |

### 1.2 文件编码
| 参数 | 值 | 说明 |
|------|-----|------|
| `INPUT_ENCODING` | `utf-8` | 输入文件编码 |
| `OUTPUT_ENCODING` | `utf-8-sig` | 输出 CSV 编码 (兼容 Excel) |

---

## 二、检索参数

### 2.1 Web of Science 检索配置
| 参数 | 说明 |
|------|------|
| `database` | Web of Science Core Collection |
| `export_format` | Full Record and Cited References |
| `record_count` | 默认 16,000 (需根据实际检索结果调整) |

### 2.2 检索结果文件格式
- 文件名格式：`download_*.txt`
- 每条记录以 `ER` 结尾分隔
- 文件头包含 `FN Clarivate Analytics Web of Science`

---

## 三、字段参数

### 3.1 Web of Science 核心字段映射

| 字段代码 | 字段名称 | 说明 | 是否必填 |
|----------|----------|------|----------|
| `TI` | Title | 文献标题 | 是 |
| `AB` | Abstract | 摘要 | 否 |
| `DE` | Keywords | 关键词 | 否 |
| `AU` | Author | 作者 | 否 |
| `PY` | Publication Year | 出版年份 | 否 |
| `SO` | Source | 来源出版物/期刊 | 否 |
| `DI` | DOI | 数字对象标识符 | 去重用 |
| `CR` | Cited References | 参考文献列表 | 引用分析用 |

### 3.2 证据链提取字段
| 字段代码 | 字段名称 | 说明 |
|----------|----------|------|
| `Method` | 技术方法 | 压缩算法、电路架构等 |
| `Data` | 信号类型 | ECoG, LFP, MUA, SUA 等 |
| `Application` | 应用场景 | 癫痫检测、运动解码等 |
| `Performance` | 性能指标 | 功耗、压缩比、工艺节点等 |
| `Title` | 标题 | 文献标题 |
| `Year` | 年份 | 出版年份 |
| `Journal` | 期刊 | 来源期刊 |

---

## 四、数据源参数

### 4.1 数据源路径配置
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `screening_csv` | `../outputs/screening_results.csv` | 筛选结果 CSV 路径 |
| `citation_csv` | `../data/merged_with_citations.csv` | 引用关系 CSV 路径 |
| `citespace_txt` | `../outputs/download_included_for_citespace.txt` | CiteSpace 专用 TXT 路径 |
| `evidence_csv` | `../outputs/evidence_raw_data.csv` | 证据链数据 CSV 路径 |

### 4.2 批量数据读取
```python
data_folder = "../data"  # 批量读取整个文件夹
```

---

## 五、目录参数

### 5.1 项目目录结构
```
citespace-homework/
├── src/                    # 源代码目录
│   ├── filter.py          # 文献筛选脚本
│   ├── citespace.py       # 数据清洗脚本
│   ├── extract_citations.py # 引用提取脚本
│   ├── co_citation.py     # 共被引分析脚本
│   ├── evidence_chain.py  # 证据链提取脚本
│   ├── evidence_analyze.py # 证据统计分析脚本
│   └── draw_prisma.py     # PRISMA 流程图绘制脚本
├── data/                   # 数据目录
│   ├── savedrecs.txt      # 原始 WOS 导出文件
│   └── merged_with_citations.csv  # 引用关系表
├── outputs/                # 输出目录
│   ├── screening_results.csv       # 筛选结果
│   ├── download_included_for_citespace.txt  # CiteSpace 输入
│   ├── field_stats.csv           # 字段统计
│   ├── co_citation_network/      # 共被引网络输出
│   │   ├── citation_matrix_R.csv
│   │   ├── co_citation_matrix_C.csv
│   │   ├── similarity_matrix.csv
│   │   └── co_citation_edges.csv
│   └── evidence_raw_data.csv     # 证据链数据
└── report/                 # 报告目录
    ├── screenrules.md     # 筛选规则
    ├── clean_rules.md     # 清洗规则
    └── params.md          # 参数说明
```

---

## 六、筛选参数

### 6.1 概念关键词参数

#### 概念 1 - BCI/神经接口关键词
```python
c1_keywords = [
    'implant',           # 植入式
    'invasive',          # 侵入式
    'neural interfac',   # 神经接口
    'neural record',     # 神经记录
    'ecog',              # 皮层脑电
    'lfp',               # 局部场电位
    'eeg'                # 脑电
]
```

#### 概念 2 - 数据压缩/边缘计算关键词
```python
c2_keywords = [
    'compress',              # 压缩
    'data reduc',            # 数据减少
    'compressive sensing',   # 压缩感知
    'feature extract',       # 特征提取
    'on-chip process',       # 片上处理
    'edge comput'            # 边缘计算
]
```

### 6.2 排除关键词参数

#### E4 - 深度学习关键词 (纯算法排除)
```python
dl_keywords = [
    'deep learning',
    'convolutional neural network',
    'transformer model',
    'neural network'
]
```

#### E3 - 动物实验关键词
```python
animal_pattern = r'\b(rat|rats|mouse|mice|rodent|rodents|macaque|macaques|monkey|monkeys|primate|primates|animal|animals|feline|canine|pig|pigs|porcine)\b'
human_pattern = r'\b(human|humans|patient|patients|clinical|subject|subjects)\b'
```

#### E5 - 非神经医学噪音关键词
```python
med_noise_pattern = r'\b(bone|bones|spine|spinal|vertebroplasty|orthopedic|orthopaedic|fracture|fractures|fixation|lumbar|cervical|dental|stent|stents|arthroplasty|osteoporosis|joint|cardiovascular|myocardial)\b'
```

### 6.3 筛选阈值参数
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `min_similarity` | `0.1` | 共被引相似度阈值 (建边) |
| `co_citation_threshold` | `3` | 共被引频次最小阈值 (过滤低频文献) |

### 6.4 筛选统计参数
| 统计项 | 变量名 |
|--------|--------|
| 初始记录总数 | `stats["Total"]` |
| E1 排除数量 | `stats["Excluded_E1"]` |
| E3 排除数量 | `stats["Excluded_E3"]` |
| E4 排除数量 | `stats["Excluded_E4"]` |
| E5 排除数量 | `stats["Excluded_E5"]` |
| 最终纳入数量 | `stats["Included"]` |

---

## 七、可视化参数

### 7.1 PRISMA 流程图参数 (基于 draw_prisma.py)

#### 画布配置
| 参数 | 值 | 说明 |
|------|-----|------|
| `figsize` | `(10, 8)` | 画布尺寸 (英寸) |
| `dpi` | `300` | 输出分辨率 |

#### 文本框样式
| 参数 | 值 | 说明 |
|------|-----|------|
| `box_style` | `{"boxstyle": "round,pad=0.5", "facecolor": "#F5F5F5", "edgecolor": "#333333", "linewidth": 1.5}` | 通用文本框样式 |
| `exclude_box_style` | `{"facecolor": "#FFF0F0", "edgecolor": "#D62728"}` | 排除框样式 (红色边框) |
| `include_box_style` | `{"facecolor": "#F0FFF0", "edgecolor": "#2CA02C"}` | 纳入框样式 (绿色边框) |

#### 节点位置参数
| 节点 | X 坐标 | Y 坐标 | 说明 |
|------|-------|-------|------|
| `pos_id` | `0.35` | `0.85` | Identification (标识) |
| `pos_screen` | `0.35` | `0.55` | Screening (筛选) |
| `pos_exclude` | `0.80` | `0.55` | Excluded (排除) |
| `pos_include` | `0.35` | `0.25` | Included (纳入) |

#### 箭头样式参数
| 参数 | 值 | 说明 |
|------|-----|------|
| `facecolor` | `'black'` | 箭头填充色 |
| `edgecolor` | `'black'` | 箭头边框色 |
| `width` | `2` | 箭头宽度 |
| `headwidth` | `8` | 箭头头部宽度 |
| `headlength` | `10` | 箭头头部长度 |
| `shrink` | `0.05` | 箭头收缩比例 |

#### 区域标签参数
| 参数 | 值 | 说明 |
|------|-----|------|
| `fontsize` | `14` | 区域标签字号 |
| `fontweight` | `'bold'` | 区域标签粗体 |
| `rotation` | `90` | 区域标签旋转角度 |
| `color` | `'gray'` | 区域标签颜色 |

#### 分隔线参数
| 参数 | 值 | 说明 |
|------|-----|------|
| `linestyle` | `'--'` | 虚线样式 |
| `color` | `'lightgray'` | 分隔线颜色 |
| `zorder` | `0` | 分层顺序 |

### 7.2 数据质量统计图参数
| 参数 | 值 | 说明 |
|------|-----|------|
| `plot_type` | `'bar'` | 柱状图 |
| `title` | `'Missing Rate per Field'` | 图表标题 |
| `tight_layout` | `True` | 自动调整布局 |

### 7.3 作者合作网络图参数 (`report/author_collaboration/author_collaboration.jpg`)

> 基于 CiteSpace 生成的作者合作网络图谱，聚焦领域科研协作格局。

#### CiteSpace 运行参数
| 参数 | 值 | 说明 |
|------|-----|------|
| `time_slicing` | `2010-2026` | 时间切片范围 |
| `years_per_slice` | `1` | 每个时间切片长度 (年) |
| `term_source` | `Title / Abstract / Author Keywords / Keywords Plus` | 术语来源 |
| `term_type` | `None` | 术语类型 (未启用突发检测) |
| `node_type` | `Author` | 节点类型：作者 |
| `selection_criteria` | `g-index (k=25)` | 节点筛选标准 |
| `pruning` | `Pathfinder` | 网络裁剪算法 |
| `pruning_merged_network` | `True` | 对合并网络裁剪 |
| `visualization` | `Cluster View (Static)` | 可视化视图 |

#### 节点指标参数
| 指标 | 说明 | 图谱标注方式 |
|------|------|-------------|
| `Citation` | 被引次数 | 节点大小 / 标注 |
| `Burst` | 突现强度 | 红色光圈 |
| `Centrality` | 中介中心性 | 紫色外圈 |
| `Sigma` | Burst × Centrality | 综合里程碑指标 |

#### 图谱输出文件
| 文件 | 路径 |
|------|------|
| 网络图 | `report/author_collaboration/author_collaboration.jpg` |
| 分析文本 | `report/author_collaboration/author_collaboration.txt` |

### 7.4 关键词聚类图参数 (`report/co_citation_network/b60691c83e608745fb4624c463eebac8.png`)

> 基于 CiteSpace 生成的关键词共现聚类图谱，揭示领域知识基础。

#### CiteSpace 运行参数
| 参数 | 值 | 说明 |
|------|-----|------|
| `time_slicing` | `2010-2026` | 时间切片范围 |
| `years_per_slice` | `1` | 每个时间切片长度 (年) |
| `term_source` | `Title / Abstract / Author Keywords / Keywords Plus` | 术语来源 |
| `term_type` | `None` | 术语类型 |
| `node_type` | `Keyword` | 节点类型：关键词 |
| `selection_criteria` | `g-index (k=25)` | 节点筛选标准 |
| `pruning` | `Pathfinder` | 网络裁剪算法 |
| `pruning_merged_network` | `True` | 对合并网络裁剪 |
| `visualization` | `Cluster View (Static)` | 可视化视图 |

#### 聚类结果参数
| 聚类编号 | 聚类标签 | 说明 |
|----------|----------|------|
| `#0` | 三叉神经痛 | 临床诊断方向 |
| `#1` | 机器学习 | BCI 核心应用 |
| `#2` | 运动想象 | BCI 核心应用 |
| `#3` | 脑建模 | 信号建模方向 |
| `#4` | 阿尔茨海默症 | 临床疾病场景 |
| `#5` | 急性深静脉血栓 | 临床疾病场景 |

#### 节点指标参数
| 指标 | Top 1 | Top 2 | Top 3 |
|------|-------|-------|-------|
| `Citation` (被引次数) | eeg (304) | 机器学习 (279) | 诊断 (214) |
| `Degree` (度中心性) | electroencephalogram (55) | eeg (51) | 诊断 (47) |
| `Centrality` (中介中心性) | 诊断 (0.25) | 大脑 (0.12) | 疾病 (0.10) |

#### 图谱输出文件
| 文件 | 路径 |
|------|------|
| 聚类图 | `report/co_citation_network/b60691c83e608745fb4624c463eebac8.png` |
| 分析文本 | `report/co_citation_network/co_citation_network.txt` |

### 7.5 关键词时间线图谱参数 (`report/timeline/timeline.png`)

> 基于 CiteSpace 生成的时间线视图，展示研究热点随时间的演化脉络。

#### CiteSpace 运行参数
| 参数 | 值 | 说明 |
|------|-----|------|
| `time_slicing` | `2010-2026` | 时间切片范围 |
| `years_per_slice` | `1` | 每个时间切片长度 (年) |
| `term_source` | `Title / Abstract / Author Keywords / Keywords Plus` | 术语来源 |
| `term_type` | `None` | 术语类型 |
| `node_type` | `Keyword` | 节点类型：关键词 |
| `selection_criteria` | `g-index (k=25)` | 节点筛选标准 |
| `pruning` | `Pathfinder` | 网络裁剪算法 |
| `pruning_merged_network` | `True` | 对合并网络裁剪 |
| `visualization` | `Timeline View` | 可视化视图：时间线 |

#### 时间线聚类参数
| 聚类编号 | 聚类标签 | 活跃时段 | 阶段特征 |
|----------|----------|----------|----------|
| `#0` | 三叉神经痛 | 2010-2015 | 早期：临床诊断方向 |
| `#1` | 机器学习 | 2015-2020 | 中期：BCI 核心应用 |
| `#2` | 脑建模 | 2015-2020 | 中期：信号建模方向 |
| `#3` | 运动想象 | 2015-2020 | 中期：BCI 核心应用 |
| `#4` | 力学特性 | 2020-2026 | 近期：具体疾病场景 |
| `#5` | 阿尔茨海默病 | 2020-2026 | 近期：临床落地深化 |
| `#6` | 急性深静脉血栓 | 2020-2026 | 近期：临床落地深化 |

#### 关键技术演化线索
| 技术线 | 演化关键词 | 阶段 |
|--------|-----------|------|
| 信号采集 | EEG → BCI | 贯穿始终 |
| 信号处理 | 小波变换 → 特征选择 → 离散小波变换 | 中期 |
| 压缩技术 | 压缩感知 → 熵 → 压缩感知(深化) | 中期→近期 |
| 智能分析 | 机器学习 → 迁移学习 | 近期 |

#### 图谱输出文件
| 文件 | 路径 |
|------|------|
| 时间线图 | `report/timeline/timeline.png` |
| 分析文本 | `report/timeline/timeline.txt` |

### 7.6 证据链统计图参数 (`report/Figure_1.png`)

> 基于 `evidence_analyze.py` 生成的证据链深度统计可视化图。

#### 图表配置
| 参数 | 值 | 说明 |
|------|-----|------|
| `数据源` | `outputs/evidence_raw_data.csv` | 证据链数据 CSV |
| `统计模块` | 6 项 | 核心电路架构 / 信号模态 / 功耗 / 压缩比 / 工艺制程 / 应用场景 |

#### 各子图参数
| 子图编号 | 统计内容 | 图表类型 | 关键参数 |
|----------|----------|----------|----------|
| 1 | 核心电路架构与算法热点 (Top 8) | 频次柱状图 | `top_n = 8` |
| 2 | 侵入式神经信号模态 | 百分比柱状图 | 按占比排序 |
| 3 | 系统功耗水平 | 统计摘要 | 单位: uW, 极低功耗阈值: `<10uW` |
| 4 | 片上数据压缩性能 | 统计摘要 | 单位: `:1`, 超高压缩阈值: `≥10倍` |
| 5 | CMOS 制造工艺制程 | 频次分布 | 单位: nm, `top_n = 5` |
| 6 | 终端临床应用场景 | 频次/百分比 | 按文献数排序 |

#### 功耗提取参数
| 参数 | 正则模式 | 单位换算 |
|------|----------|----------|
| 功耗提取 | `(?:功耗:)?([\d\.]+)\s*([µuumnp])w` | mW×1000, µW×1, nW÷1000, pW÷1000000 → uW |

#### 压缩比提取参数
| 参数 | 正则模式 | 说明 |
|------|----------|------|
| 压缩率(CR) | `压缩率\(CR\):(\d+\.?\d*)` | 从结构化字段提取 |
| 比率格式 | `(\d+\.?\d*)\s*:\s*1` | 匹配 8:1 格式 |
| 倍数格式 | `(\d+\.?\d*)\s*(?:x\|fold)` | 匹配 10x 格式 |

#### 工艺节点提取参数
| 参数 | 正则模式 | 单位换算 |
|------|----------|----------|
| nm 格式 | `(?:工艺:)?(\d{2,3})\s*(?:nm)` | 直接取值 |
| um 格式 | `(?:工艺:)?(0\.\d+)\s*(?:um\|µm)` | ×1000 → nm |

---

## 八、算法参数

### 8.1 共被引分析参数
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `min_weight` | `0.1` | 最小相似度权重阈值 |
| `THRESHOLD` | `3` | 被引频次最小阈值 |

### 8.2 证据链提取参数
| 参数 | 说明 |
|------|------|
| `method_categories` | 技术方法分类字典 (压缩与特征提取、模拟前端、硬件架构) |
| `data_keywords` | 信号类型关键词列表 |
| `application_rules` | 应用场景匹配规则 |

### 8.3 性能指标正则提取参数
| 指标 | 正则模式 | 说明 |
|------|----------|------|
| 工艺节点 | `(\d{2,3}\s*[-]?\s*(?:nm|um|µm)\s*(?:cmos)?)` | 匹配 65nm, 180nm 等 |
| 功耗 | `([\d\.]+\s*(?:[nµu]w|mw|pw))` | 匹配 1.2uW, 450nW 等 |
| 压缩比 | `(?:compression ratio|cr)[^\d]*?([\d\.]+\s*(?:x|times|:?\s*1|%))` | 匹配 16x, 15:1 等 |