from datetime import datetime, timedelta
import calendar

def calculate_years_months_days(n):
    """
    计算从出生日(2024-11-15)起第n天的年月日表示
    n=0: 2024-11-15 -> 0年0月0天
    """
    if n == 0:
        return 0, 0, 0
    
    birth_date = datetime(2024, 11, 15)
    current_date = birth_date + timedelta(days=n)
    
    # 计算年份
    years = current_date.year - birth_date.year
    
    # 调整年份（如果还没到周年日）
    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        years -= 1
    
    # 计算周年日
    if years > 0:
        anniversary = birth_date.replace(year=birth_date.year + years)
    else:
        anniversary = birth_date
    
    # 计算月份
    months = 0
    temp_date = anniversary
    while temp_date < current_date:
        # 计算下个月的同一天
        next_month = temp_date.month + 1
        next_year = temp_date.year
        if next_month > 12:
            next_month = 1
            next_year += 1
        
        try:
            next_date = temp_date.replace(year=next_year, month=next_month)
        except ValueError:
            # 处理无效日期（如2月30日）
            next_date = temp_date.replace(day=1) + timedelta(days=32)
            next_date = next_date.replace(day=1) - timedelta(days=1)
        
        if next_date > current_date:
            break
            
        months += 1
        temp_date = next_date
    
    # 计算天数
    days = (current_date - temp_date).days
    
    return years, months, days

# 计算100年的总天数 (2024-11-15 到 2124-11-15)
start_date = datetime(2024, 11, 15)
end_date = datetime(2124, 11, 15)
total_days = (end_date - start_date).days  # 36525天
total_events = total_days + 1  # 包含起始日

with open('GrowthCalendar2.ics', 'w', encoding='utf-8') as f:
    # 文件头
    f.write("BEGIN:VCALENDAR\n")
    f.write("VERSION:2.0\n")
    f.write("PRODID:-//BabyDays Calendar//EN\n")
    f.write("CALSCALE:GREGORIAN\n")
    f.write("METHOD:PUBLISH\n")
    f.write("X-WR-CALNAME:小宝の成长日记🍼\n")
    f.write("X-WR-TIMEZONE:Asia/Shanghai\n\n")
    
    # 生成每一天的事件
    for n in range(0, total_events):
        current_date = start_date + timedelta(days=n)
        years, months, days = calculate_years_months_days(n)
        
        # 特殊日期标记
        description = ""
        if n == 0: 
            description = "DESCRIPTION:出生日🍼"
        elif n == 30: 
            description = "DESCRIPTION:满月🍼"
        elif n == 365: 
            description = "DESCRIPTION:周岁🍼"
        elif years == 18 and months == 0 and days == 0: 
            description = "DESCRIPTION:成人礼"
        
        # 写入事件
        f.write("BEGIN:VEVENT\n")
        f.write(f"UID:babydays-{n}@example.com\n")
        f.write("DTSTAMP:20240807T000000Z\n")
        f.write(f"DTSTART;VALUE=DATE:{current_date.strftime('%Y%m%d')}\n")
        f.write(f"DTEND;VALUE=DATE:{(current_date + timedelta(days=1)).strftime('%Y%m%d')}\n")
        f.write(f"SUMMARY:小宝出生第{years}年{months}月{days}天🍼\n")
        if description: 
            f.write(f"{description}\n")
        f.write("END:VEVENT\n\n")
    
    # 文件尾
    f.write("END:VCALENDAR")

print(f"已生成100年日历文件: GrowthCalendar2.ics (共{total_events}天)")
