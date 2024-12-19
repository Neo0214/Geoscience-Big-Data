import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from utils.DataLoader import DataLoader
from tqdm import tqdm



def aggregate_group_with_progress(group):

    return {
        'called_city': group['called_city'].mode()[0],
        'calling_roam_city': group['calling_roam_city'].mode()[0],
        'called_roam_city': group['called_roam_city'].mode()[0],
        'start_hour': group['start_hour'].mean(),
        'raw_dur': group['raw_dur'].mean(),
        'calling_cell': group['calling_cell'].mode()[0],
        'call_type': group['call_type'].mode()[0]
    }


def main():

    data = DataLoader().load_data()


    columns = ['day_id', 'calling_nbr', 'called_nbr', 'calling_optr', 'called_optr', 'calling_city', 'called_city',
               'calling_roam_city', 'called_roam_city', 'start_time', 'end_time', 'raw_dur', 'call_type',
               'calling_cell']
    df = pd.DataFrame(data, columns=columns)


    df['start_hour'] = pd.to_datetime(df['start_time'], format='%H:%M:%S').dt.hour
    df['raw_dur'] = pd.to_numeric(df['raw_dur'], errors='coerce')
    print("process 2")
    grouped = df.groupby('calling_nbr')
    total_groups = len(grouped)
    aggregated_df = pd.DataFrame(
        [aggregate_group_with_progress(group) for _, group in tqdm(grouped, total=total_groups, desc="Aggregating")]
    )
    print("process 3")


    encoder = LabelEncoder()
    categorical_columns = ['called_city', 'calling_roam_city',
                           'called_roam_city', 'calling_cell']
    for col in tqdm(categorical_columns):
        aggregated_df[col] = encoder.fit_transform(aggregated_df[col])


    X = aggregated_df.drop(columns=['call_type'])
    y = aggregated_df['call_type']

    # 5. 随机森林分类

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("process 4")

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # 预测并评估
    y_pred = model.predict(X_test)


    print("Classification Report:")
    print(classification_report(y_test, y_pred))


    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['市话', '其它'],
                yticklabels=['市话', '其它'])
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()

    # 可视化特征重要性
    feature_importance = model.feature_importances_
    features = X.columns
    feature_df = pd.DataFrame({'Feature': features, 'Importance': feature_importance})
    feature_df = feature_df.sort_values(by='Importance', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=feature_df)
    plt.title('Feature Importance')
    plt.show()




if __name__ == '__main__':
    main()
