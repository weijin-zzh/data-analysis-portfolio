# - 定义：统计当日新增用户中，在次日（注册日 + 1 天）再次登录的用户比例，反映新用户对产品的初期接受度。
# - 核心作用：评估新用户体验（如注册流程、首屏引导、核心功能），是产品优化的关键指标（留存率低意味着用户流失风险高）。
# - 计算逻辑：
# 公式：次日留存率 = （次日登录的新增用户数 / 当日新增用户数）× 100%
# 涉及字段：user_id、register_time（用于筛选当日新增）、last_login_time（用于判断次日登录）。
# - 结果字段示例：
#   - 统计日期：2025-06-15
#   - 当日新增用户数：1,000 人
#   - 次日登录用户数：280 人
#   - 次日留存率：28%
# - 理想结果：
#   - 整体留存率≥20%（电商行业均值），且高价值渠道（如抖音）的新用户留存率≥25%。
#   - 留存率随用户分层提升：付费用户次日留存≥35%，未付费用户≥15%。
# - 业务解读：
#   - 若留存率＜15%，需优化新用户引导（如简化首单流程、赠送新人券），或排查产品是否存在 “注册后无明确操作路径” 的问题（如首页杂乱无重点）
select  DATE(register_time) from user_master;
WITH daily_new_users AS (
SELECT
        DATE(register_time) AS register_date,COUNT(DISTINCT user_id) AS new_user_count
    FROM user_master
    WHERE register_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE()
    GROUP BY DATE(register_time)
    ),
retained_users AS (SELECT
        DATE(u.register_time) AS register_date,COUNT(DISTINCT u.user_id) AS retained_count
    FROM user_master u
    WHERE
        u.register_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE()AND u.last_login_time >= DATE_ADD(DATE(u.register_time), INTERVAL 1 DAY)
        GROUP BY DATE(u.register_time)
        )
        SELECT
    d.register_date,
    d.new_user_count,
    r.retained_count,ROUND(r.retained_count / d.new_user_count * 100, 2) AS retention_rate
FROM daily_new_users d
LEFT JOIN retained_users r ON d.register_date = r.register_date;