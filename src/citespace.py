import pandas as pd
import os


def load_wos_data(file_path: str) -> pd.DataFrame:
    """
    加载并解析 Web of Science 导出的纯文本数据
    :param file_path: 合并后的 all_wos.txt 路径
    :return: 清洗后的 DataFrame
    """
    # 读取文本并按记录分割（WOS 每条记录以 "ER" 结尾）
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    records = content.split('\nER\n')[:-1]  # 去除最后一个空记录

    # 解析每条记录为字典
    data = []
    for rec in records:
        fields = {}
        lines = rec.strip().split('\n')
        for line in lines:
            if line.startswith(' '):
                # 续行，追加到上一个字段
                fields[last_key] += ' ' + line.strip()
            else:
                if ' ' in line:
                    key, value = line.split(' ', 1)
                    fields[key] = value.strip()
                    last_key = key
        data.append(fields)

    df = pd.DataFrame(data)

    # 基础清洗
    df = df.drop_duplicates(subset=['DI']).dropna(subset=['TI'])  # 按DOI去重，删除无标题的记录
    return df


def get_data_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    计算字段缺失率和重复率
    :param df: 加载后的 DataFrame
    :return: 统计 DataFrame
    """
    stats = pd.DataFrame({
        '缺失率': df.isnull().sum() / len(df),
        '重复率': df.duplicated().sum() / len(df)
    })
    return stats


if __name__ == "__main__":
    data_path = "data/spacetext.txt"  # 相对路径，根据项目结构调整
    df = load_wos_data(data_path)
    stats = get_data_stats(df)
    print("数据规模:", len(df))
    print(stats)
    stats.to_csv("outputs/field_stats.csv", encoding='utf-8-sig')

    import matplotlib.pyplot as plt

    missing_rate = df.isnull().sum() / len(df)
    missing_rate.plot(kind='bar', title='missing rate')
    plt.show()