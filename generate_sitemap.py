#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

# 站点基础URL
BASE_URL = "http://ip地址"

# 需要排除的文件和目录
EXCLUDED_FILES = ["_navbar.md", "_sidebar.md"]
EXCLUDED_DIRS = []

# XML头部
XML_HEADER = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" 
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9" 
        xmlns:xhtml="http://www.w3.org/1999/xhtml" 
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" 
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">'''

# XML尾部
XML_FOOTER = "</urlset>"

# URL模板
# 使用绝对路径
URL_TEMPLATE = "<url>\n<loc>{}.md</loc>\n</url>"

def is_markdown_file(filename):
    """
    检查文件是否为Markdown文件
    """
    return filename.endswith(".md")

def should_include(path, filename):
    """
    检查文件是否应该被包含在站点地图中
    """
    if filename in EXCLUDED_FILES:
        return False
    
    for excluded_dir in EXCLUDED_DIRS:
        if excluded_dir in path:
            return False
    
    return True

def escape_xml(text):
    """
    转义XML特殊字符
    """
    # 替换XML特殊字符
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text

def path_to_url(path):
    """
    将文件路径转换为URL
    """
    # 移除.md扩展名
    if path.endswith(".md"):
        path = path[:-3]
    
    # 处理README.md特殊情况
    if path.endswith("README"):
        path = path[:-7]
    
    # 确保路径使用正斜杠
    path = path.replace("\\", "/")
    
    # 构建完整URL
    url = f"{BASE_URL}/{path}"
    
    # 处理可能的双斜杠，但保留协议中的双斜杠
    url = re.sub(r'(?<!:)//+', '/', url)
    
    # 确保BASE_URL后有一个斜杠
    if not BASE_URL.endswith('/'):
        url = url.replace(f"{BASE_URL}/", f"{BASE_URL}/")
    
    return url

def generate_sitemap(docs_dir, output_file="sitemap.xml"):
    """
    生成站点地图
    """
    urls = []
    
    # 遍历docs目录
    for root, dirs, files in os.walk(docs_dir):
        # 过滤掉不需要的目录
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        
        for file in files:
            if is_markdown_file(file) and should_include(root, file):
                # 获取相对于docs目录的路径
                rel_path = os.path.relpath(os.path.join(root, file), docs_dir)
                
                # 转换为URL
                url = path_to_url(rel_path)
                
                # 添加到URL列表
                urls.append(url)
    
    # 生成XML内容
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(XML_HEADER + "\n")
        
        for url in sorted(urls):
            # 转义URL中的XML特殊字符
            escaped_url = escape_xml(url)
            f.write(URL_TEMPLATE.format(escaped_url) + "\n")
        
        f.write(XML_FOOTER)
    
    print(f"站点地图已生成: {output_file}")
    print(f"共包含 {len(urls)} 个URL")

def main():
    # 获取docs目录的路径
    docs_dir = input("请输入docs目录的路径 (默认为当前目录下的docs): ") or "docs"
    
    # 获取输出文件路径
    output_file = input("请输入输出文件路径 (默认为当前目录下的sitemap.xml): ") or "sitemap.xml"
    
    # 检查docs目录是否存在
    if not os.path.exists(docs_dir):
        print(f"错误: 目录 '{docs_dir}' 不存在!")
        return
    
    # 生成站点地图
    generate_sitemap(docs_dir, output_file)

if __name__ == "__main__":
    main()