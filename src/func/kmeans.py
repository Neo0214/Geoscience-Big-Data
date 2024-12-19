import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from utils.DataLoader import DataLoader


def main():

    data = DataLoader().load_data()


    columns = [
        'day_id', 'calling_nbr', 'called_nbr', 'calling_optr', 'called_optr',
        'calling_city', 'called_city', 'calling_roam_city', 'called_roam_city',
        'start_time', 'end_time', 'raw_dur', 'call_type', 'calling_cell'
    ]

    # 将数据转为 DataFrame
    df = pd.DataFrame(data, columns=columns)


    df['raw_dur'] = df['raw_dur'].astype(int)  # 通话时长转为数值
    df['call_type'] = df['call_type'].astype(int)  # 通话类型转为数值


    df['call_duration'] = df['raw_dur']  # 通话时长
    df['start_hour'] = df['start_time'].str.split(':').str[0].astype(int)  # 通话开始时刻（小时）
    df['end_hour'] = df['end_time'].str.split(':').str[0].astype(int)  # 通话结束时刻（小时）


    user_features = df.groupby('calling_nbr').agg(
        total_call_duration=('call_duration', 'sum'),  # 总通话时长
        avg_start_hour=('start_hour', 'mean'),         # 平均开始时间
        avg_end_hour=('end_hour', 'mean'),             # 平均结束时间
        call_type_ratio=('call_type', lambda x: x.mean()),  # 通话类型比例
    ).reset_index()


    user_features.fillna(0, inplace=True)

    # 特征标准化
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(user_features.iloc[:, 1:])  # 除去主叫号码列

    # 使用 KMeans 聚类
    n_clusters = 3
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    user_features['cluster'] = kmeans.fit_predict(scaled_features)


    numeric_columns = user_features.select_dtypes(include=[np.number])
    cluster_summary = numeric_columns.groupby(user_features['cluster']).mean()
    print("Cluster summary:")
    print(cluster_summary)
    # 写到文件
    cluster_summary.to_excel('kmeans_cluster_summary.xlsx')

    # 数据可视化
    plt.figure(figsize=(10, 6))
    sns.countplot(x='cluster', data=user_features, palette='viridis')
    plt.title('Cluster Distribution')
    plt.xlabel('Cluster')
    plt.ylabel('Number of Users')
    plt.show()


    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x='total_call_duration', y='avg_start_hour', hue='cluster', data=user_features, palette='viridis'
    )
    plt.title('Clusters by Total Call Duration and Avg Start Hour')
    plt.xlabel('Total Call Duration (seconds)')
    plt.ylabel('Average Start Hour')
    plt.legend(title='Cluster')
    plt.show()


    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x='total_call_duration',
        y='call_type_ratio',
        hue='cluster',
        data=user_features,
        palette='viridis'
    )
    plt.title('Clusters by Total Call Duration and Call Type Ratio')
    plt.xlabel('Total Call Duration (seconds)')
    plt.ylabel('Call Type Ratio')
    plt.legend(title='Cluster')
    plt.show()


if __name__ == '__main__':
    main()
