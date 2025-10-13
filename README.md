# PaperRenamer: 学术论文PDF智能重命名工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://python.org)

一个智能化的学术论文PDF重命名工具，通过提取元数据、查询DOI信息并应用自定义模板，一键将杂乱的论文文件重命名为规范的格式。

## 📁 项目结构

```
paper-renamer/
├── paper_renamer_gui.py    # 主程序入口
├── README.md              # 项目说明文档
├── LICENSE                # 开源许可证
└── requirements.txt       # Python依赖包列表
```

## ✨ 核心功能

- **智能元数据提取**：自动从PDF中提取作者、年份、期刊、标题等关键信息。
- **权威数据增强**：通过DOI号联网查询Crossref，获取最准确的论文元数据。
 - **arXiv支持**：识别arXiv预印本ID并获取其元数据。
- **多源数据融合**：智能整合PDF内嵌元数据、BibTeX文件和文本内容，确保信息完整。
- **灵活命名模板**：提供预设模板并支持完全自定义，如 `{author}-{year}-{journal}-{title}`。
- **图形化界面**：简洁直观的GUI，操作简单，无需命令行知识。

## 🚀 快速开始

1. 确保已安装 Python 3.7+
2. 安装依赖：`pip install PyPDF2 pdfminer.six pymupdf bibtexparser requests`
3. 运行程序：`python paper_renamer_gui.py`

## 📷 截图

> <img width="674" height="462" alt="image" src="https://github.com/user-attachments/assets/6eeef2cd-040b-40de-8eb1-c1593575d797" />


## 🤝 贡献

欢迎提交Issue报告问题或提出建议。也欢迎通过Pull Request贡献代码！

## 📄 许可证

本项目采用 [MIT许可证](LICENSE)。
