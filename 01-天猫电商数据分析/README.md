# 天猫电商数据分析项目

## 项目简介
基于天猫平台约5万条商品数据（2024年1月-11月），分析品类销售、价格策略、促销效果与补贴ROI。

## 技术栈
- Python 3.x
- Pandas / NumPy
- Matplotlib / Seaborn
- MySQL / SQLAlchemy
- tabulate

## 项目结构
```
天猫电商项目/
├── analysis.py              # 主分析代码（整合优化版v2.0）
├── Tools/
│   └── DF_Tools.py          # 工具模块（已整合到主代码中）
├── 天猫数据_1月到11月.xlsx   # 原始数据
├── 分析结果汇总.xlsx         # 分析结果输出
├── analysis_dashboard.png    # 可视化看板
├── 电商分析.pbix            # Power BI文件
├── .gitignore               # Git忽略配置
└── README.md                # 项目说明
```

## 功能特性

### 1. 数据清洗
- 处理"万+"格式销量数据
- 价格字段标准化转换
- 计算真实折扣率

### 2. 统计分析
- 品类指标分析（销量排名、平均售价、补贴金额）
- 价格区间分析（6档价格带分布）
- 折扣策略分析（5档折扣区间+相关性分析）
- 补贴效果分析（品类补贴ROI评估）
- 爆款商品特征分析（TOP20%高销量商品对比）

### 3. 可视化分析
- 品类销量TOP10柱状图
- 价格带销量占比饼图
- 折扣率分布直方图
- 价格-销量关系散点图
- 品类平均折扣率对比
- 补贴-销量关系散点图

### 4. 数据导出
- MySQL数据库导出（支持5张分析表）
- Excel文件导出（备选方案）

## 运行方式

```bash
# 安装依赖
pip install pandas numpy matplotlib seaborn sqlalchemy pymysql tabulate openpyxl

# 运行分析
python analysis.py
```

## 配置说明

代码中的`Config`类包含可配置参数：
- `INPUT_FILE`: 输入数据文件路径
- `OUTPUT_FILE`: Excel输出路径
- `DB_CONFIG`: MySQL数据库连接配置
- `PRICE_BINS`: 价格区间分箱配置
- `DISCOUNT_BINS`: 折扣区间分箱配置

## 分析报告输出

运行后自动生成：
1. 控制台输出详细分析结果
2. 可视化看板图片（analysis_dashboard.png）
3. Excel分析报告（分析结果汇总.xlsx）
4. MySQL数据库表（如配置正确）

## 作者
赵哲弘 - 北华大学大数据专业

## 版本历史
- v2.0: 整合优化版，启用可视化功能
- v1.0: 初始版本