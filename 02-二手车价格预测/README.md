# 二手车价格预测与影响因素分析

## 项目简介
基于约9000条二手车交易数据（燃油车+新能源车），挖掘价格驱动因素并构建预测模型。

## 技术栈
- Python 3.x
- Pandas / NumPy
- Scikit-learn (LinearRegression, RandomForest, LabelEncoder, TF-IDF)
- Matplotlib / Seaborn

## 项目结构
```
第一组结课设计/
├── data/
│   ├── 新能源.csv           # 新能源车数据
│   └── 汽油.csv             # 燃油车数据
├── 代码/
│   └── Untitled2.ipynb      # Jupyter分析代码
├── ppt/
│   └── 二手车价格预测分析系统.pptx
├── 报告/
│   └── 第1组结课设计+二手车交易价格分析.docx
└── 参考文献/
    └── (3个PDF参考文献)
```

## 分析内容
1. 数据清洗：处理"暂无报价"、单位文本等特殊值
2. 特征工程：车龄计算、品牌/城市编码、TF-IDF文本特征提取
3. 可视化分析：价格分布、相关性热力图、车龄vs价格散点图
4. 模型构建：线性回归模型训练与评估（燃油车R²=0.57，新能源车R²=0.86）

## 运行方式
```bash
jupyter notebook 代码/Untitled2.ipynb
```

## 作者
赵哲弘 - 北华大学大数据专业