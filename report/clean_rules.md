clean_rules.md
本文件用于规范本项目在全植入式情景下脑电信号相关数据（原始信号、预处理数据、压缩结果、验证数据）导出、字段统一、数据清洗、初步筛选与去重过程中的处理规则。
本文件服务于以下目标：
- 保证不同采集场景、不同设备导出的脑电信号数据在进入正式分析、算法迭代与系统联调前具备统一结构；
- 保证每一步清洗操作可追溯、可解释，便于后续算法优化与系统故障排查；
- 为后续 data_quality.md、processed 数据文件夹、系统性能验证及论文写作提供统一的数据处理依据。
当前项目已实际涉及两类核心数据源，涵盖信号采集、算法处理全流程：
- 植入式设备采集原始数据（颅内ECoG、LFP、S/U/MUA信号）
- 算法处理中间/结果数据（预处理后信号、压缩编码数据、重构信号、性能指标数据）
由于两类数据源的格式规范、噪声特性、数据维度、字段含义不同，因此本文件采用“先分类清洗，再统一映射”的原则，确保数据一致性与可用性。
一、总原则
1. 分类处理，不直接混表
植入式设备原始采集数据与算法处理数据不得直接合并后再清洗。必须先分别完成以下操作，之后才能进入统一字段映射与合并阶段：
- 字段识别与标注（明确数据来源、信号类型、采集参数）
- 基础去噪（剔除设备故障、环境干扰导致的无效数据）
- 文本/参数规范化（统一单位、编码格式、字段命名）
- 初步筛选（剔除明显无效、异常的数据记录）
- 唯一标识保留（为每条数据分配可追溯的唯一标识）
2. 保留原始数据
所有清洗操作都必须建立在“保留原始文件”的前提下进行。原始采集的信号文件（.txt、.csv、.dat格式）、算法输出原始文件不得覆盖。清洗后的数据应另存为新文件，并在文件名中标注清洗阶段与日期，便于追溯。
3. 优先保留核心字段
无论数据来源如何，以下核心字段/参数优先保留，确保后续系统设计、算法验证与论文分析的可用性：
- 信号基础信息：信号类型（ECoG/LFP/MUA）、采集通道号、采样率、位宽
- 采集参数：采集时间、植入设备型号、采集部位（颅内/皮层）
- 数据核心内容：原始采样值/预处理后采样值、压缩编码结果、重构信号值
- 性能指标：信噪比（SNR）、压缩比、处理延迟、功耗数据
- 唯一标识：DOI（如有）、数据采集编号、算法处理批次号
如数据支持，建议额外保留：
- 采集环境：实验对象（动物/模拟装置）、环境温度、干扰情况
- 算法参数：预处理滤波参数、压缩算法类型、编码方式
- 验证数据：信号重构误差、临床/实验验证标注
4. 先清洗格式，再做有效性判断
不要在字段命名混乱、参数单位不统一、数据格式不规范前就做正式的有效性筛选。正确处理顺序是：
- 统一字段命名与参数单位
- 清除明显错误值（如采样率为0、信号值超出ADC量程、延迟为负）
- 标准化文本与格式（统一编码、日期格式、算法名称）
- 去重（剔除重复采集、重复处理的数据）
- 初筛有效性（判断数据是否符合系统设计与分析要求）
二、数据源分项清洗规则
2.1 植入式设备原始采集数据清洗规则
2.1.1 当前主要字段/参数
植入式设备（如颅内采集电极、植入式ASIC）当前已出现或已稳定导出的字段/参数主要包括：
- DeviceID-设备编号
- SignalType-信号类型
- Channel-通道号
- SamplingRate-采样率（Hz）
- BitWidth-位宽（bit）
- CollectTime-采集时间
- CollectSite-采集部位
- RawData-原始采样值
- NoiseLevel-噪声等级
- ValidFlag-有效标志位
2.1.2 字段重命名规则
建议将植入式设备原始字段统一映射为以下标准字段名，便于后续统一分析：
- DeviceID-设备编号 → device_id
- SignalType-信号类型 → signal_type
- Channel-通道号 → channel
- SamplingRate-采样率（Hz） → sampling_rate
- BitWidth-位宽（bit） → bit_width
- CollectTime-采集时间 → collect_time
- CollectSite-采集部位 → collect_site
- RawData-原始采样值 → raw_data
- NoiseLevel-噪声等级 → noise_level
- ValidFlag-有效标志位 → valid_flag
2.1.3 文本与参数标准化规则
- 删除所有字段值首尾空格、无效字符（如乱码、特殊符号）；
- 统一参数单位：采样率（Hz）、位宽（bit）、噪声等级（dB），不得混用单位；
- signal_type 统一规范：ECoG（皮层脑电图）、LFP（局部场电位）、MUA（多单元动作电位）、SUA（单单元动作电位），缩写统一大写；
- collect_site 统一规范：颅内、皮层，避免“大脑内部”“皮层区域”等模糊表述；
- valid_flag 统一为：1（有效）、0（无效），不得使用“有效/无效”“是/否”等文本值；
- raw_data 保留原始采样值，不做任何缩放、修正，后续预处理单独处理。
2.1.4 时间与设备标识规则
- collect_time 统一为“YYYY-MM-DD HH:MM:SS”格式，缺失时间的记录标记为“未知”，不随意补全；
- device_id 保留原始编号，不得修改，作为设备采集数据的唯一标识；
- 同一设备、同一通道、同一时间采集的数据，视为同一批次，补充“batch_id”字段标记。
2.1.5 特殊规则
- valid_flag 为0的记录（无效数据）暂不删除，标记后保留，用于后续设备故障分析；
- noise_level 超出正常范围（如>30dB）的记录，标记为“高噪声”，不直接剔除，需结合采集环境判断；
- RawData 为空或全为0的记录，标记为“无效采样”，后续统一处理。
2.2 算法处理数据清洗规则
2.2.1 当前主要字段/参数
算法处理（预处理、压缩编码、重构）过程中导出的典型字段/参数包括：
- BatchID-处理批次号
- SourceDataID-原始数据编号（关联原始采集数据）
- ProcessType-处理类型（预处理/压缩/重构）
- Algorithm-算法名称
- ProcessedData-处理后数据
- CompressionRatio-压缩比
- SNR-信噪比（dB）
- Delay-处理延迟（ms）
- PowerConsumption-功耗（μW）
- ProcessTime-处理时间
2.2.2 字段重命名规则
建议统一映射为以下标准字段名，确保与原始采集数据字段适配：
- BatchID-处理批次号 → batch_id
- SourceDataID-原始数据编号 → source_data_id
- ProcessType-处理类型 → process_type
- Algorithm-算法名称 → algorithm
- ProcessedData-处理后数据 → processed_data
- CompressionRatio-压缩比 → compression_ratio
- SNR-信噪比（dB） → snr
- Delay-处理延迟（ms） → delay
- PowerConsumption-功耗（μW） → power_consumption
- ProcessTime-处理时间 → process_time
2.2.3 算法处理数据特殊规则
- source_data_id 必须保留，作为关联原始采集数据的唯一标识，确保数据可追溯；
- process_type 统一规范：预处理（preprocess）、压缩（compression）、重构（reconstruction），缩写统一小写；
- algorithm 统一规范：如CS（压缩感知）、DWT（离散小波变换）、DPCM（差分脉冲编码调制），缩写统一大写，全称可在备注中补充；
- compression_ratio 保留小数形式（如8.0、10.5），不得使用“8:1”“10.5:1”等比例格式；
- snr、delay、power_consumption 若缺失，标记为“未检测”，不随意填充默认值；
- processed_data 需与原始数据的采样率、位宽保持一致，便于后续对比分析。
三、统一字段映射规则
在植入式设备原始采集数据与算法处理数据分别清洗完成后，再进入统一字段映射与合并阶段。建议统一保留以下字段，形成项目统一数据表，支撑后续分析与验证：
- 基础标识：data_id（全局唯一标识）、device_id、batch_id、source_data_id
- 信号信息：signal_type、channel、sampling_rate、bit_width、collect_site
- 时间信息：collect_time、process_time
- 数据内容：raw_data、processed_data
- 算法参数：process_type、algorithm、compression_ratio
- 性能指标：snr、delay、power_consumption、noise_level、valid_flag
- 辅助信息：data_source（数据来源：原始采集/算法处理）、source_file（原始文件名）
3.1 必保字段
以下字段进入统一表时优先级最高，缺失则视为无效记录（标记后单独存放）：
- data_id、device_id、source_data_id（唯一标识，确保可追溯）
- signal_type、sampling_rate、bit_width（信号核心参数）
- raw_data（原始采集数据必保）、processed_data（算法处理数据必保）
- valid_flag（判断数据有效性）
3.2 条件保留字段
以下字段有则保留，无则留空，不随意填充默认值：
- collect_site、collect_time、process_time
- algorithm、compression_ratio、snr、delay、power_consumption、noise_level
3.3 允许为空字段
以下字段允许缺失，但不能乱填，缺失时留空即可：
- batch_id（无批次处理时留空）
- process_type、algorithm（原始采集数据无相关字段时留空）
四、去重规则
4.1 去重优先级
去重按以下顺序执行，满足任一条件即判定为重复记录：
- data_id 完全一致 → 判定为重复记录；
- source_data_id + process_type + algorithm 完全一致（同一原始数据、同一处理类型、同一算法的重复处理结果）；
- device_id + collect_time + channel + signal_type 完全一致（同一设备、同一时间、同一通道、同一类型的重复采集数据）；
- raw_data 与 processed_data 完全一致，且其他核心参数（sampling_rate、bit_width）无差异，视为重复处理数据。
4.2 去重保留原则
若存在重复记录，保留规则如下：
- 优先保留字段更完整者（如性能指标、辅助信息更齐全的记录）；
- 算法处理数据重复时，优先保留处理时间最新、性能更优（snr更高、delay更低、power_consumption更低）的记录；
- 原始采集数据重复时，优先保留 valid_flag=1（有效）、noise_level 更低的记录；
- 不删除原始来源信息，应保留 data_source 和 source_file 字段，便于追溯重复原因。
4.3 不应误判为重复的情况
以下情况不视为重复记录，不得误判剔除：
- 同一原始数据，采用不同算法（algorithm不同）处理的结果；
- 同一设备、同一通道，不同时间（collect_time不同）采集的相同类型信号；
- 同一批次处理，不同通道（channel不同）的信号数据；
- 同一原始数据，不同处理类型（process_type不同）的结果（如预处理后与压缩后的数据）。
五、有效性筛选规则（清洗阶段初筛）
5.1 纳入标准
数据需尽量同时满足以下条件，方可纳入后续分析与系统验证：
- 原始采集数据：valid_flag=1，noise_level ≤ 30dB，采样率、位宽符合系统设计要求（8kHz~32kHz、12bit/16bit）；
- 算法处理数据：关联的原始数据有效，处理过程无异常，性能指标符合设计目标（压缩比≥8:1、snr≥25dB、delay≤10ms、power_consumption≤5μW）；
- 核心字段（必保字段）无缺失，数据格式规范，无明显错误。
5.2 排除标准
以下情况在清洗阶段可初步标记为排除候选，后续统一处理：
- 原始采集数据：valid_flag=0，noise_level > 30dB，采样率、位宽超出系统设计范围，raw_data为空或全为0；
- 算法处理数据：关联的原始数据无效，处理结果异常（如compression_ratio<1、snr<10dB、delay>50ms）；
- 核心字段缺失，无法补充且无法追溯；
- 数据格式混乱，无法完成标准化处理，且无原始文件可追溯修正。
5.3 边界数据处理规则
对于“有一定有效性，但未完全满足纳入标准”的边界数据，不直接删除，而是标记为以下状态，便于后续人工复核：
- keep = maybe（是否保留：待定）
- exclude_reason = 边界数据（说明排除原因：如性能指标略低于设计目标、部分辅助字段缺失）
- note = 需二次人工判断（补充备注：如snr=24dB，接近设计目标25dB，可用于算法优化分析）
六、建议新增字段
在清洗后的统一表中，建议新增以下人工处理字段，便于后续数据管理、质量验证与追溯：
- keep：是否保留（yes / no / maybe）
- exclude_reason：排除原因（如“高噪声”“核心字段缺失”“性能不达标”）
- note：备注（补充数据异常原因、复核意见等）
- screen_stage：筛选阶段（raw/processed/merged，标记数据当前所处的清洗筛选阶段）
- data_source：数据来源（原始采集/算法处理）
- source_file：原始文件名（便于追溯原始数据）
新增字段的作用：
- 便于后续生成 processed 文件夹中的最终分析数据；
- 为 data_quality.md 提供数据质量统计依据；
- 回溯筛选过程，便于论文中数据处理部分的撰写；
- 支撑系统性能验证的数据追溯与异常排查。
七、文件保存规则
为规范文件管理，确保数据可追溯、可复用，所有数据文件与说明文档按以下目录结构保存：
7.1 原始文件
原始采集信号文件、算法原始输出文件统一放入以下目录，文件名标注数据来源、日期与类型：
data/raw/
示例：data/raw/device_01_20240520_ECoG.txt、data/raw/batch_01_20240520_compression.csv
7.2 清洗中间表
字段重命名、文本/参数标准化、初筛标记后的中间数据表格，建议放入以下目录：
data/interim/
示例：data/interim/raw_data_cleaned_20240520.csv、data/interim/processed_data_cleaned_20240520.csv
7.3 最终分析表
用于后续系统性能验证、算法优化、知识图谱分析、论文写作的统一数据表，建议放入以下目录：
data/processed/
示例：data/processed/unified_brain_signal_data.csv
7.4 文档说明
本文件 clean_rules.md 属于项目数据处理规则说明文档，应放入以下目录，与其他说明文档统一管理：
reports/
配套的 data_quality.md、系统性能验证报告等文档，也统一放入此目录。
