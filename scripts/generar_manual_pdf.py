"""
Genera el Manual de Usuario en PDF usando ReportLab.
Ejecutar:
  cd smart_pm && ../env/bin/python scripts/generar_manual_pdf.py
"""
import os
import re
import sys

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_PATH = os.path.join(BASE_DIR, 'MANUAL_USUARIO.md')
IMG_DIR = os.path.join(BASE_DIR, 'Manual de usuario')
OUTPUT_PATH = os.path.join(BASE_DIR, 'MANUAL_USUARIO.pdf')

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, PageBreak, KeepTogether, ListFlowable, ListItem
)
from reportlab.lib.utils import ImageReader
from io import BytesIO


# ─── COLORES ───────────────────────────────────────────────
AZUL = colors.HexColor('#0066FF')
AZUL_OSCURO = colors.HexColor('#1E3A8A')
VERDE = colors.HexColor('#22C55E')
GRIS_OSCURO = colors.HexColor('#1E293B')
GRIS_MEDIO = colors.HexColor('#475569')
GRIS_CLARO = colors.HexColor('#F1F5F9')
GRIS_BORDE = colors.HexColor('#CBD5E1')
NEGRO = colors.HexColor('#0F172A')
BLANCO = colors.white
AZUL_FONDO = colors.HexColor('#EFF6FF')


def create_styles():
    styles = getSampleStyleSheet()

    custom = {}

    custom['titulo_doc'] = ParagraphStyle(
        'TituloDoc', parent=styles['Normal'],
        fontSize=24, fontName='Helvetica-Bold',
        textColor=AZUL_OSCURO, spaceAfter=4, leading=28,
    )
    custom['subtitulo_doc'] = ParagraphStyle(
        'SubtituloDoc', parent=styles['Normal'],
        fontSize=13, fontName='Helvetica',
        textColor=GRIS_MEDIO, spaceAfter=2, leading=16,
    )
    custom['version'] = ParagraphStyle(
        'Version', parent=styles['Normal'],
        fontSize=10, fontName='Helvetica-Oblique',
        textColor=GRIS_MEDIO, spaceAfter=12,
    )
    custom['h1'] = ParagraphStyle(
        'H1Custom', parent=styles['Normal'],
        fontSize=18, fontName='Helvetica-Bold',
        textColor=AZUL_OSCURO, spaceBefore=20, spaceAfter=8, leading=22,
    )
    custom['h2'] = ParagraphStyle(
        'H2Custom', parent=styles['Normal'],
        fontSize=14, fontName='Helvetica-Bold',
        textColor=GRIS_OSCURO, spaceBefore=14, spaceAfter=6, leading=18,
    )
    custom['h3'] = ParagraphStyle(
        'H3Custom', parent=styles['Normal'],
        fontSize=11, fontName='Helvetica-Bold',
        textColor=GRIS_OSCURO, spaceBefore=10, spaceAfter=4, leading=14,
    )
    custom['body'] = ParagraphStyle(
        'BodyCustom', parent=styles['Normal'],
        fontSize=9, fontName='Helvetica',
        textColor=NEGRO, spaceAfter=4, leading=13,
        alignment=TA_JUSTIFY,
    )
    custom['body_bold'] = ParagraphStyle(
        'BodyBold', parent=custom['body'],
        fontName='Helvetica-Bold',
    )
    custom['bullet'] = ParagraphStyle(
        'BulletCustom', parent=custom['body'],
        leftIndent=14, bulletIndent=4, spaceAfter=2,
    )
    custom['code'] = ParagraphStyle(
        'CodeCustom', parent=styles['Normal'],
        fontSize=8, fontName='Courier',
        textColor=GRIS_OSCURO, backColor=GRIS_CLARO,
        leftIndent=8, rightIndent=8,
        spaceBefore=4, spaceAfter=4, leading=11,
    )
    custom['note'] = ParagraphStyle(
        'NoteCustom', parent=styles['Normal'],
        fontSize=8.5, fontName='Helvetica-Oblique',
        textColor=AZUL_OSCURO, backColor=AZUL_FONDO,
        leftIndent=10, rightIndent=10,
        spaceBefore=4, spaceAfter=6, leading=12,
        borderPadding=6,
    )
    custom['toc'] = ParagraphStyle(
        'TOC', parent=styles['Normal'],
        fontSize=10, fontName='Helvetica',
        textColor=AZUL, spaceAfter=3, leading=14,
        leftIndent=8,
    )
    custom['table_header'] = ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontSize=8, fontName='Helvetica-Bold',
        textColor=BLANCO, alignment=TA_CENTER,
    )
    custom['table_cell'] = ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontSize=8, fontName='Helvetica',
        textColor=NEGRO, leading=10,
    )
    custom['table_cell_center'] = ParagraphStyle(
        'TableCellCenter', parent=custom['table_cell'],
        alignment=TA_CENTER,
    )
    custom['footer'] = ParagraphStyle(
        'Footer', parent=styles['Normal'],
        fontSize=7, fontName='Helvetica',
        textColor=GRIS_MEDIO, alignment=TA_CENTER,
    )
    custom['img_caption'] = ParagraphStyle(
        'ImgCaption', parent=styles['Normal'],
        fontSize=8, fontName='Helvetica-Oblique',
        textColor=GRIS_MEDIO, alignment=TA_CENTER,
        spaceBefore=2, spaceAfter=8,
    )

    return custom


