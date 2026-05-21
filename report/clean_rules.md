\# 植入式脑电信号数据清洗与字段统一规范 (clean\_rules.md)



本文件规范了项目在“全植入式”场景下，针对\*\*硬件采集原始数据\*\*与\*\*片上压缩重构数据\*\*的清洗、对齐与去重标准。



\## 一、 总原则 (General Principles)

1\.  \*\*分类清洗，统一映射\*\*：硬件原始采集数据（如 ASIC 导出的 ECoG）与算法处理结果数据（压缩后数据）格式差异巨大，必须先分别清洗，最后再基于唯一标识符合并。

2\.  \*\*核心字段零容忍\*\*：采样率、位宽、信号类型缺失的记录直接标记无效；严禁对缺失参数进行“均值填充”或“默认补全”。

3\.  \*\*源文件不可变\*\*：所有清洗操作必须输出至新文件，严禁覆盖 `data/raw/` 目录下的任何原始设备日志或算法输出表。



\## 二、 字段标准化映射表 (Field Standardization)



\### 2.1 硬件采集端数据 (Raw Acquisition)

| 原始可能字段 | 标准化字段名 (统一小写) | 数据规范要求 |

| :--- | :--- | :--- |

| DeviceID / 芯片编号 | `device\_id` | 保持不变 |

| SignalType / 模态 | `signal\_type` | 统一大写：ECoG, LFP, MUA, SUA |

| SamplingRate | `sampling\_rate` | 统一单位：Hz (纯数字，勿带单位字符) |

| BitWidth / 精度 | `bit\_width` | 统一单位：bit (如 12, 16) |

| CollectSite | `collect\_site` | 统一规范词：颅内 (Intracranial), 皮层 (Cortical) |

| NoiseLevel | `noise\_level` | 统一单位：dB |



\### 2.2 算法压缩端数据 (Processed/Compressed)

| 原始可能字段 | 标准化字段名 (统一小写) | 数据规范要求 |

| :--- | :--- | :--- |

| SourceDataID | `source\_data\_id` | \*\*极重要\*\*：必须与采集端的 data\_id 绝对对应 |

| Algorithm / 算法 | `algorithm` | 统一大写简写：CS, DWT, DPCM, PCA |

| CompressionRatio | `compression\_ratio` | 统一转换为小数浮点数 (如 8.5)，不得保留 "8.5:1" |

| PowerConsumption | `power\_consumption` | 统一换算为微瓦 (uW) 纯数值 |

| Delay / 延迟 | `delay` | 统一单位：ms |

| SNR / 恢复信噪比 | `snr` | 统一单位：dB |



\## 三、 有效性校验与去重 (Validation \& Deduplication)



\### 3.1 质量初筛门限 (Quality Thresholds)

数据需满足以下最低硬件设计与验证指标，方可进入 `processed` 分析集：

\* \*\*硬件信号\*\*：`noise\_level` ≤ 30dB，采样率位于 1kHz - 32kHz 区间。

\* \*\*压缩性能\*\*：`compression\_ratio` ≥ 2.0，重构信号 `snr` ≥ 15dB，系统处理 `delay` ≤ 20ms。



\### 3.2 严格去重逻辑 (Deduplication Rules)

1\.  \*\*全局唯一冲突\*\*：`data\_id` 完全一致，强制覆盖/剔除。

2\.  \*\*采集端重复\*\*：`device\_id` + `collect\_time` + `channel` 完全一致，保留 `noise\_level` 更低的记录。

3\.  \*\*处理端重复\*\*：针对同一 `source\_data\_id` 运行了相同 `algorithm` 的多次记录，保留 `snr` 最高或 `power\_consumption` 最低的记录。



\## 四、 目录结构与版本控制 (Directory Structure)

所有数据必须严格遵守以下文件流转生命周期：

\* 📂 `data/raw/`：存放原始设备导出日志 (如 `.dat`, `.csv`)。\*\*\[只读]\*\*

\* 📂 `data/interim/`：存放完成格式标准化但未合并的中间表。

\* 📂 `data/processed/`：存放最终字段对齐、通过质量门限的综合验证数据集。

\* 📂 `reports/`：存放本规则说明文档 (`clean\_rules.md`) 及数据质量统计报告 (`data\_quality.md`)。

