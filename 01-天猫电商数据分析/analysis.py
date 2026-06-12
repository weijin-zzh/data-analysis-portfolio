"""
天猫电商数据分析项目
作者：赵哲弘
日期：2026年
版本：v2.0 - 整合优化版

项目概述：
基于天猫平台约5万条商品数据，分析品类销售、价格策略、促销效果与补贴ROI
技术栈：Python、Pandas、NumPy、Matplotlib、MySQL、SQLAlchemy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sqlalchemy import create_engine
import pymysql
import os

# 全局设置
warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 获取当前脚本所在目录（支持项目移动）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==================== 配置参数 ====================
class Config:
    # 使用相对路径，项目移动后自动适应
    INPUT_FILE = os.path.join(BASE_DIR, '天猫数据_1月到11月.xlsx')
    OUTPUT_FILE = os.path.join(BASE_DIR, '分析结果汇总.xlsx')
    DASHBOARD_FILE = os.path.join(BASE_DIR, 'analysis_dashboard.png')
    DB_CONFIG = 'mysql+pymysql://root:123456@localhost:3306/tmall_analysis?charset=utf8mb4'
    
    # 价格区间配置
    PRICE_BINS = [0, 50, 100, 200, 500, 1000, float('inf')]
    PRICE_LABELS = ['0-50元', '50-100元', '100-200元', '200-500元', '500-1000元', '1000元以上']
    
    # 折扣区间配置
    DISCOUNT_BINS = [0, 0.7, 0.8, 0.9, 1.0, 1.1]
    DISCOUNT_LABELS = ['7折以下', '7-8折', '8-9折', '9-10折', '原价或更高']

# ==================== 数据读取 ====================
def load_data(file_path):
    """加载并预览数据"""
    df = pd.read_excel(file_path)
    print(f"✓ 数据加载完成，共 {len(df):,} 条记录，{len(df.columns)} 个字段")
    return df

# ==================== 数据清洗 ====================
def clean_data(df):
    """数据清洗主函数"""
    # 清洗销量数据（处理"万+"格式）
    def clean_sales(s):
        s = s.astype(str).str.replace('+', '', regex=False)
        is_wan = s.str.contains('万')
        s = s.str.replace('万', '', regex=False)
        s = pd.to_numeric(s, errors='coerce').fillna(0)
        return np.where(is_wan, s * 10000, s)
    
    df['年销量_clean'] = clean_sales(df['年销量'])
    
    # 清洗价格字段
    price_cols = ['原价', '折后价', '最终促销价', '预估凑单价']
    for col in price_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算真实折扣率
    df['真实折扣率'] = (df['最终促销价'] / df['原价']).round(2)
    df['真实折扣率'] = df['真实折扣率'].apply(lambda x: x if 0 < x <= 1 else np.nan)
    
    return df

# ==================== 特征工程 ====================
def feature_engineering(df):
    """特征工程：创建衍生指标"""
    # 添加价格区间
    df['价格区间'] = pd.cut(df['最终促销价'], bins=Config.PRICE_BINS, 
                          labels=Config.PRICE_LABELS, right=False)
    
    # 添加折扣区间
    df['折扣区间'] = pd.cut(df['真实折扣率'], bins=Config.DISCOUNT_BINS, 
                          labels=Config.DISCOUNT_LABELS, right=False)
    
    return df

# ==================== 统计分析 ====================
def category_analysis(df):
    """品类指标分析"""
    category_metrics = df.groupby('所属品类', as_index=False).agg({
        '年销量_clean': ['sum', 'mean'],
        '最终促销价': 'mean',
        '原价': 'mean',
        '补贴金额': ['sum', 'mean'],
        '商品标题': 'count'
    }).round(2)
    
    category_metrics.columns = [
        '品类', '总销量', '平均单品销量',
        '平均最终售价', '平均原价',
        '总补贴金额', '平均单品补贴', '商品总数'
    ]
    
    category_metrics = category_metrics.sort_values(by='总销量', ascending=False)
    category_metrics['rank'] = category_metrics['总销量'].rank(ascending=False).astype(int)
    
    print("\n===== 品类指标分析 =====")
    display_df(category_metrics)
    
    return category_metrics

def price_band_analysis(df):
    """价格区间分析"""
    price_band_stats = df.groupby('价格区间', observed=False).agg({
        '年销量_clean': ['sum', 'mean', 'count'],
        '最终促销价': 'mean',
        '真实折扣率': 'mean',
        '补贴金额': 'mean'
    }).round(2)
    
    price_band_stats.columns = ['总销量', '平均单品销量', '商品数量', '平均售价', '平均折扣率', '平均补贴']
    price_band_stats = price_band_stats.reset_index()
    total_sales = price_band_stats['总销量'].sum()
    price_band_stats['销量占比'] = (price_band_stats['总销量'] / total_sales * 100).round(2)
    
    print("\n===== 价格区间分析 =====")
    display_df(price_band_stats)
    
    return price_band_stats

def discount_analysis(df):
    """折扣策略分析"""
    discount_stats = df.groupby('折扣区间', observed=False).agg({
        '年销量_clean': ['sum', 'mean'],
        '商品标题': 'count',
        '最终促销价': 'mean',
        '补贴金额': 'mean'
    }).round(2)
    
    discount_stats.columns = ['总销量', '平均销量', '商品数', '平均售价', '平均补贴']
    discount_stats = discount_stats.reset_index()
    
    print("\n===== 折扣策略分析 =====")
    display_df(discount_stats)
    
    # 计算相关性
    valid_data = df[df['真实折扣率'].notna()]
    correlation = valid_data['真实折扣率'].corr(valid_data['年销量_clean'])
    print(f"\n折扣率与销量相关系数: {correlation:.4f}")
    
    return discount_stats, correlation

def subsidy_analysis(df):
    """补贴效果分析"""
    subsidy_by_category = df.groupby('所属品类').agg({
        '补贴金额': ['sum', 'mean'],
        '年销量_clean': ['sum', 'mean'],
        '最终促销价': 'mean',
        '商品标题': 'count'
    }).round(2)
    
    subsidy_by_category.columns = ['总补贴', '平均补贴', '总销量', '平均销量', '平均售价', '商品数']
    subsidy_by_category['单位补贴销量'] = (subsidy_by_category['总销量'] / subsidy_by_category['总补贴']).round(2)
    subsidy_by_category = subsidy_by_category.sort_values(by='总销量', ascending=False)
    
    print("\n===== 补贴效果分析 =====")
    display_df(subsidy_by_category.head(20))
    
    # 明星商品识别
    high_subsidy = df['补贴金额'].quantile(0.8)
    high_sales = df['年销量_clean'].quantile(0.8)
    star_products = df[(df['补贴金额'] >= high_subsidy) & (df['年销量_clean'] >= high_sales)]
    print(f"\n明星商品数量: {len(star_products)}")
    
    return subsidy_by_category

def bestseller_analysis(df):
    """爆款商品特征分析"""
    threshold = df['年销量_clean'].quantile(0.8)
    best_sellers = df[df['年销量_clean'] >= threshold].copy()
    others = df[df['年销量_clean'] < threshold].copy()
    
    print(f"\n===== 爆款商品特征分析 =====")
    print(f"爆款阈值（前20%）: {threshold:.0f} 件")
    print(f"爆款商品数量: {len(best_sellers)}")
    
    comparison = pd.DataFrame({
        '指标': ['平均售价', '平均折扣率', '平均补贴', '平均原价'],
        '爆款商品': [
            best_sellers['最终促销价'].mean(),
            best_sellers['真实折扣率'].mean(),
            best_sellers['补贴金额'].mean(),
            best_sellers['原价'].mean()
        ],
        '普通商品': [
            others['最终促销价'].mean(),
            others['真实折扣率'].mean(),
            others['补贴金额'].mean(),
            others['原价'].mean()
        ]
    })
    comparison['差异(%)'] = ((comparison['爆款商品'] - comparison['普通商品']) / comparison['普通商品'] * 100).round(2)
    
    print("\n爆款 vs 普通商品对比:")
    display_df(comparison)
    
    return best_sellers, comparison

# ==================== 可视化分析 ====================
def create_visualizations(df, category_metrics, price_band_result):
    """创建多维度可视化图表"""
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('天猫电商数据分析看板', fontsize=16, fontweight='bold')
    
    # 1. 品类销量TOP10
    top10 = category_metrics.head(10)
    axes[0, 0].barh(range(len(top10)), top10['总销量'], color='#2ecc71')
    axes[0, 0].set_yticks(range(len(top10)))
    axes[0, 0].set_yticklabels(top10['品类'])
    axes[0, 0].set_xlabel('总销量')
    axes[0, 0].set_title('品类销量TOP10')
    axes[0, 0].invert_yaxis()
    
    # 2. 价格区间分布
    axes[0, 1].pie(price_band_result['销量占比'], labels=price_band_result['价格区间'], autopct='%1.1f%%')
    axes[0, 1].set_title('各价格带销量占比')
    
    # 3. 折扣率分布
    valid_discount = df[df['真实折扣率'].notna()]['真实折扣率']
    axes[0, 2].hist(valid_discount, bins=30, color='#3498db', edgecolor='black', alpha=0.7)
    axes[0, 2].set_xlabel('折扣率')
    axes[0, 2].set_ylabel('商品数量')
    axes[0, 2].set_title('折扣率分布')
    axes[0, 2].axvline(x=valid_discount.mean(), color='red', linestyle='--', label=f'均值: {valid_discount.mean():.2f}')
    axes[0, 2].legend()
    
    # 4. 价格-销量关系
    sample = df.sample(min(500, len(df)))
    scatter = axes[1, 0].scatter(sample['最终促销价'], sample['年销量_clean'],
                                 alpha=0.5, c=sample['真实折扣率'], cmap='viridis')
    axes[1, 0].set_xlabel('最终促销价')
    axes[1, 0].set_ylabel('年销量')
    axes[1, 0].set_title('价格-销量关系')
    plt.colorbar(scatter, ax=axes[1, 0], label='折扣率')
    
    # 5. 品类平均折扣率TOP10
    cat_discount = df.groupby('所属品类')['真实折扣率'].mean().sort_values(ascending=True).head(10)
    axes[1, 1].barh(range(len(cat_discount)), cat_discount.values, color='#e74c3c')
    axes[1, 1].set_yticks(range(len(cat_discount)))
    axes[1, 1].set_yticklabels(cat_discount.index)
    axes[1, 1].set_xlabel('平均折扣率')
    axes[1, 1].set_title('品类平均折扣率TOP10')
    axes[1, 1].invert_yaxis()
    
    # 6. 补贴-销量关系
    sample_subsidy = df[df['补贴金额'] > 0].sample(min(500, len(df[df['补贴金额'] > 0])))
    axes[1, 2].scatter(sample_subsidy['补贴金额'], sample_subsidy['年销量_clean'],
                       alpha=0.5, color='#9b59b6')
    axes[1, 2].set_xlabel('补贴金额')
    axes[1, 2].set_ylabel('年销量')
    axes[1, 2].set_title('补贴-销量关系')
    
    plt.tight_layout()
    plt.savefig(Config.DASHBOARD_FILE, dpi=300, bbox_inches='tight')
    print("\n✓ 可视化看板已保存")
    plt.show()

# ==================== 数据导出 ====================
def export_results(df, category_metrics, price_band_result, discount_result, subsidy_result):
    """导出分析结果"""
    try:
        engine = create_engine(Config.DB_CONFIG)
        df.to_sql('raw_data_cleaned', engine, if_exists='replace', index=False, chunksize=1000)
        category_metrics.to_sql('category_metrics', engine, if_exists='replace', index=False)
        price_band_result.to_sql('price_band_analysis', engine, if_exists='replace', index=False)
        discount_result.to_sql('discount_analysis', engine, if_exists='replace', index=False)
        subsidy_result.to_sql('subsidy_analysis', engine, if_exists='replace', index=False)
        print("\n✓ 分析结果已导出到数据库")
    except Exception as e:
        print(f"\n数据库导出失败: {e}")
        with pd.ExcelWriter(Config.OUTPUT_FILE, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='清洗后数据', index=False)
            category_metrics.to_excel(writer, sheet_name='品类指标', index=False)
            price_band_result.to_excel(writer, sheet_name='价格区间分析', index=False)
            discount_result.to_excel(writer, sheet_name='折扣分析', index=False)
            subsidy_result.to_excel(writer, sheet_name='补贴分析', index=False)
        print(f"✓ 分析结果已导出到Excel: {Config.OUTPUT_FILE}")

# ==================== 报告生成 ====================
def generate_report(df, category_metrics, price_band_result, bestseller_comparison, discount_corr):
    """生成分析总结报告"""
    print("\n" + "=" * 60)
    print("           天猫电商数据分析总结报告")
    print("=" * 60)
    
    print("\n【一、整体概况】")
    print(f"• 数据总量: {len(df):,} 条商品记录")
    print(f"• 涉及品类: {df['所属品类'].nunique()} 个")
    print(f"• 总销量: {df['年销量_clean'].sum():,.0f} 件")
    print(f"• 平均售价: ¥{df['最终促销价'].mean():.2f}")
    print(f"• 平均折扣率: {df['真实折扣率'].mean():.2%}")
    
    print("\n【二、核心发现】")
    top_category = category_metrics.iloc[0]
    print(f"1. 销冠品类: {top_category['品类']} (总销量: {top_category['总销量']:,.0f})")
    
    dominant_band = price_band_result.loc[price_band_result['销量占比'].idxmax()]
    print(f"2. 主力价格带: {dominant_band['价格区间']} (占比: {dominant_band['销量占比']:.2f}%)")
    
    effect = '显著负相关，降价促销有效' if discount_corr < -0.1 else '相关性较弱'
    print(f"3. 折扣效应: 相关系数={discount_corr:.4f}，{effect}")
    
    price_diff = bestseller_comparison.loc[0, '差异(%)']
    print(f"4. 爆款特征: 平均售价比普通商品{price_diff:+.2f}%")
    
    print("\n【三、策略建议】")
    print("1. 定价策略: 重点关注主力价格带，适当布局高利润区间")
    print("2. 促销策略: 合理控制折扣力度在最优区间，避免过度让利")
    print("3. 补贴优化: 向高转化品类倾斜补贴预算，提升ROI")
    print("4. 选品方向: 参考爆款商品特征，优先开发相似属性产品")
    
    print("\n" + "=" * 60)

# ==================== 辅助工具 ====================
def display_df(df, max_rows=20):
    """美化显示DataFrame"""
    from tabulate import tabulate
    display_df = df.head(max_rows) if len(df) > max_rows else df
    print(tabulate(display_df, headers='keys', tablefmt='psql', showindex=False))

# ==================== 主函数 ====================
def main():
    """主执行函数"""
    print("=" * 60)
    print("     天猫电商数据分析项目 v2.0")
    print("=" * 60)
    
    # 1. 数据加载
    df = load_data(Config.INPUT_FILE)
    
    # 2. 数据清洗与特征工程
    df = clean_data(df)
    df = feature_engineering(df)
    
    # 3. 统计分析
    category_metrics = category_analysis(df)
    price_band_result = price_band_analysis(df)
    discount_result, discount_corr = discount_analysis(df)
    subsidy_result = subsidy_analysis(df)
    bestsellers, bestseller_comparison = bestseller_analysis(df)
    
    # 4. 可视化分析
    create_visualizations(df, category_metrics, price_band_result)
    
    # 5. 数据导出
    export_results(df, category_metrics, price_band_result, discount_result, subsidy_result)
    
    # 6. 生成报告
    generate_report(df, category_metrics, price_band_result, bestseller_comparison, discount_corr)
    
    print("\n✅ 数据分析项目完成！")

if __name__ == '__main__':
    main()