# Web of Science 文献数据清洗规则 (Clean Rules)

## 一、数据输入来源
- Web of Science 导出格式 (纯文本 .txt)
- 每条记录以 `ER` 结尾分隔
- 可能包含多个批次的数据文件

## 二、数据字段提取与映射

### 2.1 核心字段提取
citespace.py 从 WOS 格式中提取以下核心字段：

| 字段代码 | 字段名称 | 说明 |
|----------|----------|------|
| TI | Title | 文献标题 |
| AB | Abstract | 摘要 |
| DE | Keywords | 关键词 |
| AU | Author | 作者 |
| PY | Publication Year | 出版年份 |
| SO | Source | 来源出版物 |
| DI | DOI | 数字对象标识符 |

### 2.2 字段解析逻辑

```python
# 逐行解析 WOS 记录
for line in lines:
    if not line:
        continue
    if line.startswith(' '):
        # 续行：追加到上一个字段
        fields[last_key] += ' ' + line.strip()
    else:
        # 新字段：分割键值对
        if ' ' in line:
            key, value = line.split(' ', 1)
            fields[key] = value.strip()
            last_key = key
```

**关键规则**:
1. 行首带空格的为续行内容，需追加到上一字段末尾
2. 其他行为新字段定义，使用第一个空格分隔键和值
3. 值会自动去除首尾空白

## 三、数据清洗规则

### 3.1 去重规则

**去重依据**: DOI (`DI` 字段)

```python
if 'DI' in df.columns:
    df = df.drop_duplicates(subset=['DI'])  # 按 DOI 去重
```

**说明**:
- 以 DOI 作为唯一标识符
- 相同 DOI 的记录视为重复，保留第一条，其余删除
- 仅当 DI 字段存在时才执行去重

### 3.2 缺失值处理

**必填字段**: TI (标题)

```python
df = df.dropna(subset=['TI'])  # 删除无标题的记录
```

**规则**:
- 所有缺少标题 (TI) 的记录直接删除
- 其他字段 (AB, DE, AU, SO 等) 允许缺失

### 3.3 有效记录过滤

**排除规则**:
1. 空记录：解析后为空的记录
2. 元数据记录：包含 `FN Clarivate` 的记录

```python
for rec in records:
    rec = rec.strip()
    if not rec or "FN Clarivate" in rec:
        continue  # 跳过无效记录
```

## 四、数据质量统计

### 4.1 统计指标

```python
def get_data_stats(df: pd.DataFrame):
    stats = pd.DataFrame({
        '缺失率': df.isnull().sum() / len(df),
        '重复数': df.duplicated().sum()
    })
    return stats
```

| 统计项 | 计算方式 | 说明 |
|--------|----------|------|
| 缺失率 | `df.isnull().sum() / len(df)` | 各字段缺失记录比例 |
| 重复数 | `df.duplicated().sum()` | 存在重复的记录总数 |

### 4.2 可视化输出

- 使用 matplotlib 绘制各字段缺失率柱状图
- 图表标题：`Missing Rate per Field`

## 五、批量数据处理流程

### 5.1 文件夹批量读取

```python
def load_wos_data_folder(folder_path: str) -> pd.DataFrame:
    all_records = []
    
    # 遍历文件夹所有 .txt 文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            # 读取并解析每条记录
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            records = content.split('\nER\n')
            for rec in records:
                rec = rec.strip()
                if not rec or "FN Clarivate" in rec:
                    continue
                all_records.append(rec)
```

### 5.2 数据转换与清洗

1. 解析所有记录为字典列表
2. 转换为 pandas DataFrame
3. 按 DOI 去重
4. 删除无标题记录

## 六、输出文件

### 6.1 统计数据
- 文件路径：`../outputs/field_stats.csv`
- 编码：`utf-8-sig`
- 内容：各字段缺失率和重复数统计

### 6.2 数据规模输出
```
数据规模: <记录总数>
字段统计：
<各字段统计详情>
```

## 七、技术实现细节

### 记录分隔符
- **主分隔符**: `\nER\n` (换行 + ER + 换行)
- 解析后需去除每条记录的首尾空白

### 编码要求
- 输入文件：`utf-8`
- 输出 CSV: `utf-8-sig` (兼容 Excel)

### 依赖库
- `pandas`: 数据处理和统计分析
- `matplotlib`: 数据质量可视化
- `os`: 文件系统操作