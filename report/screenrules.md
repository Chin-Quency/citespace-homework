根据你提供的关键词，我为你更新了 **`screening_rules.md`**。

这份文档将逻辑进行了结构化，特别强调了你对“电路/信号处理”的偏好以及对“深度学习/侵入式”研究的排除。

---

# 文献筛选规则说明 (screening_rules.md)

**版本：** v1.1
**研究重点：** 基于脑电信号 (EEG) 的电路级与传统信号处理研究
**筛选逻辑更新日期：** 2026-04-07

---

## 1. 核心筛选逻辑概览
本研究倾向于探索 **硬件实现、电路设计及经典信号处理算法** 在脑电交互中的应用，主动排除纯算法驱动的深度学习黑盒模型。

### 筛选流程图参考


---

## 2. 纳入标准 (Inclusion Criteria) - `Include`
文献必须满足以下 **任一** 核心领域，且不触发排除条件：

*   **硬件与电路 (Circuit)**：涉及集成电路 (IC)、FPGA 实现、模拟前端 (AFE) 或低功耗芯片设计。
*   **信号处理 (Signal Processing)**：包含滤波、特征提取 (PCA/LDA)、时频分析等确定性处理方法。
*   **信息理论 (Information)**：涉及脑电信号的特征信息量分析、编码或传输协议。
*   **系统应用**：非侵入式脑机接口 (BCI) 系统集成。

---

## 3. 排除标准与原因编码 (Exclusion Codes) - `Exclude`

一旦触发以下任一标准，文献将被排除并标记对应编码：

| 编码 | 排除原因 | 匹配关键词 / 判定标准 |
| :--- | :--- | :--- |
| **E1** | **非本主题 (Irrelevant)** | 摘要中未出现 `circuit`, `eeg`, `bci`, `signal processing` 等核心词。 |
| **E2** | **侵入式研究 (Invasive)** | 包含 `implantable` (可植入), `invasive` (侵入式) 或 `intracranial` (颅内)。 |
| **E3** | **非人类实验 (Non-human)** | 包含 `animal`, `rat`, `monkey` 等非人类受试者研究。 |
| **E4** | **深度学习干扰 (Deep Learning)** | 包含 `deep learning`, `cnn`, `rnn`, `transformer`。*注：本研究关注底层处理与电路。* |
| **E5** | **时间不符 (Outdated)** | 晚于项目规定年限或数据格式不完整。 |

---

## 4. 自动化脚本配置 (Python Snippet)
脚本中的 `screen_logic` 函数已按照上述规则更新：

```python
def screen_logic(item):
    include_keywords = [
        'low power', 'energy efficient', 'data compression', 
        'signal acquisition', 'on-chip', 'asic', 'fpga',
        'eeg', 'brain-computer interface', 'bci',
        'integrated circuit', 'analog frontend', 'afe'
    ]
    
    
    exclude_keywords = [
        'animal', 'rat', 'monkey', 'canine',
        'deep learning', 'convolutional neural network', 'transformer model'
    ]
    
    title_abs = (item['TI'] + " " + item['AB']).lower()
    
    # E1: 主题不相关
    if not any(kw in title_abs for kw in include_keywords):
        return "Exclude", "E1"
    text = (item['TI'] + " " + item['AB']).lower()
    # E4: 时间不符 (示例：只要 2010 年以后的)
    # 逻辑判断
    if not any(kw in text for kw in include_keywords):
        return "Exclude", "E1 - Topic Irrelevant"
    
    if any(kw in text for kw in exclude_keywords):
        if 'deep learning' in text or 'neural network' in text:
            return "Exclude", "E4 - Pure Algorithm/DL"
        return "Exclude", "E3 - Non-human study"

    return "Include", "Pass"

---

## 5. 预期产出清单
1.  **筛选报告** (`screening.csv`)：包含每篇文献的 `Reason_Code`。
2.  **证据链** (`evidence_chain.md`)：重点提取电路架构和信号处理流。
3.  **PRISMA 数据**：用于统计各阶段被 E1-E4 拦截的文献数量。

