"""Fake Profile Investigator — desktop app and command-line report mode."""
import argparse
import json
from pathlib import Path
from core import CREDIT, NOTICE, FIELDS, compare, load_case, save_case, report_html

BASE = Path(__file__).resolve().parent

def gui():
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    from tkinter.scrolledtext import ScrolledText
    root = tk.Tk()
    root.title('Fake Profile Investigator | Sabaz Ali Khan')
    root.geometry('1120x820')
    root.minsize(850, 650)
    root.configure(bg='#0b151d')
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='#0b151d')
    style.configure('TLabel', background='#0b151d', foreground='#c7fbe1')
    style.configure('TButton', padding=7)
    ttk.Label(root, text='FAKE PROFILE INVESTIGATOR', font=('Segoe UI', 21, 'bold')).pack(pady=(12,3))
    ttk.Label(root, text=CREDIT).pack()
    ttk.Label(root, text='Offline comparison • Public-profile details entered by you • Local photos only').pack(pady=5)
    book = ttk.Notebook(root)
    book.pack(fill='both', expand=True, padx=12, pady=10)
    case_tab, results_tab, about_tab = [ttk.Frame(book, padding=12) for _ in range(3)]
    for tab, name in ((case_tab,'Case & profiles'),(results_tab,'Comparison results'),(about_tab,'Banner & guide')):
        book.add(tab, text=name)
    title = tk.StringVar(value='New profile review')
    observed = tk.StringVar()
    ttk.Label(case_tab, text='Case title').pack(anchor='w')
    ttk.Entry(case_tab, textvariable=title).pack(fill='x')
    ttk.Label(case_tab, text='Observation date/time and timezone (as recorded by you)').pack(anchor='w', pady=(8,0))
    ttk.Entry(case_tab, textvariable=observed).pack(fill='x')
    columns = ttk.Frame(case_tab)
    columns.pack(fill='both', expand=True, pady=10)
    inputs = {}
    for col, key in enumerate(('reference','candidate')):
        panel = ttk.Frame(columns, padding=8)
        panel.grid(row=0, column=col, sticky='nsew')
        columns.columnconfigure(col, weight=1)
        ttk.Label(panel, text=key.title()+' profile', font=('Segoe UI',14,'bold')).pack(anchor='w')
        inputs[key] = {}
        for field in FIELDS:
            ttk.Label(panel, text=field.replace('_',' ').title()).pack(anchor='w', pady=(6,0))
            if field == 'bio':
                widget = ScrolledText(panel, height=4, wrap='word')
                widget.pack(fill='x')
                inputs[key][field] = widget
            else:
                variable = tk.StringVar()
                ttk.Entry(panel, textvariable=variable).pack(fill='x')
                inputs[key][field] = variable
                if field == 'photo':
                    def choose(v=variable):
                        name = filedialog.askopenfilename(title='Select local photo', filetypes=[('Photos','*.png *.jpg *.jpeg *.webp *.bmp'),('All files','*.*')])
                        if name: v.set(name)
                    ttk.Button(panel, text='Choose photo', command=choose).pack(anchor='w', pady=4)
    ttk.Label(case_tab, text='Evidence / ownership notes (saved locally as plain text)').pack(anchor='w')
    notes = ScrolledText(case_tab, height=3, wrap='word')
    notes.pack(fill='x')
    output = ScrolledText(results_tab, wrap='word', bg='#07110e', fg='#88f5ba', font=('Consolas',11))
    output.pack(fill='both', expand=True)
    guide = ScrolledText(about_tab, bg='#07110e', fg='#88f5ba', font=('Consolas',10), wrap='word')
    guide.pack(fill='both', expand=True)
    guide.insert('1.0', (BASE/'banner.txt').read_text(encoding='utf-8')+'\n'+CREDIT+'\n\n'+NOTICE+'\n\n1. Enter a trusted reference and a candidate profile.\n2. Paste usernames, display names, bios and source URLs. URLs are recorded, not fetched.\n3. Optionally select two local photos.\n4. Compare, save a JSON case, or export an HTML report.\n\nSave before closing or opening another case. Photos remain at their original paths; case files do not copy them. Protect reports and case files: they are not encrypted. No automated scraping, face recognition, reporting or identity lookup is performed.\n\nText percentages measure character overlap, not likelihood of fraud. Photo distance is 0–64 (lower means closer coarse structure); crops, color changes and unrelated simple images can mislead it. Verify clues manually.')
    guide.configure(state='disabled')
    def collect():
        return {'version':1, 'title':title.get(), 'observed_at':observed.get(), 'notes':notes.get('1.0','end-1c'),
                **{key:{field:(w.get('1.0','end-1c') if field=='bio' else w.get()) for field,w in entries.items()} for key,entries in inputs.items()}}
    def protect(fn):
        try: fn()
        except Exception as exc: messagebox.showerror('Unable to complete action', str(exc))
    def run():
        result = compare(collect())
        output.configure(state='normal')
        output.delete('1.0','end')
        output.insert('1.0', NOTICE+'\n\n'+json.dumps(result, ensure_ascii=False, indent=2))
        output.configure(state='disabled')
        book.select(results_tab)
    def save():
        p = filedialog.asksaveasfilename(defaultextension='.json',filetypes=[('JSON case','*.json')])
        if p:
            save_case(p,collect())
            messagebox.showinfo('Saved','Case saved. Keep photo originals at their recorded paths.')
    def open_case():
        p = filedialog.askopenfilename(filetypes=[('JSON case','*.json')])
        if not p: return
        case = load_case(p)
        title.set(case.get('title',''))
        observed.set(case.get('observed_at',''))
        notes.delete('1.0','end'); notes.insert('1.0',case.get('notes',''))
        for key,entries in inputs.items():
            for field,w in entries.items():
                if field == 'bio':
                    w.delete('1.0','end'); w.insert('1.0',case[key].get(field,''))
                else: w.set(case[key].get(field,''))
        output.configure(state='normal'); output.delete('1.0','end'); output.configure(state='disabled')
        book.select(case_tab)
    def export():
        case = collect()
        result = compare(case)
        p = filedialog.asksaveasfilename(defaultextension='.html',filetypes=[('HTML report','*.html')])
        if p:
            Path(p).write_text(report_html(case,result),encoding='utf-8')
            messagebox.showinfo('Exported','Report saved. Open it in a browser; Print > Save as PDF is also available.')
    actions = ttk.Frame(root)
    actions.pack(fill='x', padx=12, pady=(0,12))
    for label,fn in [('Compare profiles',run),('Save case',save),('Open case',open_case),('Export HTML report',export)]:
        ttk.Button(actions,text=label,command=lambda f=fn: protect(f)).pack(side='left',padx=4)
    root.mainloop()

def main():
    parser = argparse.ArgumentParser(description='Local public-profile comparison assistant')
    parser.add_argument('--case', help='Analyze a saved JSON case without the GUI')
    parser.add_argument('--report', help='Output HTML report path (requires --case)')
    args = parser.parse_args()
    if args.report and not args.case: parser.error('--report requires --case')
    if args.case:
        try:
            case = load_case(args.case)
            result = compare(case)
            print(json.dumps(result,ensure_ascii=True,indent=2))
            if args.report: Path(args.report).write_text(report_html(case,result),encoding='utf-8')
        except (ValueError,OSError) as exc: parser.exit(1,f'Error: {exc}\n')
    else: gui()

if __name__ == '__main__': main()
