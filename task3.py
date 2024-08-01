import sys
import os


def parse_log_line(line):
    parts = line.split(' ', 3)
    if len(parts) != 4:
        return None
    date, time, level, message = parts
    return {'date': date, 'time': time, 'level': level, 'message': message.strip()}

def load_logs(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не знайдено.")
    
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            log_entry = parse_log_line(line)
            if log_entry:
                logs.append(log_entry)
    return logs

def filter_logs_by_level(logs, level):
    return [log for log in logs if log['level'].upper() == level.upper()]

def count_logs_by_level(logs):
    levels = ['INFO', 'ERROR', 'DEBUG', 'WARNING']
    counts = {level: 0 for level in levels}
    
    for log in logs:
        if log['level'] in counts:
            counts[log['level']] += 1
    return counts

def display_log_counts(counts):
    header = f"{'Рівень логування':<18} | {'Кількість':<10}"
    divider = '-' * len(header)
    print(header)
    print(divider)
    for level, count in counts.items():
        print(f"{level:<18} | {count:<10}")

def main():
    valid_levels = ['INFO', 'ERROR', 'DEBUG', 'WARNING']
    if len(sys.argv) < 2:
        print("Використання: python task3.py <шлях_до_лог_файлу> [рівень логування]")
        sys.exit(1)

    file_path = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) > 2 else None
    
    if level and level not in valid_levels:
        print(f"Невідомий рівень логування: {level}. Введіть один з наступних рівнів: {', '.join(valid_levels)}")
        sys.exit(1)

    try:
        logs = load_logs(file_path)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
        
    log_counts = count_logs_by_level(logs)
    display_log_counts(log_counts)

    if level:
        filtered_logs = filter_logs_by_level(logs, level)
        print(f"Деталі логів для рівня {level.upper()}:")
        for log in filtered_logs:
            print(f"{log['date']} {log['time']} {log['level']} {log['message']}")
       
if __name__ == "__main__":
    main()