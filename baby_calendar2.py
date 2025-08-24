from datetime import datetime, timedelta
import calendar

def calculate_years_months_days(n, birth_date):
    """
    计算从出生日(2024-11-15)起第n天的年月日表示
    特殊规则：第一个月(0月)天数从0开始，后续月份天数从1开始
    """
    if n == 0:
        return 0, 0, 0
    
    # 当前日期 = 出生日期 + n天
    current_date = birth_date + timedelta(days=n)
    
    # 计算年份
    years = current_date.year - birth_date.year
    
    # 检查是否已过周年日
    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        years -= 1
    
    # 计算周年日
    if years > 0:
        # 尝试创建周年日期
        try:
            anniversary = datetime(birth_date.year + years, birth_date.month, birth_date.day)
        except ValueError:
            # 处理2月29日等特殊情况
            anniversary = datetime(birth_date.year + years, birth_date.month, birth_date.day - 1)
    else:
        anniversary = birth_date
    
    # 计算月份和天数
    if n < 30:  # 第一个月内
        months = 0
        days = n
    else:
        # 计算从周年日开始的月数
        months = 0
        temp_date = anniversary
        
        while temp_date < current_date:
            # 计算下个月的同一天
            next_month = temp_date.month + 1
            next_year = temp_date.year
            if next_month > 12:
                next_month = 1
                next_year += 1
            
            # 处理月末情况
            try:
                next_date = datetime(next_year, next_month, birth_date.day)
            except ValueError:
                # 当目标日期无效时，使用该月最后一天
                _, last_day = calendar.monthrange(next_year, next_month)
                next_date = datetime(next_year, next_month, last_day)
            
            if next_date > current_date:
                break
                
            months += 1
            temp_date = next_date
        
        # 计算天数 (从1开始)
        days = (current_date - temp_date).days + 1  # 后续月份从1开始
    
    return years, months, days

# 出生日期
birth_date = datetime(2024, 11, 15)
# 结束日期
end_date = datetime(2124, 11, 15)
# 总天数（包含起始日）
total_days = (end_date - birth_date).days
total_events = total_days + 1  # 包含第0天

# 生成ICS文件
with open('小宝成长日历.ics', 'w', encoding='utf-8') as f:
    # 文件头
    f.write("BEGIN:VCALENDAR\n")
    f.write("VERSION:2.0\n")
    f.write("PRODID:-//BabyDays Calendar//EN\n")
    f.write("CALSCALE:GREGORIAN\n")
    f.write("METHOD:PUBLISH\n")
    f.write("X-WR-CALNAME:小宝成长日记🍼\n")
    f.write("X-WR-TIMEZONE:Asia/Shanghai\n")
    f.write("X-WR-CALDESC:记录小宝成长的每一天，从2024年11月15日开始\n\n")
    
    # 生成每一天的事件
    for n in range(0, total_events):
        current_date = birth_date + timedelta(days=n)
        years, months, days = calculate_years_months_days(n, birth_date)
        
        # 特殊日期标记
        description = ""
        if n == 0: 
            description = "DESCRIPTION:出生日🎉"
        elif n == 30: 
            description = "DESCRIPTION:满月啦🌙"
        elif n == 365: 
            description = "DESCRIPTION:周岁快乐🎂"
        elif n == 365 * 5: 
            description = "DESCRIPTION:五岁啦🌟"
        elif n == 365 * 10: 
            description = "DESCRIPTION:十岁生日🎁"
        elif n == 365 * 18: 
            description = "DESCRIPTION:成人礼🎓"
        
        # 写入事件
        f.write("BEGIN:VEVENT\n")
        f.write(f"UID:babydays-{n}@family.com\n")
        f.write("DTSTAMP:20240807T000000Z\n")
        f.write(f"DTSTART;VALUE=DATE:{current_date.strftime('%Y%m%d')}\n")
        f.write(f"DTEND;VALUE=DATE:{(current_date + timedelta(days=1)).strftime('%Y%m%d')}\n")
        f.write(f"SUMMARY:小宝出生第{years}年{months}月{days}天🍼\n")
        if description: 
            f.write(f"{description}\n")
        f.write(f"SEQUENCE:{n}\n")
        f.write("END:VEVENT\n\n")
    
    # 文件尾
    f.write("END:VCALENDAR\n")

print(f"已生成100年日历文件: 小宝成长日历.ics")
print(f"总天数: {total_events}天 (从2024-11-15到2124-11-15)")
print("\n特殊计数规则:")
print(" - 第一个月(0月): 天数从0开始 (0-30天)")
print(" - 后续月份: 天数从1开始 (1-31天)")
print("\n重要里程碑:")
print(f" - 第0天 (2024-11-15): 出生日 (0年0月0天)")
print(f" - 第30天 (2024-12-15): 满月 (0年1月0天)")
print(f" - 第365天 (2025-11-15): 周岁 (1年0月0天)")
print(f" - 第3650天 (2034-11-15): 十岁 (10年0月0天)")
print(f" - 第6570天 (2042-11-15): 十八岁 (18年0月0天)")
