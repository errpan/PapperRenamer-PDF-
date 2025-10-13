import os, re, threading, requests, tkinter as tk
from tkinter import filedialog, messagebox, ttk, StringVar
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
import fitz
import bibtexparser

def extract_pdf_metadata(pdf_path):
    meta = {}
    try:
        r = PdfReader(pdf_path)
        info = r.metadata
        meta.update({k.lower(): v for k, v in info.items() if isinstance(v, str)})
    except Exception: pass
    try:
        doc = fitz.open(pdf_path)
        meta.update({k.lower(): v for k, v in doc.metadata.items() if isinstance(v, str)})
        doc.close()
    except Exception: pass
    return meta

def extract_text_info(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = doc[0].get_text()
        doc.close()
        return text
    except Exception:
        try:
            return extract_text(pdf_path, maxpages=1)
        except Exception:
            return ""

def extract_doi(text):
    m = re.search(r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b', text, re.I)
    return m.group(0) if m else ""

def extract_arxiv_id(text):
    m = re.search(r'arXiv:\s?(\d{4}\.\d{4,5})', text)
    return m.group(1) if m else ""

def extract_bibtex_metadata(bibtex_path):
    try:
        with open(bibtex_path, encoding='utf-8') as f:
            bib = bibtexparser.load(f)
        entry = bib.entries[0]
        return {k.lower(): v for k, v in entry.items()}
    except Exception:
        return {}

def query_crossref(doi):
    url = f"https://api.crossref.org/works/{doi}"
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            d = r.json()["message"]
            authors = "; ".join([f"{a.get('family','')}, {a.get('given','')}" for a in d.get("author",[])])
            return {
                "title": d.get("title", [""])[0],
                "author": authors,
                "journal": d.get("container-title", [""])[0],
                "year": str(d.get("published-print", d.get("created", {})).get("date-parts", [[None]])[0][0]),
                "volume": d.get("volume", ""),
                "issue": d.get("issue", ""),
                "pages": d.get("page", ""),
                "doi": doi,
                "issn": d.get("ISSN", [""])[0] if d.get("ISSN") else "",
                "publisher": d.get("publisher", "")
            }
    except Exception:
        return {}
    return {}

def query_arxiv(arxiv_id):
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(r.content)
            entry = root.find('{http://www.w3.org/2005/Atom}entry')
            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            authors = "; ".join([a.find('{http://www.w3.org/2005/Atom}name').text for a in entry.findall('{http://www.w3.org/2005/Atom}author')])
            year = entry.find('{http://www.w3.org/2005/Atom}published').text[:4]
            return {
                "title": title, "author": authors, "journal": "arXiv", "year": year, "arxiv_id": arxiv_id
            }
    except Exception:
        return {}
    return {}

def extract_candidates(text):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    title, author, journal, year, volume, issue, pages, issn = "", "", "", "", "", "", "", ""
    # 优先检查前5行，排除摘要/引言等章节标题
    title_candidates = []
    for i, l in enumerate(lines[:5]):
        if 10 < len(l) < 120 and not re.search(r'Abstract|Introduction|References|Keywords', l, re.I):
            title_candidates.append(l)
    # 若前5行无候选，扩展至前10行
    if not title_candidates:
        title_candidates = [l for l in lines[:10] if 10 < len(l) < 120]
    if title_candidates:
        title = max(title_candidates, key=lambda l: len(l))  # 选择最长行作为标题
    author_candidates = [l for l in lines if (',' in l or 'and' in l or 'et al' in l) and len(l) < 70]
    if author_candidates:
        author = author_candidates[0]
    for l in lines:
        if re.match(r'\d{4}', l): year = l[:4]
        if 'Vol' in l or 'Volume' in l: volume = l
        if 'Issue' in l or 'No.' in l: issue = l
        if re.search(r'pp\.|pages', l): pages = l
        if 'ISSN' in l: issn = l
        if re.match(r'^[A-Z][A-Za-z0-9 \-]{8,}$', l) and not journal: journal = l
    return dict(title=title, author=author, journal=journal, year=year, volume=volume, issue=issue, pages=pages, issn=issn)

def get_complete_metadata(pdf_path, bibtex_path=None):
    meta = extract_pdf_metadata(pdf_path)
    text = extract_text_info(pdf_path)
    doi = extract_doi(text)
    arxiv_id = extract_arxiv_id(text)
    bibtex_meta = extract_bibtex_metadata(bibtex_path) if bibtex_path else {}
    candidates = extract_candidates(text)
    crossref_info = query_crossref(doi) if doi else {}
    arxiv_info = query_arxiv(arxiv_id) if arxiv_id else {}

    result = {}
    # 优先使用Crossref数据（如果DOI存在且查询成功）
    if crossref_info:
        result.update({k: v for k, v in crossref_info.items() if v})
    # 补充arXiv信息（仅当必要字段缺失时）
    if arxiv_info and not result.get('title'):
        result.update({k: v for k, v in arxiv_info.items() if v and k not in result})
    # 合并BibTeX元数据
    result.update({k: v for k, v in bibtex_meta.items() if v and k not in result})
    # 合并PDF元数据
    result.update({k: v for k, v in meta.items() if v and k not in result})
    # 使用文本提取的候选信息作为最后补充
    result.update({k: v for k, v in candidates.items() if v and k not in result})
    # 确保所有字段都存在
    for k in ['title', 'author', 'journal', 'year', 'volume', 'issue', 'pages', 'doi', 'issn', 'publisher', 'arxiv_id']:
        if k not in result:
            result[k] = ""
    return result

def sanitize_filename(s):
    return re.sub(r'[\\/:*?"<>|]', '_', s).strip()

def make_filename(meta, template="{author}-{year}-{journal}-{title}"):
    return sanitize_filename(template.format(**{k: meta.get(k, "") for k in meta}))[:128]

class PaperRenamerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("学术论文PDF自动重命名工具")
        self.selected_files = []
        self.template_var = StringVar()
        self.template_var.set("{author}-{year}-{journal}-{title}")
        self.bibtex_dir = None
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0, sticky='nsew')

        self.file_label = ttk.Label(frame, text="未选择文件/文件夹")
        self.file_label.grid(row=0, column=0, columnspan=4, sticky='w')

        ttk.Button(frame, text="选择PDF文件", command=self.select_file).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(frame, text="选择文件夹", command=self.select_folder).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text="选择BibTeX文件夹", command=self.select_bibtex_folder).grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(frame, text="命名模板：").grid(row=2, column=0, sticky='e')
        # 预设模板选项
        template_options = [
            "{author}-{year}-{journal}-{title}",
            "{year}_{author}_{title}",
            "{doi}_{title}",
            "{author}_{year}_{pages}",
            "{journal}_{year}_{title}"
        ]
        self.template_combo = ttk.Combobox(frame, textvariable=self.template_var, values=template_options, width=50, state="normal")
        self.template_combo.grid(row=2, column=1, columnspan=3, sticky='w')
        self.template_combo.set("{author}-{year}-{journal}-{title}")

        ttk.Button(frame, text="开始重命名", command=self.start_rename).grid(row=3, column=0, columnspan=4, pady=8)

        self.progress = ttk.Progressbar(frame, orient="horizontal", length=480, mode="determinate")
        self.progress.grid(row=4, column=0, columnspan=4, pady=10)

        self.result_text = tk.Text(frame, height=14, width=90, state='disabled')
        self.result_text.grid(row=5, column=0, columnspan=4, pady=8)

        doc = "可用字段：author, year, journal, title, volume, issue, pages, doi, issn, publisher, arxiv_id\n如：{author}-{year}-{journal}-{title}.pdf"
        ttk.Label(frame, text=doc, foreground="#555", font=("Consolas", 10)).grid(row=6, column=0, columnspan=4, sticky='w')

    def select_file(self):
        file = filedialog.askopenfilename(filetypes=[("PDF 文件", "*.pdf")])
        if file:
            self.selected_files = [file]
            self.file_label.config(text=f"已选择文件：{os.path.basename(file)}")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            pdfs = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith('.pdf')]
            self.selected_files = pdfs
            self.file_label.config(text=f"已选择文件夹：{folder}（{len(pdfs)} 个PDF）")

    def select_bibtex_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.bibtex_dir = folder

    def start_rename(self):
        if not self.selected_files:
            messagebox.showwarning("未选择文件", "请先选择文件或文件夹！")
            return

        rule = self.template_var.get().strip()
        if not rule:
            messagebox.showwarning("模板错误", "请设置有效的重命名模板！")
            return

        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.progress['value'] = 0
        self.progress['maximum'] = len(self.selected_files)

        def batch():
            for idx, pdf_path in enumerate(self.selected_files):
                bibtex_path = None
                if self.bibtex_dir:
                    base = os.path.splitext(os.path.basename(pdf_path))[0]
                    bibtex_path = os.path.join(self.bibtex_dir, base + ".bib")
                    if not os.path.exists(bibtex_path): bibtex_path = None
                meta = get_complete_metadata(pdf_path, bibtex_path)
                new_name = make_filename(meta, rule) + ".pdf"
                new_path = os.path.join(os.path.dirname(pdf_path), new_name)
                status, error = "成功", ""
                try:
                    if os.path.abspath(pdf_path) != os.path.abspath(new_path):
                        os.rename(pdf_path, new_path)
                except Exception as e:
                    status, error = "失败", str(e)
                msg = f"{idx+1}/{len(self.selected_files)}：{os.path.basename(pdf_path)} -> {new_name} —— {status}"
                if error: msg += f"（{error}）"
                self.result_text.insert(tk.END, msg + "\n")
                self.progress['value'] = idx+1
                self.root.update_idletasks()
            self.result_text.config(state='disabled')
            messagebox.showinfo("处理完成", f"处理完成，共{len(self.selected_files)}个文件。")

        threading.Thread(target=batch).start()

def main():
    root = tk.Tk()
    PaperRenamerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()