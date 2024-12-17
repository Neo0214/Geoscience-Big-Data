import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from utils.DataLoader import DataLoader


def main():
    # 1. 读取数据
    data = DataLoader().load_data()
    columns = [
        'day_id', 'calling_nbr', 'called_nbr', 'calling_optr', 'called_optr',
        'calling_city', 'called_city', 'calling_roam_city', 'called_roam_city',
        'start_time', 'end_time', 'raw_dur', 'call_type', 'calling_cell'
    ]
    df = pd.DataFrame(data, columns=columns)
    print("start process 2")
    # 2. 特征工程
    # 转换时间格式
    df['start_time'] = pd.to_datetime(df['start_time'], format='%H:%M:%S', errors='coerce')
    df['end_time'] = pd.to_datetime(df['end_time'], format='%H:%M:%S', errors='coerce')
    df['raw_dur'] = pd.to_numeric(df['raw_dur'], errors='coerce')

    # 统计每个用户的基站变化次数
    df['calling_cell'] = df['calling_cell'].astype(str)  # 确保类型一致
    user_cell_counts = df.groupby('calling_nbr')['calling_cell'].nunique()
    df['cell_changes'] = df['calling_nbr'].map(user_cell_counts)

    # 聚合用户特征
    user_features = df.groupby('calling_nbr').agg(
        total_calls=('calling_nbr', 'count'),
        avg_dur=('raw_dur', 'mean'),
        cell_changes=('cell_changes', 'max'),
        long_distance_calls=('call_type', lambda x: (x.isin(['漫游', '长途'])).sum()),
        city_changes=('calling_city', 'nunique')
    ).reset_index()

    # 创建目标标签
    # 定义基站是否固定
    user_features['is_fixed_location'] = (user_features['cell_changes'] <= 2).astype(int)

    # 定义通话类型是否为长途或漫游
    user_features['is_long_distance'] = (user_features['long_distance_calls'] > 0).astype(int)
    print("start process 2.2")
    # 将两者结合，形成4种分类：固定基站+市话、固定基站+长途/漫游、不固定基站+市话、不固定基站+长途/漫游
    user_features['target'] = (user_features['is_fixed_location'] * 2 + user_features['is_long_distance'])
    print("start process 2.2.1")
    # 编码城市特征
    # 创建 calling_nbr 到 calling_city 的映射
    calling_city_mapping = df[['calling_nbr', 'calling_city']].drop_duplicates().set_index('calling_nbr')[
        'calling_city'].to_dict()
    print("start process 2.2.2")
    # 使用这个字典直接映射
    user_features['calling_city_encoded'] = user_features['calling_nbr'].map(
        lambda x: calling_city_mapping.get(x, None))
    print("start process 2.2.3")
    # 编码城市特征
    city_mapping = {city: idx for idx, city in enumerate(df['calling_city'].unique())}
    print("start process 2.2.4")
    user_features['calling_city_encoded'] = user_features['calling_city_encoded'].map(city_mapping)

    print("start process 2.3")
    # 创建特征集和标签
    features = user_features[['calling_city_encoded', 'cell_changes', 'avg_dur', 'long_distance_calls', 'city_changes']]
    labels = user_features['target']
    print("start process 3")
    # 3. 数据集拆分
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42, stratify=labels)
    print("start process 4")
    # 4. 分类模型训练
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    print("start process 5")
    # 5. 模型评估
    y_pred = clf.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("start process 6")
    # 6. 特征重要性
    importances = clf.feature_importances_
    feature_names = features.columns
    print("Feature Importances:")
    for name, importance in zip(feature_names, importances):
        print(f"{name}: {importance:.4f}")

    # 7. 可视化部分
    # 混淆矩阵
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Fixed-Local', 'Fixed-LD', 'Multi-Local', 'Multi-LD'],
                yticklabels=['Fixed-Local', 'Fixed-LD', 'Multi-Local', 'Multi-LD'])
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.show()

    # 特征重要性条形图
    plt.figure(figsize=(8, 6))
    sns.barplot(x=importances, y=feature_names)
    plt.title("Feature Importance")
    plt.xlabel("Importance Score")
    plt.ylabel("Features")
    plt.show()

    # 分类结果分布
    plt.figure(figsize=(6, 4))
    sns.countplot(x='target', data=user_features, palette='viridis')
    plt.title("User Categories Distribution")
    plt.xlabel("User Category")
    plt.ylabel("Count")
    plt.show()


if __name__ == '__main__':
    main()
