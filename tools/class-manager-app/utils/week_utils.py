"""
周数计算工具 / Week calculation utilities
"""

from datetime import datetime, timedelta


# 第一周的开始日期 / Start date of week 1
WEEK_ONE_START = datetime(2025, 11, 13)


def get_current_week() -> int:
    """
    获取当前是第几周（基于2025年11月13日为第一周）
    / Get current week number (based on Nov 13, 2025 as week 1)
    
    Returns:
        当前周数 / Current week number
    """
    today = datetime.now()
    delta = today - WEEK_ONE_START
    
    # 计算相差的天数，然后除以7得到周数
    # Calculate days difference, then divide by 7 to get week number
    weeks_passed = delta.days // 7
    
    # 如果还没到第一周的开始日期，返回0
    # If before week 1 start date, return 0
    if weeks_passed < 0:
        return 0
    
    # 返回当前周数（从1开始）
    # Return current week number (starting from 1)
    return weeks_passed + 1


def get_week_date_range(week_num: int) -> tuple:
    """
    获取指定周的日期范围
    / Get date range for a specific week
    
    Args:
        week_num: 周数 / Week number
        
    Returns:
        (start_date, end_date) 元组 / Tuple of start and end dates
    """
    if week_num < 1:
        return None, None
    
    # 计算该周的开始日期
    # Calculate start date of the week
    start_date = WEEK_ONE_START + timedelta(weeks=week_num - 1)
    end_date = start_date + timedelta(days=6)
    
    return start_date, end_date


def format_week_label(week_num: int) -> str:
    """
    格式化周标签显示
    / Format week label for display
    
    Args:
        week_num: 周数 / Week number
        
    Returns:
        格式化的周标签 / Formatted week label
    """
    start_date, end_date = get_week_date_range(week_num)
    if start_date is None:
        return f"第{week_num}周"
    
    return f"第{week_num}周\n({start_date.strftime('%m/%d')}-{end_date.strftime('%m/%d')})"
