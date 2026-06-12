# - 定义：统计周期内，商品销售数量与平均库存的比值，反映库存周转效率（“卖得快还是积压”）。
# - 核心作用：优化库存结构，避免 “滞销积压”（占用资金）或 “畅销缺货”（损失营收），降低仓储成本。
# - 计算逻辑：
# 数据来源：product_detail（库存）+ order_detail（销量）
# 公式：库存周转率 = 统计周期内销售数量 / 平均库存（平均库存 =（期初库存 + 期末库存）/2）
# 涉及字段：
#   - order_detail.purchase_quantity（销售数量，需扣除退货：purchase_quantity - return_quantity）；
#   - product_detail.stock_quantity（期初 / 期末库存，需按周期快照统计）。
# - 结果字段示例：
#   - 商品分类：女装
#   - 统计周期：2025 年 6 月
#   - 销售数量：8,000 件
#   - 期初库存：5,000 件，期末库存：3,000 件
#   - 平均库存：4,000 件
#   - 库存周转率：2 次 / 月（即 24 次 / 年）
# - 理想结果：
#   - 快消品（如女装、日用品）：≥12 次 / 年（每月 1 次）；
#   - 耐用品（如家电、数码）：≥4 次 / 年（每季度 1 次）。
#   - 无分类周转率＜3 次 / 年（避免积压风险）。
# - 业务解读：
#   - 若周转率＜3 次 / 年（如家电 2 次 / 年）：通过折扣清仓（如 “季末 5 折”）、捆绑销售（如 “买冰箱送微波炉”）消化库存。
#   - 若周转率＞20 次 / 年（如女装 24 次 / 年）：需警惕缺货风险，增加备货量（如按销量的 1.2 倍备货）。
select
    pc.category_id,
    sum(pd.sales_count) as total_sales,
    avg(pd.stock_quantity) as avg_stock,
    round(sum(pd.sales_count)/avg(pd.stock_quantity),2) as inventory_turnover
from product_detail pd
join product_category pc
on pd.category_id = pc.category_id
group by pc.category_id
order by inventory_turnover desc