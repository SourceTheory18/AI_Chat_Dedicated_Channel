#!/usr/bin/env python3
"""
Markdown 文件质量检查脚本
由 BugHunter 创建，用于检查 AI_Chat_Dedicated_Channel 仓库中的 .md 文件格式规范性

功能：
1. 检查文件是否存在标题
2. 检查是否有空文件
3. 检查链接是否有效（基础检查）
4. 检查代码块是否闭合
5. 生成简单的质量报告
"""

import os
import sys
import re
from pathlib import Path

class MarkdownChecker:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.issues = []
        self.stats = {
            "total_files": 0,
            "files_with_issues": 0,
            "empty_files": 0,
            "missing_title": 0,
            "unclosed_code_blocks": 0
        }
    
    def find_markdown_files(self):
        """查找所有 .md 文件"""
        md_files = []
        for path in self.root_dir.rglob("*.md"):
            # 排除 .git 目录
            if ".git" not in str(path):
                md_files.append(path)
        return md_files
    
    def check_file(self, file_path):
        """检查单个文件"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            issues.append(f"无法读取文件：{e}")
            return issues
        
        # 检查是否为空文件
        if not content.strip():
            issues.append("⚠️ 空文件")
            self.stats["empty_files"] += 1
            return issues
        
        lines = content.split('\n')
        
        # 检查是否有标题（# 开头）
        has_title = any(line.strip().startswith('#') for line in lines[:10])
        if not has_title:
            issues.append("⚠️ 缺少主标题（建议在文件开头添加 # 标题）")
            self.stats["missing_title"] += 1
        
        # 检查代码块是否闭合（``` 成对出现）
        code_block_count = content.count('```')
        if code_block_count % 2 != 0:
            issues.append("❌ 代码块未闭合（``` 数量为奇数）")
            self.stats["unclosed_code_blocks"] += 1
        
        # 检查是否有明显的格式问题
        # 例如：连续的多个空行
        if '\n\n\n\n' in content:
            issues.append("💡 建议：存在连续多个空行，可以精简")
        
        # 检查链接格式 [text](url) 是否有明显错误
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, content)
        for text, url in links:
            if url.startswith(' ') or url.endswith(' '):
                issues.append(f"⚠️ 链接格式问题：[{text}]({url}) - URL 包含空格")
        
        return issues
    
    def check_all(self):
        """检查所有 Markdown 文件"""
        md_files = self.find_markdown_files()
        self.stats["total_files"] = len(md_files)
        
        print(f"🔍 开始检查 {len(md_files)} 个 Markdown 文件...\n")
        
        for file_path in md_files:
            rel_path = file_path.relative_to(self.root_dir)
            issues = self.check_file(file_path)
            
            if issues:
                self.stats["files_with_issues"] += 1
                print(f"📄 {rel_path}")
                for issue in issues:
                    print(f"   {issue}")
                print()
            else:
                print(f"✅ {rel_path}")
        
        self.print_report()
    
    def print_report(self):
        """打印总结报告"""
        print("\n" + "="*50)
        print("📊 质量检查报告")
        print("="*50)
        print(f"总文件数：{self.stats['total_files']}")
        print(f"有问题的文件：{self.stats['files_with_issues']}")
        print(f"空文件：{self.stats['empty_files']}")
        print(f"缺少标题：{self.stats['missing_title']}")
        print(f"代码块未闭合：{self.stats['unclosed_code_blocks']}")
        print("="*50)
        
        if self.stats["files_with_issues"] == 0:
            print("🎉 所有文件都符合基本规范！")
        else:
            print(f"💡 发现 {self.stats['files_with_issues']} 个文件需要改进")

if __name__ == "__main__":
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    checker = MarkdownChecker(root_dir)
    checker.check_all()
