# 文献筛选规则 (Screening Rules)

## 一、数据来源
- Web of Science 导出格式 (纯文本 .txt)
- 每条记录以 `ER` 结尾分隔

## 二、数据字段提取
筛选过程涉及以下字段：
| 字段 | 说明 | 用途 |
|------|------|------|
| TI | Title (标题) | 用于关键词匹配 |
| AB | Abstract (摘要) | 用于关键词匹配 |
| DE | Keywords (关键词) | 用于关键词匹配 |

## 三、筛选逻辑流程图

```
开始 → 提取 TI + AB + DE (转小写)
    ↓
检查概念 1(C1) 和概念 2(C2)
    ↓ (两者都必须存在)
    ├─ 概念 1: implant, invasive, neural interfac, neural record, ecog, lfp, eeg
    └─ 概念 2: compress, data reduc, compressive sensing, feature extract, on-chip process, edge comput
    ↓
不符合 C1 AND C2? → 排除 (E1 - Topic Irrelevant)
    ↓
检查深度学习关键词 (E4)
    ├─ deep learning
    ├─ convolutional neural network
    ├─ transformer model
    └─ neural network
    ↓
存在深度学习关键词？→ 排除 (E4 - Pure Algorithm/DL)
    ↓
检查动物实验 (E3)
    ├─ 动物关键词：rat, rats, mouse, mice, rodent, rodents, macaque, macaques, monkey, monkeys, primate, primates, animal, animals, feline, canine, pig, pigs, porcine
    └─ 人类关键词：human, humans, patient, patients, clinical, subject, subjects
    ↓
有动物但无人类？→ 排除 (E3 - Pure Animal Study)
    ↓
检查非神经医学噪音 (E5)
    ├─ 骨骼相关：bone, bones, spine, spinal, vertebroplasty, orthopedic, orthopaedic, fracture, fractures, fixation, lumbar, cervical
    ├─ 牙科：dental
    ├─ 心血管：stent, stents, arthroplasty, osteoporosis, joint, cardiovascular, myocardial
    └─ 其他：spine, spinal
    ↓
存在噪音关键词？→ 排除 (E5 - Non-Neural Medical/Orthopedic Noise)
    ↓
纳入筛选 (Include - Pass)
```

## 四、详细排除规则

### E1 - Topic Irrelevant (Missing BCI or Compression)
**排除条件**: 同时缺少概念 1 和概念 2

**概念 1 (BCI/神经接口关键词)**:
```
implant, invasive, neural interfac, neural record, ecog, lfp, eeg
```

**概念 2 (数据压缩/边缘计算关键词)**:
```
compress, data reduc, compressive sensing, feature extract, on-chip process, edge comput
```

**判定逻辑**:
```
必须同时满足：has_c1 AND has_c2
否则排除 → E1
```

---

### E3 - Pure Animal Study (纯动物实验)
**排除条件**: 存在动物实验关键词 **且** 不存在人类研究关键词

**动物关键词**:
```
rat, rats, mouse, mice, rodent, rodents, macaque, macaques, monkey, monkeys, 
primate, primates, animal, animals, feline, canine, pig, pigs, porcine
```

**人类关键词**:
```
human, humans, patient, patients, clinical, subject, subjects
```

**判定逻辑**:
```
if has_animal AND (not has_human):
    排除 → E3
```

---

### E4 - Pure Algorithm/DL (纯算法/深度学习)
**排除条件**: 存在深度学习相关关键词

**深度学习关键词**:
```
deep learning, convolutional neural network, transformer model, neural network
```

**判定逻辑**:
```
if any DL keyword in text:
    排除 → E4
```

**说明**: 此规则用于排除纯算法研究，保留有实际神经接口应用背景的研究。

---

### E5 - Non-Neural Medical/Orthopedic Noise (非神经医学/骨科噪音)
**排除条件**: 存在非神经领域的医疗/骨科/外科关键词

**排除关键词**:
```
bone, bones, spine, spinal, vertebroplasty, orthopedic, orthopaedic, 
fracture, fractures, fixation, lumbar, cervical, dental, stent, stents, 
arthroplasty, osteoporosis, joint, cardiovascular, myocardial
```

**排除类别说明**:
| 类别 | 关键词示例 |
|------|-----------|
| 骨骼相关 | bone, spine, vertebroplasty, fracture, fixation, lumbar, cervical |
| 骨科手术 | orthopedic, orthopaedic, arthroplasty |
| 心血管 | stent, cardiovascular, myocardial |
| 牙科 | dental |
| 其他 | osteoporosis, joint |

**判定逻辑**:
```
if any medical noise keyword in text:
    排除 → E5
```

---

## 五、筛选统计输出

### 统计维度
| 统计项 | 说明 |
|--------|------|
| Total | 初始记录总数 |
| Excluded_E1 | E1 排除数量 (主题不符) |
| Excluded_E3 | E3 排除数量 (纯动物实验) |
| Excluded_E4 | E4 排除数量 (纯算法/DL) |
| Excluded_E5 | E5 排除数量 (医疗噪音) |
| Included | 最终纳入数量 |

### 输出文件
1. **CSV 结果**: `screening_results.csv` - 包含所有记录的筛选结果
2. **CiteSpace 文件**: `download_included_for_citespace.txt` - 仅包含纳入的记录

---

## 六、技术实现细节

### 文本处理
- 所有文本转换为小写进行匹配
- 使用正则表达式进行单词边界匹配（动物/人类关键词）

### 正则表达式模式
```python
# 动物模式 - 使用单词边界确保精确匹配
r'\b(rat|rats|mouse|mice|rodent|rodents|macaque|macaques|monkey|monkeys|primate|primates|animal|animals|feline|canine|pig|pigs|porcine)\b'

# 人类模式 - 使用单词边界确保精确匹配  
r'\b(human|humans|patient|patients|clinical|subject|subjects)\b'

# 医疗噪音模式 - 使用单词边界确保精确匹配
r'\b(bone|bones|spine|spinal|vertebroplasty|orthopedic|orthopaedic|fracture|fractures|fixation|lumbar|cervical|dental|stent|stents|arthroplasty|osteoporosis|joint|cardiovascular|myocardial)\b'
```

### 记录分隔
- 使用 `\nER` 作为记录分隔符
- 排除包含 `FN Clarivate` 的元数据记录