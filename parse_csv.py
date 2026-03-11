# -*- coding: utf-8 -*-
"""
解析share.csv文件，生成HTML代码并写入share.html
"""
import csv
import re

# 输入和输出文件路径
INPUT_CSV = 'j:\\wangpangou\\share.csv'
OUTPUT_HTML = 'j:\\wangpangou\\share.html'

def extract_url(text):
    """
    从文本中提取完整的https链接
    """
    url_pattern = r'(https://[^\s"]+)'
    matches = re.findall(url_pattern, text)
    if matches:
        return matches[0]
    return None

def get_img_url(url):
    """
    根据URL判断使用哪个图片
    """
    if 'kuake' in url.lower() or 'quark' in url.lower():
        return './assets/images/kuake.png'
    elif 'baidu' in url.lower():
        return './assets/images/baidu.png'
    else:
        return './assets/images/kuake.png'  # 默认使用夸克图标

def generate_html(title, url, img_url):
    """
    生成HTML代码段
    """
    html = f'''<div class="col-sm-3">
<div class="xe-widget xe-conversations box2 label-info" onclick="window.open('{url}', '_blank')" data-toggle="tooltip" data-placement="bottom" title="{title}">
	 <div class="xe-comment-entry">
	 	 <a class="xe-user-img">
	 	 	 <img data-src="{img_url}" class="lozad img-circle" width="40">
	 	 </a>
	 	 <div class="xe-comment">
	 	 	 <p class="overflowClip_2">{title}</p>
	 	 </div>
	 </div>
</div>
</div>
'''
    return html

def main():
    """
    主函数
    """
    print("开始解析share.csv文件...")
    
    html_items = []
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
                                # 获取图片URL
                                img_url = get_img_url(url)
                                
                                # 生成HTML
                                html = generate_html(title, url, img_url)
                                html_items.append(html)
                                processed_count += 1
                                print(f"处理第 {i} 行：{title}")
                    
                    # 如果成功处理了数据，跳出循环
                    if processed_count > 0:
                        break
        except Exception as e:
            continue
    
    # 写入HTML文件
    if html_items:
        with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
            for item in html_items:
                f.write(item)
        
        print(f"\n✓ 完成！")
        print(f"  处理项目：{processed_count} 个")
        print(f"  输出文件：{OUTPUT_HTML}")
    else:
        print("错误：没有找到有效的分享数据")

if __name__ == '__main__':
    main()
