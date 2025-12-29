#!/usr/bin/env python3
"""
将多个 Markdown 文档拼接成一个完整的 book.md 文件
"""

import os
import re
from pathlib import Path

# 定义文档顺序
DOCS_ORDER = [
    "README.md",
    "docs/00-HOW-TO.md",
    "docs/01-第一部分.md",
    "docs/02-第二部分.md",
    "docs/03-第三部分.md",
    "docs/04-第四部分.md",
    "docs/05-第五部分.md",
    "docs/06-附录.md",
    "docs/07-结语.md",
]

def read_file(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"警告: 文件 {filepath} 不存在，跳过")
        return None

def fix_image_paths(content, source_dir):
    """修复图片路径，从相对路径改为相对于 docs/assets 的路径"""
    # 将 ./assets/ 替换为 docs/assets/
    content = content.replace('./assets/', 'docs/assets/')
    return content

def fix_links(content):
    """将跨文件链接转换为文档内锚点链接"""
    # 匹配 Markdown 链接格式: [文本](路径#锚点) 或 [文本](路径)
    # 例如: [第一部分](docs/01-第一部分.md#_11-引言) -> [第一部分](#_11-引言)
    
    def replace_link(match):
        text = match.group(1)  # 链接文本
        link = match.group(2)   # 链接路径
        
        # 如果链接指向 docs/ 目录下的 .md 文件，转换为锚点链接
        if (link.startswith('docs/') or link.startswith('./docs/')) and '.md' in link:
            # 提取锚点部分
            if '#' in link:
                anchor = '#' + link.split('#', 1)[1]
                return f'[{text}]({anchor})'
            else:
                # 没有锚点，只保留文本（移除链接）
                return text
        
        # 如果已经是文档内链接（以#开头），保持不变
        if link.startswith('#'):
            return match.group(0)
        
        # 其他链接（如外部链接）保持不变
        return match.group(0)
    
    # 匹配 [文本](链接) 格式
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    content = re.sub(pattern, replace_link, content)
    
    return content

def promote_headings(content):
    """将所有标题等级提升一级，一级标题保持不变"""
    # 匹配 Markdown 标题格式: # 标题 或 ## 标题 等
    # 一级标题 (#) 保持不变，其他级别都提升一级（减少一个#）
    
    def replace_heading(match):
        hashes = match.group(1)  # # 符号
        title = match.group(2)   # 标题文本
        
        # 如果是一级标题（只有一个#），保持不变
        if len(hashes) == 1:
            return match.group(0)
        
        # 其他级别：减少一个#符号
        new_hashes = hashes[1:]  # 去掉第一个#
        return f'{new_hashes} {title}'
    
    # 匹配标题行：以 # 开头，后面跟空格和标题文本
    # 支持 ATX 风格标题: # 标题
    pattern = r'^(#{1,6})\s+(.+)$'
    content = re.sub(pattern, replace_heading, content, flags=re.MULTILINE)
    
    return content

def build_book():
    """构建完整的 book.md"""
    book_content = []
    
    for doc_path in DOCS_ORDER:
        print(f"处理: {doc_path}")
        content = read_file(doc_path)
        
        if content is None:
            continue
        
        # 修复图片路径
        if 'docs/' in doc_path:
            content = fix_image_paths(content, doc_path)
        
        # 修复链接（转换为文档内锚点）
        content = fix_links(content)
        
        # 提升标题级别（一级标题保持不变）
        content = promote_headings(content)
        
        # 添加分隔符（除了第一个文件）
        if book_content:
            book_content.append("\n\n---\n\n")
        
        # 添加文档内容
        book_content.append(content)
    
    # 写入 book.md
    output = ''.join(book_content)
    with open('book.md', 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"\n✅ 完成! book.md 已生成 ({len(output)} 字符)")

if __name__ == '__main__':
    build_book()

