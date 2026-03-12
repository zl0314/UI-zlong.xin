# -*- coding: utf-8 -*-
"""
解析share.csv文件，提取分享名和URL，生成新的CSV文件
"""
import csv
import re

# 输入和输出文件路径
INPUT_CSV = 'j:\\wangpangou\\share.csv'
OUTPUT_CSV = 'j:\\wangpangou\\share_extracted.csv'

def extract_url(text):
    """
    从文本中提取完整的https链接
    """
    url_pattern = r'(https://[^\s"]+)'
    matches = re.findall(url_pattern, text)
    if matches:
        return matches[0]
    return None

def main():
    """
    主函数
    """
    print("开始解析share.csv文件...")
    
    extracted_data = []
    processed_count = 0
    
    # 尝试不同的编码
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16']
    
    for encoding in encodings:
        try:
            with open(INPUT_CSV, 'r', encoding=encoding) as f:
                # 读取CSV文件
                reader = csv.reader(f)
                rows = list(reader)
                
                if len(rows) > 0:
                    print(f"使用编码：{encoding}")
                    print(f"找到 {len(rows)} 行数据")
                    
                    # 跳过标题行
                    for i, row in enumerate(rows[1:], start=2):
                        if len(row) >= 3:
                            # 分享名在第二列
                            title = row[1].strip() if len(row) > 1 else ''
                            # 分享地址在第三列
                            share_text = row[2].strip() if len(row) > 2 else ''
                            
                            # 从分享地址中提取URL
                            url = extract_url(share_text)
                            
                            if title and url:
                                extracted_data.append([title, url])
                                processed_count += 1
                                print(f"处理第 {i} 行：{title}")
                    
                    # 如果成功处理了数据，跳出循环
                    if processed_count > 0:
                        break
        except Exception as e:
            continue
    
    # 写入新的CSV文件
    if extracted_data:
        with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # 写入标题行
            writer.writerow(['title', 'url'])
            # 写入数据
            for item in extracted_data:
                writer.writerow(item)
        
        print(f"\n✓ 完成！")
        print(f"  处理项目：{processed_count} 个")
        print(f"  输出文件：{OUTPUT_CSV}")
    else:
        print("错误：没有找到有效的分享数据")

if __name__ == '__main__':
    main()
