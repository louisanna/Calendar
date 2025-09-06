from datetime import datetime, timedelta
import calendar

def calculate_years_months_days(n, birth_date):
    """
    计算从出生日(2024-11-15)起第n天的年月日表示
    n=0: 2024-11-15 -> 0年0月0天
    月份计算：自然月方式（例如11月15日到12月15日为1个月）
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
        last_anniversary = datetime(current_date.year - 1, birth_date.month, birth_date.day)
    else:
        last_anniversary = datetime(current_date.year, birth_date.month, birth_date.day)
    
    # 计算月份
    months = 0
    temp_date = last_anniversary
    while True:
        # 计算下个月的同一天
        if temp_date.month == 12:
            next_month = 1
            next_year = temp_date.year + 1
        else:
            next_month = temp_date.month + 1
            next_year = temp_date.year
        
        # 处理月末情况（如1月30日到2月）
        try:
            next_date = datetime(next_year, next_month, birth_date.day)
        except ValueError:
            # 当目标日期无效时（如2月30日），使用该月最后一天
            _, last_day = calendar.monthrange(next_year, next_month)
            next_date = datetime(next_year, next_month, last_day)
        
        if next_date > current_date:
            break
            
        months += 1
        temp_date = next_date
    
    # 计算天数
    days = (current_date - temp_date).days
    
    return years, months, days

# 出生日期
birth_date = datetime(2024, 11, 15)
# 结束日期
end_date = datetime(2124, 11, 15)
# 总天数（包含起始日）
total_days = (end_date - birth_date).days
total_events = total_days + 1  # 包含第0天

with open('baby_calendar.ics', 'w', encoding='utf-8') as f:
    # 文件头
    f.write("BEGIN:VCALENDAR\n")
    f.write("VERSION:2.0\n")
    f.write("PRODID:-//BabyDays Calendar//EN\n")
    f.write("CALSCALE:GREGORIAN\n")
    f.write("METHOD:PUBLISH\n")
    f.write("X-WR-CALNAME:小宝成长日记\n")
    f.write("X-WR-TIMEZONE:Asia/Shanghai\n\n")
    
    # 生成每一天的事件
    for n in range(0, total_events):
        current_date = birth_date + timedelta(days=n)
        years, months, days = calculate_years_months_days(n, birth_date)
        
        # 特殊日期标记
        description = ""
        if n == 0: 
            description = "DESCRIPTION:出生日"
        elif n == 30: 
            description = "DESCRIPTION:满月"
        elif n == 365: 
            description = "DESCRIPTION:周岁"
        
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

print(f"已生成100年日历文件: 小宝成长日历.ics (共{total_events}天)")