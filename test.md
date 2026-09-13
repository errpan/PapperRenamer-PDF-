# PaperRenamer: 学术论文PDF智能重命名工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://python.org)

**🌐 Language / 语言：点击切换 → &nbsp;&nbsp;<kbd>🇨🇳 中文</kbd>&nbsp;&nbsp;|&nbsp;&nbsp;<kbd>🇬🇧 English</kbd>**

---

<details open>
<summary><b>🇨🇳 中文（点击收起）</b></summary>

<br>

一个智能化的学术论文PDF重命名工具，通过提取元数据、查询DOI信息并应用自定义模板，一键将杂乱的论文文件重命名为规范的格式。

## 📁 项目结构

```plaintext
paper-renamer/
├── paper_renamer_gui.py    # 主程序入口
├── README.md               # 项目说明文档
├── LICENSE                 # 开源许可证
└── requirements.txt        # Python依赖包列表
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

<img width="674" height="462" alt="GUI screenshot" src="https://github.com/user-attachments/assets/6eeef2cd-040b-40de-8eb1-c1593575d797" />

## 🤝 贡献

欢迎提交 Issue 报告问题或提出建议。也欢迎通过 Pull Request 贡献代码！

## 📄 许可证

本项目采用 [MIT License](LICENSE)。

## 📌 引用 Citation

如果该项目对你的研究有帮助，欢迎 Star 并引用本仓库：

```bibtex
@software{paper_renamer,
  author = {Erpan},
  title  = {PaperRenamer: 学术论文PDF智能重命名工具},
  year   = {2026},
  url    = {https://github.com/erppan/PapperRenamer-PDF-}
}
```

</details>

<details>
<summary><b>🇬🇧 English（点击展开）</b></summary>

<br>

An intelligent tool for renaming academic-paper PDFs. It extracts metadata, queries DOI information and applies custom templates to batch rename messy PDF files into standardized filenames with one click.

## 📁 Project Structure

```plaintext
paper-renamer/
├── paper_renamer_gui.py    # Main program entry
├── README.md               # Project documentation
├── LICENSE                 # Open-source license
└── requirements.txt        # Python dependency list
```

## ✨ Key Features

- **Intelligent Metadata Extraction**: Automatically extract authors, year, journal, title and other key information from PDF files.
- **Authoritative Data Enrichment**: Retrieve accurate paper metadata from Crossref via DOI lookup.
- **arXiv Support**: Recognize arXiv preprint IDs and fetch corresponding metadata.
- **Multi-source Data Fusion**: Smartly merge embedded PDF metadata, BibTeX entries and text content for complete information.
- **Flexible Naming Templates**: Built-in presets and full customisation support, e.g. `{author}-{year}-{journal}-{title}`.
- **Graphical User Interface**: Clean and intuitive GUI, no command-line knowledge required.

## 🚀 Quick Start

1. Make sure Python 3.7+ is installed
2. Install dependencies: `pip install PyPDF2 pdfminer.six pymupdf bibtexparser requests`
3. Launch the application: `python paper_renamer_gui.py`

## 📷 Screenshot

<img width="674" height="462" alt="GUI screenshot" src="https://github.com/user-attachments/assets/6eeef2cd-040b-40de-8eb1-c1593575d797" />

## 🤝 Contributing

Feel free to open Issues for bug reports and feature suggestions. Pull Requests for code contributions are welcome!

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 📌 Citation

If this software helps your research, please star this repository:

```bibtex
@software{paper_renamer,
  author = {Erpan},
  title  = {PaperRenamer: Intelligent Academic Paper PDF Renaming Tool},
  year   = {2026},
  url    = {https://github.com/erppan/PapperRenamer-PDF-}
}
```

</details>
