import base64
from pathlib import Path

from src.ingestion import ingest_file

PDF_B64 = (
    "CiVQREYtMS40CjEgMCBvYmoKPDwgL1R5cGUgL0NhdGFsb2cgL1BhZ2VzIDIgMCBSID4+CmVuZG9iagoy"
    "IDAgb2JqCjw8IC9UeXBlIC9QYWdlcyAvS2lkcyBbMyAwIFJdIC9Db3VudCAxID4+CmVuZG9iagozIDAg"
    "b2JqCjw8IC9UeXBlIC9QYWdlIC9QYXJlbnQgMiAwIFIgL1Jlc291cmNlcyA8PCAvRm9udCA8PCAvRjEg"
    "NCAwIFIgPj4gPj4gL01lZGlhQm94IFswIDAgMjAwIDIwMF0gL0NvbnRlbnRzIDUgMCBSID4+CmVuZG9i"
    "ago0IDAgb2JqCjw8IC9UeXBlIC9Gb250IC9TdWJ0eXBlIC9UeXBlMSAvQmFzZUZvbnQgL0hlbHZldGlj"
    "YSA+PgplbmRvYmoKNSAwIG9iago8PCAvTGVuZ3RoIDQ0ID4+CnN0cmVhbQpCVAovRjEgMTIgVGYKNzIg"
    "NzIgVGQKKEhlbGxvIFBERikgVGoKRVQKZW5kc3RyZWFtCmVuZG9iagp4cmVmCjAgNgowMDAwMDAwMDAw"
    "IDY1NTM1IGYgCjAwMDAwMDAwMTAgMDAwMDAgbiAKMDAwMDAwMDA2MSAwMDAwMCBuIAowMDAwMDAwMTEx"
    "IDAwMDAwIG4gCjAwMDAwMDAyMjIgMDAwMDAgbiAKMDAwMDAwMDI5NiAwMDAwMCBuIAp0cmFpbGVyCjw8"
    "IC9Sb290IDEgMCBSIC9TaXplIDYgPj4Kc3RhcnR4cmVmCjM3NQolJUVPRgo="
)


def write_pdf(path: Path) -> None:
    data = base64.b64decode(PDF_B64)
    path.write_bytes(data)


def test_ingest_pdf(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    write_pdf(pdf_path)
    doc = ingest_file(str(pdf_path))
    assert "Hello PDF" in doc.chunks[0].content


def test_ingest_docx(tmp_path):
    from docx import Document as Doc

    file_path = tmp_path / "sample.docx"
    document = Doc()
    document.add_paragraph("Hello DOCX")
    document.save(file_path)

    doc = ingest_file(str(file_path))
    assert "Hello DOCX" in doc.chunks[0].content


def test_ingest_xlsx(tmp_path):
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.append(["A", "B"])
    ws.append(["1", "2"])
    file_path = tmp_path / "sample.xlsx"
    wb.save(file_path)

    doc = ingest_file(str(file_path))
    assert "A\tB" in doc.chunks[0].content