def escape_html(text):
    """Escape HTML special chars but preserve our tags."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


def inline_format(text):
    """Convert markdown inline formatting to ReportLab XML."""
    # Bold+Italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<font face="Courier" size="8" color="#1E3A8A">\1</font>', text)
    return text


def parse_table(lines):
    """Parse markdown table lines into header + rows."""
    if len(lines) < 2:
        return None, None

    def split_row(line):
        cells = [c.strip() for c in line.strip('|').split('|')]
        return cells

    header = split_row(lines[0])
    # Skip separator line (lines[1])
    rows = []
    for line in lines[2:]:
        if line.strip():
            rows.append(split_row(line))

    return header, rows


def build_table(header, rows, styles, page_width):
    """Build a ReportLab Table from parsed markdown table."""
    ncols = len(header)
    col_width = (page_width - 1*cm) / ncols
    col_widths = [col_width] * ncols

    # Build data
    data = []
    header_row = [Paragraph(inline_format(h), styles['table_header']) for h in header]
    data.append(header_row)

    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            cell_text = inline_format(cell)
            # Center columns that look like Si/No or symbols
            if cell.strip() in ('Si', 'No', '—'):
                cells.append(Paragraph(cell_text, styles['table_cell_center']))
            else:
                cells.append(Paragraph(cell_text, styles['table_cell']))
        # Pad if needed
        while len(cells) < ncols:
            cells.append(Paragraph('', styles['table_cell']))
        data.append(cells)

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL),
        ('TEXTCOLOR', (0, 0), (-1, 0), BLANCO),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLANCO, GRIS_CLARO]),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 0.5, GRIS_BORDE),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, GRIS_BORDE),
    ]))
    return table


def add_page_number(canvas, doc):
    """Footer with page number."""
    canvas.saveState()
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(GRIS_MEDIO)
    canvas.drawCentredString(
        letter[0] / 2, 1.2*cm,
        f"Smart Project Management — Manual de Usuario v1.0 | Pág. {doc.page}"
    )
    # Top line
    canvas.setStrokeColor(GRIS_BORDE)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, letter[1] - 1.5*cm, letter[0] - 2*cm, letter[1] - 1.5*cm)
    canvas.restoreState()


def build_pdf():
    print("Leyendo MANUAL_USUARIO.md...")
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_content = f.read()

    lines = md_content.split('\n')
    styles = create_styles()
    story = []
    page_width = letter[0] - 4*cm  # usable width

    # ─── PORTADA ───────────────────────────────────────────
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("Smart Project Management", styles['titulo_doc']))
    story.append(Paragraph("Manual de Usuario v1.0", styles['subtitulo_doc']))
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=3, color=AZUL, spaceAfter=12))
    story.append(Paragraph("Sistema para Industrias Técnicas Barquisimeto, C.A. (I.T.B.C.A.)", styles['subtitulo_doc']))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Versión MVP 1.0 | Marzo 2026", styles['version']))
    story.append(Paragraph("Desarrollado por SmartSolutions VE", styles['version']))
    story.append(Paragraph("Simón Briceño &amp; Javier Figueroa", styles['version']))
    story.append(Spacer(1, 3*cm))

    # Info box
    info_data = [
        [Paragraph('<b>URL de acceso:</b>', styles['table_cell']),
         Paragraph('<font face="Courier">http://127.0.0.1:8080/auth/login/</font>', styles['table_cell'])],
        [Paragraph('<b>Usuario demo:</b>', styles['table_cell']),
         Paragraph('<font face="Courier">valmore</font> / <font face="Courier">itbca2026</font>', styles['table_cell'])],
        [Paragraph('<b>Rol:</b>', styles['table_cell']),
         Paragraph('Administrador (acceso completo)', styles['table_cell'])],
    ]
    info_table = Table(info_data, colWidths=[4*cm, page_width - 4*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), AZUL_FONDO),
        ('BOX', (0, 0), (-1, -1), 1, AZUL),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(info_table)
    story.append(PageBreak())

    # ─── PARSE MARKDOWN ────────────────────────────────────
    i = 0
    in_code_block = False
    code_buffer = []
    table_buffer = []
    in_table = False
    skip_until_toc_end = False

    while i < len(lines):
        line = lines[i]

        # Skip the first few header lines (already in cover page)
        if i < 6:
            i += 1
            continue

        # Skip TOC section
        if line.strip() == '## Tabla de Contenidos':
            skip_until_toc_end = True
            i += 1
            continue
        if skip_until_toc_end:
            if line.startswith('## ') and 'Contenidos' not in line:
                skip_until_toc_end = False
            elif line.startswith('---'):
                skip_until_toc_end = False
                i += 1
                continue
            else:
                i += 1
                continue

        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End code block
                code_text = '\n'.join(code_buffer)
                code_text = escape_html(code_text)
                code_text = code_text.replace('\n', '<br/>')
                story.append(Paragraph(code_text, styles['code']))
                code_buffer = []
                in_code_block = False
            else:
                # Flush table if pending
                if in_table and table_buffer:
                    header, rows = parse_table(table_buffer)
                    if header and rows:
                        story.append(build_table(header, rows, styles, page_width))
                        story.append(Spacer(1, 4))
                    table_buffer = []
                    in_table = False
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_buffer.append(line)
            i += 1
            continue

        # Table detection
        stripped = line.strip()
        if '|' in stripped and not stripped.startswith('```'):
            # Check if it's a table row
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            if len(cells) >= 2:
                # Check if separator row
                is_separator = all(re.match(r'^:?-+:?$', c.strip()) for c in cells if c.strip())
                if is_separator and table_buffer:
                    table_buffer.append(stripped)
                    i += 1
                    continue
                elif table_buffer and not is_separator:
                    table_buffer.append(stripped)
                    i += 1
                    continue
                elif not table_buffer:
                    # Flush any pending table
                    table_buffer = [stripped]
                    in_table = True
                    i += 1
                    continue

        # If we were in a table and this line is not a table row, flush
        if in_table and table_buffer:
            header, rows = parse_table(table_buffer)
            if header and rows:
                story.append(build_table(header, rows, styles, page_width))
                story.append(Spacer(1, 4))
            table_buffer = []
            in_table = False

        # Empty line
        if not stripped:
            i += 1
            continue

        # Horizontal rule
        if stripped == '---':
            story.append(HRFlowable(width="100%", thickness=0.5, color=GRIS_BORDE, spaceBefore=6, spaceAfter=6))
            i += 1
            continue

        # Headers
        if stripped.startswith('## '):
            title = stripped[3:].strip()
            title = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', title)  # Remove links
            story.append(Spacer(1, 6))
            story.append(HRFlowable(width="100%", thickness=2, color=AZUL, spaceAfter=4))
            story.append(Paragraph(escape_html(title).upper(), styles['h1']))
            i += 1
            continue

        if stripped.startswith('### '):
            title = stripped[4:].strip()
            story.append(Paragraph(inline_format(escape_html(title)), styles['h2']))
            i += 1
            continue

        if stripped.startswith('#### '):
            title = stripped[5:].strip()
            story.append(Paragraph(inline_format(escape_html(title)), styles['h3']))
            i += 1
            continue

        # Skip top-level header (already in cover)
        if stripped.startswith('# '):
            i += 1
            continue

        # Image
        img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', stripped)
        if img_match:
            alt_text = img_match.group(1)
            img_path = img_match.group(2)
            # Resolve path
            img_path = img_path.replace('%20', ' ')
            full_path = os.path.join(BASE_DIR, img_path)
            if os.path.exists(full_path):
                try:
                    img = Image(full_path)
                    # Scale to fit page width
                    aspect = img.imageWidth / img.imageHeight
                    img_width = min(page_width, 16*cm)
                    img_height = img_width / aspect
                    if img_height > 10*cm:
                        img_height = 10*cm
                        img_width = img_height * aspect
                    img.drawWidth = img_width
                    img.drawHeight = img_height
                    story.append(Spacer(1, 4))
                    story.append(img)
                    if alt_text:
                        story.append(Paragraph(escape_html(alt_text), styles['img_caption']))
                    else:
                        story.append(Spacer(1, 4))
                except Exception as e:
                    story.append(Paragraph(f'[Imagen: {escape_html(alt_text)}]', styles['note']))
            else:
                story.append(Paragraph(f'[Imagen no encontrada: {escape_html(img_path)}]', styles['note']))
            i += 1
            continue

        # Blockquote / Note
        if stripped.startswith('> '):
            note_text = stripped[2:].strip()
            note_text = inline_format(escape_html(note_text))
            story.append(Paragraph(note_text, styles['note']))
            i += 1
            continue

        # Bullet points
        if stripped.startswith('- ') or stripped.startswith('* '):
            text = stripped[2:].strip()
            text = inline_format(escape_html(text))
            story.append(Paragraph(f"• {text}", styles['bullet']))
            i += 1
            continue

        # Numbered list
        num_match = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if num_match:
            num = num_match.group(1)
            text = num_match.group(2).strip()
            text = inline_format(escape_html(text))
            story.append(Paragraph(f"<b>{num}.</b> {text}", styles['bullet']))
            i += 1
            continue

        # Sub-bullets
        if stripped.startswith('  - ') or stripped.startswith('   - '):
            text = stripped.strip()[2:].strip()
            text = inline_format(escape_html(text))
            bullet_style = ParagraphStyle(
                'SubBullet', parent=styles['bullet'],
                leftIndent=28, bulletIndent=18,
            )
            story.append(Paragraph(f"◦ {text}", bullet_style))
            i += 1
            continue

        # Regular paragraph
        text = inline_format(escape_html(stripped))
        # Skip lines that are just link references
        if not re.match(r'^\d+\.\s*\[', stripped):
            story.append(Paragraph(text, styles['body']))

        i += 1

    # Flush any remaining table
    if in_table and table_buffer:
        header, rows = parse_table(table_buffer)
        if header and rows:
            story.append(build_table(header, rows, styles, page_width))

    # ─── BUILD PDF ─────────────────────────────────────────
    print(f"Generando PDF en: {OUTPUT_PATH}")
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF generado exitosamente: {OUTPUT_PATH}")
    print(f"Tamaño: {os.path.getsize(OUTPUT_PATH) / 1024:.0f} KB")


if __name__ == '__main__':
    build_pdf()
