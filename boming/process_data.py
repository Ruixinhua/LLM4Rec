import csv
import random

L = 3  # 保留的历史新闻数量
K = 2  # 负例数量

# 读取CSV文件
with open('sampled_1000.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    processed_lines = []

    for line in reader:
        # 处理历史新闻
        history_news = line['history'].split('\n')
        history_news = history_news[-L:]  # 保留最后L个历史新闻

        # 处理候选新闻
        candidate_news = line['candidate'].split('\n')
        labels = line['label'][1:-1].split(', ')  # 假设label是以[Cx, Cy, ...]格式给出

        # 选择一个正例和K个负例
        positive_example = random.choice(labels)
        negative_examples = random.choices([c for c in candidate_news if c not in labels], k=K)

        # 组成新的候选列表
        new_candidates = [positive_example] + negative_examples
        new_label = positive_example  # 新的标签是选择的正例

        # 将处理后的数据添加到新的列表中
        processed_lines.append({
            'history': '\n'.join(history_news),
            'candidate': '\n'.join(new_candidates),
            'label': new_label
        })

# 写入到新的CSV文件
with open('processed_file.csv', mode='w', encoding='utf-8', newline='') as file:
    fieldnames = ['history', 'candidate', 'label']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for line in processed_lines:
        writer.writerow(line)
