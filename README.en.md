# PaperRenamer: Intelligent Academic Paper PDF Renaming Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://python.org)

**[中文](README.md) | English**

An intelligent tool for renaming academic‑paper PDFs. It extracts metadata, queries DOI information and applies custom templates to batch rename messy PDF files into standardized filenames with one click.

## 📁 Project Structure

```plaintext
paper-renamer/
├── paper_renamer_gui.py      # 主程序入口
├── README.md                 # 项目说明文档
├── LICENSE                   # 开源许可证
└── requirements.txt          # Python依赖包列表
```

## ✨ Key Features

- **Intelligent Metadata Extraction**: Automatically extract authors, year, journal, title and other key information from PDF files.
- **Authoritative Data Enrichment**: Retrieve accurate paper metadata from Crossref via DOI lookup.
- **arXiv Support**: Recognize arXiv preprint IDs and fetch corresponding metadata.
- **Multi‑source Data Fusion**: Smart merge embedded PDF metadata, BibTeX entries and text content for complete information.
- **Flexible Naming Templates**: Built‑in presets and full customisation support, e.g. `{author}-{year}-{journal}-{title}`.
- **Graphical User Interface**: Clean and intuitive GUI, no command‑line knowledge required.

## 🚀 Quick Start

1. Make sure Python 3.7+ is installed
2. Install dependencies: `pip install PyPDF2 pdfminer.six pymupdf bibtexparser requests`
3. Launch the application: `python paper_renamer_gui.py`

## 📷 Screenshot

> <img width="674" height="462" alt="GUI screenshot" src="https://github.com/user-attachments/assets/6eeef2cd-040b-40de-8eb1-c1593575d797" />

## 🤝 Contributing

Feel free to open Issues for bug reports and feature suggestions. Pull Requests for code contributions are welcome!

## 📄 License

This project is licensed under the [MIT License](LICENSE).
