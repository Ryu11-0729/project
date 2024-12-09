import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from django.conf import settings
from dvadmin.utils.json_response import ErrorResponse, DetailResponse
from rest_framework.viewsets import ModelViewSet
from scipy.stats import chi2_contingency
# 设置支持中文的字体
matplotlib.rcParams['font.family'] = 'SimHei'  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report
import json
from scipy.stats import spearmanr
from scipy.stats import kruskal
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error, mean_absolute_error





class CustomModelViewSet(ModelViewSet):
    pass


class DataAnalyzePredictViewSet(CustomModelViewSet):
    rf = None
    save_path = "D:/tomcat/apache-tomcat-9.0.80-windows-x64/apache-tomcat-9.0.80/webapps/ROOT/images/"

    def data_analyze(self, request):
        Kruska, kafang = self.rf_load_data()
        data = {
            'Kruska': Kruska,
            'kafang': kafang
        }
        return DetailResponse(msg="ordinaryUser page",data = data)

    def data_predict(self, request):
        class_report_rf, y_pred_rf_data_usage = self.rf_data_yuce()
        data = {
            class_report_rf,
            y_pred_rf_data_usage
        }
        return DetailResponse(msg="predict page",data = data)

    # 绘图保存到tomcat服务器路径下
    def rf_load_data(self):
        data_path = str(settings.BASE_DIR) + '/dataset.csv'
        data = pd.read_csv(data_path)
        # 保存箱线图
        plt.figure(figsize=(20, 10))
        feature_map = {
            'App Usage Time (min/day)': '每天在移动应用上花费的时间（分钟）',
            'Screen On Time (hours/day)': '屏幕每天平均活跃时间（小时）',
            'Battery Drain (mAh/day)': '每日电池消耗量（毫安时）',
            'Number of Apps Installed': '设备上安装的应用程序总数',
            'Data Usage (MB/day)': '每日移动数据消耗量（兆字节）',
            'Age': '年龄',
            'User Behavior Class': '用户行为分类'
        }
        for i, (col, col_name) in enumerate(feature_map.items(), 1):
            plt.subplot(2, 4, i)
            sns.boxplot(y=data[col], color='orange')
            plt.title(f'{col_name}的箱线图', fontsize=14)
            plt.ylabel('数值', fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(self.save_path + "/xiangxiantu1.png", dpi=300)
        plt.close()



        plt.figure(figsize=(20, 15))
        plt.subplot(3, 4, 1)
        Operating_System_counts = data['Operating System'].value_counts()
        plt.pie(Operating_System_counts, labels=Operating_System_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('设备的操作系统分布', fontsize=16)
        plt.subplot(3, 4, 2)
        sns.histplot(data['App Usage Time (min/day)'], kde=True, bins=32)
        plt.title('每天在移动应用上花费的时间分布', fontsize=16)
        plt.xlabel('每天在移动应用上花费的时间（分钟）')
        plt.ylabel('人数')

        plt.subplot(3, 4, 3)
        sns.histplot(data['Screen On Time (hours/day)'], kde=True, bins=11)
        plt.title('屏幕每天平均活跃时间分布', fontsize=16)
        plt.xlabel('屏幕每天平均活跃时间（小时）')
        plt.ylabel('人数')

        plt.subplot(3, 4, 4)
        sns.histplot(data['Battery Drain (mAh/day)'], kde=True, bins=24)
        plt.title('每日电池消耗量分布', fontsize=16)
        plt.xlabel('每日电池消耗量（毫安时）')
        plt.ylabel('人数')

        plt.subplot(3, 4, 5)
        sns.histplot(data['Number of Apps Installed'], kde=True, bins=21)
        plt.title('设备上安装的应用程序总数分布', fontsize=16)
        plt.xlabel('设备上安装的应用程序总数')
        plt.ylabel('人数')

        plt.subplot(3, 4, 6)
        sns.histplot(data['Data Usage (MB/day)'], kde=True, bins=25, color='gray')
        plt.title('每日移动数据消耗量分布', fontsize=16)
        plt.xlabel('每日移动数据消耗量（兆字节）')
        plt.ylabel('人数')

        plt.subplot(3, 4, 7)
        sns.histplot(data['Age'], kde=True, bins=20, color='lime')
        plt.title('用户年龄分布', fontsize=16)
        plt.xlabel('用户年龄')
        plt.ylabel('人数')

        ax8 = plt.subplot(3, 4, 8)
        sns.countplot(x='Gender', data=data, color='lime')
        plt.title('用户性别分布', fontsize=16)
        plt.xlabel('用户性别')
        plt.ylabel('人数')
        for p in ax8.patches:
            ax8.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', fontsize=11, color='black', xytext=(0, 5),
                         textcoords='offset points')

        ax9 = plt.subplot(3, 4, (9, 10))
        sns.countplot(x='Device Model', data=data, color='cyan')
        plt.title('用户智能手机的型号分布', fontsize=16)
        plt.xlabel('用户智能手机的型号')
        plt.ylabel('人数')
        for p in ax9.patches:
            ax9.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', fontsize=11, color='black', xytext=(0, 5),
                         textcoords='offset points')

        ax11 = plt.subplot(3, 4, (11, 12))
        sns.countplot(x='User Behavior Class', data=data, color='lime')
        plt.title('用户行为类别分布', fontsize=16)
        plt.xlabel('用户行为类别')
        plt.ylabel('人数')
        for p in ax11.patches:
            ax11.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha='center', va='center', fontsize=11, color='black', xytext=(0, 5),
                          textcoords='offset points')

        plt.tight_layout()
        plt.savefig(self.save_path + "/fenbutu1.png", dpi=300)
        plt.close()

        colors = ['#FF5733', '#33FF57', '#3357FF', '#F5B700', '#F700B8']  # 示例颜色
        device_model_sales = data.groupby(['User Behavior Class', 'Device Model']).size().unstack(fill_value=0)

        fig, ax = plt.subplots(figsize=(16, 8))
        device_model_sales.plot(kind='bar', stacked=True, ax=ax, color=colors)
        # 为了将标签放在条形中，我们计算每个条形的位置和高度
        for i, (behavior_idx, model_row) in enumerate(device_model_sales.iterrows()):
            cum_height = 0  # 累积高度，用于定位条形中的标签位置
            for model_idx, value in model_row.items():
                # 计算占比
                percentage = value / model_row.sum() * 100
                if value > 0:  # 仅为非零值添加标签
                    ax.text(i, cum_height + value / 2, f'{model_idx}: {percentage:.1f}%',
                            ha='center', va='center', color='black', fontsize=12, fontweight='bold')
                cum_height += value

        # 移除图例
        ax.legend().set_visible(False)
        ax.set_title('用户行为类别与设备型号分布', fontsize=16)
        ax.set_xlabel('用户行为类别', fontsize=12)
        ax.set_ylabel('用户数量', fontsize=12)
        ax.set_xticklabels(device_model_sales.index, rotation=0)
        plt.tight_layout()
        plt.savefig(self.save_path + "/xingwei_and_shebeileixingfenbu.png", dpi=300)
        plt.close()

        os_sales = data.groupby(['User Behavior Class', 'Operating System']).size().unstack(fill_value=0)

        fig, ax = plt.subplots(figsize=(16, 8))
        os_sales.plot(kind='bar', stacked=True, ax=ax)
        # 为了将标签放在条形中，我们计算每个条形的位置和高度
        for i, (behavior_idx, model_row) in enumerate(os_sales.iterrows()):
            cum_height = 0  # 累积高度，用于定位条形中的标签位置
            for model_idx, value in model_row.items():
                # 计算占比
                percentage = value / model_row.sum() * 100
                if value > 0:  # 仅为非零值添加标签
                    ax.text(i, cum_height + value / 2, f'{model_idx}: {percentage:.1f}%',
                            ha='center', va='center', color='black', fontsize=12, fontweight='bold')
                cum_height += value

        # 移除图例
        ax.legend().set_visible(False)
        ax.set_title('用户行为类别与操作系统分布', fontsize=16)
        ax.set_xlabel('用户行为类别', fontsize=12)
        ax.set_ylabel('用户数量', fontsize=12)
        ax.set_xticklabels(os_sales.index, rotation=0)
        plt.tight_layout()
        plt.savefig(self.save_path + "/xingwei_and_caozuoxitongfenbu.png", dpi=300)
        plt.close()

        plt.figure(figsize=(16, 8))
        sns.boxplot(x=data['User Behavior Class'], y=data['App Usage Time (min/day)'])
        plt.title('用户行为类别与每天在移动应用上花费的时间分布')
        plt.xlabel('用户行为类别')
        plt.ylabel('每天在移动应用上花费的时间（分钟）')
        plt.tight_layout()
        plt.savefig(self.save_path + "/xingwei_and_meitianyidongfenbu.png", dpi=300)
        plt.close()

        plt.figure(figsize=(16, 8))
        sns.boxplot(x=data['User Behavior Class'], y=data['Screen On Time (hours/day)'])
        plt.title('用户行为类别与屏幕每天平均活跃时间分布')
        plt.xlabel('用户行为类别')
        plt.ylabel('屏幕每天平均活跃时间（小时）')
        plt.tight_layout()
        plt.savefig(self.save_path + "/xingwei_and_pingmumeitianfenbu.png", dpi=300)
        plt.close()

        plt.figure(figsize=(16, 8))
        sns.boxplot(x=data['User Behavior Class'], y=data['Battery Drain (mAh/day)'])
        plt.title('用户行为类别与每日电池消耗量分布')
        plt.xlabel('用户行为类别')
        plt.ylabel('每日电池消耗量（毫安时）')
        plt.savefig(self.save_path + "/xingwei_and_meiridianchifenbu.png", dpi=300)
        plt.close()

        plt.figure(figsize=(16,8))
        sns.boxplot(x=data['User Behavior Class'],y=data['Number of Apps Installed'])
        plt.title('用户行为类别与设备上安装的应用程序总数分布')
        plt.xlabel('用户行为类别')
        plt.ylabel('设备上安装的应用程序总数')
        plt.savefig(self.save_path + "/xingwei_and_shebeishanganzhuangfenbu.png", dpi=300)
        plt.close()

        plt.figure(figsize=(16, 8))
        sns.boxplot(x=data['User Behavior Class'], y=data['Data Usage (MB/day)'])
        plt.title('用户行为类别与每日移动数据消耗量分布')
        plt.xlabel('用户行为类别')
        plt.ylabel('每日移动数据消耗量（兆字节）')
        plt.savefig(self.save_path + "/xingwei_and_meiriyidingshujuxiaohaoliangfenbu.png", dpi=300)
        plt.close()

        plt.figure(figsize=(16, 8))
        sns.boxplot(x=data['User Behavior Class'], y=data['Age'])
        plt.title('用户行为类别与用户年龄分布')
        plt.xlabel('用户行为类别')
        plt.ylabel('用户年龄')
        plt.savefig(self.save_path + "/xingwei_and_yonghunianlingfenbu.png", dpi=300)
        plt.close()

        gender_sales = data.groupby(['User Behavior Class', 'Gender']).size().unstack(fill_value=0)

        fig, ax = plt.subplots(figsize=(16, 8))
        gender_sales.plot(kind='bar', stacked=True, ax=ax)
        # 为了将标签放在条形中，我们计算每个条形的位置和高度
        for i, (behavior_idx, model_row) in enumerate(gender_sales.iterrows()):
            cum_height = 0  # 累积高度，用于定位条形中的标签位置
            for model_idx, value in model_row.items():
                # 计算占比
                percentage = value / model_row.sum() * 100
                if value > 0:  # 仅为非零值添加标签
                    ax.text(i, cum_height + value / 2, f'{model_idx}: {percentage:.1f}%',
                            ha='center', va='center', color='black', fontsize=12, fontweight='bold')
                cum_height += value

        # 移除图例
        ax.legend().set_visible(False)
        ax.set_title('用户行为类别与用户性别分布', fontsize=16)
        ax.set_xlabel('用户行为类别', fontsize=12)
        ax.set_ylabel('用户数量', fontsize=12)
        ax.set_xticklabels(gender_sales.index, rotation=0)
        plt.tight_layout()
        plt.savefig(self.save_path + "/xingwei_and_yonghuxingbiefenbu.png", dpi=300)
        plt.close()

        def plot_spearmanr(data, features, title, wide, height):
            # 计算斯皮尔曼相关性矩阵和p值矩阵
            spearman_corr_matrix = data[features].corr(method='spearman')
            pvals = data[features].corr(method=lambda x, y: spearmanr(x, y)[1]) - np.eye(len(data[features].columns))

            # 转换 p 值为星号
            def convert_pvalue_to_asterisks(pvalue):
                if pvalue <= 0.001:
                    return "***"
                elif pvalue <= 0.01:
                    return "**"
                elif pvalue <= 0.05:
                    return "*"
                return ""

            # 应用转换函数
            pval_star = pvals.applymap(lambda x: convert_pvalue_to_asterisks(x))

            # 转换成 numpy 类型
            corr_star_annot = pval_star.to_numpy()

            # 定制 labels
            corr_labels = spearman_corr_matrix.to_numpy()
            p_labels = corr_star_annot
            shape = corr_labels.shape

            # 合并 labels
            labels = (np.asarray(["{0:.2f}\n{1}".format(data, p) for data, p in
                                  zip(corr_labels.flatten(), p_labels.flatten())])).reshape(shape)

            # 绘制热力图
            fig, ax = plt.subplots(figsize=(height, wide), dpi=100, facecolor="w")
            sns.heatmap(spearman_corr_matrix, annot=labels, fmt='', cmap='coolwarm',
                        vmin=-1, vmax=1, annot_kws={"size": 10, "fontweight": "bold"},
                        linecolor="k", linewidths=.2, cbar_kws={"aspect": 13}, ax=ax)

            ax.tick_params(bottom=False, labelbottom=True, labeltop=False,
                           left=False, pad=1, labelsize=12)
            ax.yaxis.set_tick_params(labelrotation=0)

            # 自定义 colorbar 标签格式
            cbar = ax.collections[0].colorbar
            cbar.ax.tick_params(direction="in", width=.5, labelsize=10)
            cbar.set_ticks([-1, -0.5, 0, 0.5, 1])
            cbar.set_ticklabels(["-1.00", "-0.50", "0.00", "0.50", "1.00"])
            cbar.outline.set_visible(True)
            cbar.outline.set_linewidth(.5)

            plt.title(title)
            plt.savefig(self.save_path + "/bianliangzhijianrelitu.png", dpi=300)
            plt.close()

        new_column_names = ['User ID', 'Device Model', 'Operating System',
                            'App Usage Time', 'Screen On Time',
                            'Battery Drain', 'Apps Installed',
                            'Data Usage', 'Age', 'Gender', 'User Behavior Class']
        data.columns = new_column_names
        tdata = data.copy()
        features = data.drop(['User ID', 'Device Model', 'Operating System', 'Gender'], axis=1).columns.tolist()
        new_column_names = ['User ID', 'Device Model', 'Operating System',
                            'App Usage Time (min/day)', 'Screen On Time (hours/day)',
                            'Battery Drain (mAh/day)', 'Number of Apps Installed',
                            'Data Usage (MB/day)', 'Age', 'Gender', 'User Behavior Class']
        data.columns = new_column_names
        plot_spearmanr(tdata, features, '各变量之间的斯皮尔曼相关系数热力图', 12, 15)


        # Kruskal-Wallis H检验
        numeric_columns = [
            'App Usage Time (min/day)',
            'Screen On Time (hours/day)',
            'Battery Drain (mAh/day)',
            'Number of Apps Installed',
            'Data Usage (MB/day)',
            'Age'
        ]

        results = {}

        for col in numeric_columns:
            # 执行Kruskal-Wallis H检验
            h_statistic, p_value = kruskal(
                *[group[col].values for name, group in data.groupby('User Behavior Class')]
            )

            results[col] = {
                'H-statistic': h_statistic,
                'p-value': p_value
            }

        # 将结果转换为DataFrame
        results_df = pd.DataFrame(results).T
        Kruskal_Wallis_H = {
            'App': {
                'hh': results_df.iloc[0, 0],
                'p': results_df.iloc[0, 1],
            },
            'Screen': {
                'hh': results_df.iloc[1, 0],
                'p': results_df.iloc[1, 1],
            },
            'Battery': {
                'hh': results_df.iloc[2, 0],
                'p': results_df.iloc[2, 1],
            },
            'Number': {
                'hh': results_df.iloc[3, 0],
                'p': results_df.iloc[3, 1],
            },
            'Data': {
                'hh': results_df.iloc[4, 0],
                'p': results_df.iloc[4, 1],
            },
            'Age': {
                'hh': results_df.iloc[5, 0],
                'p': results_df.iloc[5, 1],
            }
        }
        # 卡方检验
        categorical_columns = ['Device Model', 'Operating System', 'Gender']
        chi2_results = {}

        for col in categorical_columns:
            contingency_table = pd.crosstab(data[col], data['User Behavior Class'])
            chi2, p_value, dof, expected = chi2_contingency(contingency_table)
            chi2_results[col] = {
                'chi2': chi2,
                'p-value': p_value,
                'dof': dof
            }
        results_df = pd.DataFrame(chi2_results).T
        kafang = {
            'Device': {
                'chi2': results_df.iloc[0, 0],
                'p': results_df.iloc[0, 1],
                'dof': results_df.iloc[0, 2],
            },
            'Operating': {
                'chi2': results_df.iloc[1, 0],
                'p': results_df.iloc[1, 1],
                'dof': results_df.iloc[1, 2],
            },
            'Gender': {
                'chi2': results_df.iloc[2, 0],
                'p': results_df.iloc[2, 1],
                'dof': results_df.iloc[2, 2],
            }
        }
        return Kruskal_Wallis_H, kafang

    # 根据之前的分析，剔除不显著特征，只保留显著特征，这里采用随机森林模型，不需要处理多重共线性的情况，然后划分数据集。
    def rf_data_yuce(self):
        data_path = str(settings.BASE_DIR) + '/dataset.csv'
        data = pd.read_csv(data_path)
        # 选择显著特征
        features = [
            'App Usage Time (min/day)',
            'Screen On Time (hours/day)',
            'Battery Drain (mAh/day)',
            'Number of Apps Installed',
            'Data Usage (MB/day)'
        ]
        x = data[features]
        y = data['User Behavior Class']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=15)
        # 建立回归模型
        rf_model = RandomForestRegressor(random_state=15)
        rf_model.fit(x_train, y_train)
        # 预测并转换为类别
        y_pred_rf = rf_model.predict(x_test)
        y_pred_rf_class = np.round(y_pred_rf)
        class_report_rf = classification_report(y_test, y_pred_rf_class)

        # 预测每日移动数据消耗量
        data_path = str(settings.BASE_DIR) + '/dataset.csv'
        data = pd.read_csv(data_path)
        features = [
            'App Usage Time (min/day)',
            'Screen On Time (hours/day)',
            'Battery Drain (mAh/day)',
            'Number of Apps Installed'
        ]
        x = data[features]
        y = data['Data Usage (MB/day)']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=15)
        rf_data_usage = RandomForestRegressor(random_state=15)
        rf_data_usage.fit(x_train, y_train)
        y_pred_rf_data_usage = rf_data_usage.predict(x_test)
        y_pred_rf = '模型评估指标：\n'
        t = f'R2 score: {r2_score(y_test, y_pred_rf_data_usage):.4f}\n' \
            f'MSE: {mean_squared_error(y_test, y_pred_rf_data_usage):.4f}\n' \
            f'RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_rf_data_usage)):.4f}\n' \
            f'MAE: {mean_absolute_error(y_test, y_pred_rf_data_usage):.4f}\n'
        y_pred_rf = y_pred_rf + t
        return class_report_rf, y_pred_rf
