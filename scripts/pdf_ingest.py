import pypdfium2 as pdfium
import argparse
import os 

def get_all_text(path):
    pdf = pdfium.PdfDocument(path)
    text = ""
    for i, page in enumerate(pdf, start=1):  # Page numbers manually
        text += f"\n\nPage {i}\n"
        text += page.get_textpage().get_text_range()
    return text

def get_all_text_json(path):
    pdf = pdfium.PdfDocument(path)
    text = []
    for i, page in enumerate(pdf, start=1):
        text.append({
            "page_number": str(i),
            "text": page.get_textpage().get_text_bounded()
        })
    return text

def process_file(pdf_path, mode, output_dir):
    print(f"Ingesting PDF file from path: {pdf_path}")
    file_name = os.path.basename(pdf_path).replace(".pdf", "")
    output_path = os.path.join(output_dir, f"{file_name}.{mode}")

    if mode == "txt":
        text = get_all_text(pdf_path)
        with open(output_path, "w") as f:
            f.write(text)
    elif mode == "json":
        text = get_all_text_json(pdf_path)
        with open(output_path, "w") as f:
            f.write(str(text))
    
    print(f"Output written to: {output_path}")

def main(args):
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    pdf_files_found = False
    for root, dirs, files in os.walk(args.path):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files_found = True
                pdf_path = os.path.join(root, file)
                process_file(pdf_path, args.mode, args.output)
    
    if not pdf_files_found:
        print(f"No PDF files found in the directory: {args.path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PDF Ingest')
    parser.add_argument('--path', help='Path to the directory containing PDFs')
    parser.add_argument('--mode', help='Mode to ingest the PDF file', choices=["txt", "json"], default="txt")
    parser.add_argument('--output', help='Output directory')
    args = parser.parse_args()
    main(args)
