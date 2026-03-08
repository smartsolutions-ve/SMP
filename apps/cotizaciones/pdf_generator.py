"""
Generador de PDF para cotizaciones.
Requiere: pip install reportlab
Si reportlab no está disponible, pdf_view() en views.py retorna un error elegante.
"""
from decimal import Decimal
import datetime


def generar_pdf_cotizacion(cotizacion):
    """
    Genera un PDF de la cotización y retorna los bytes del PDF.
    Lanza ImportError si reportlab no está instalado.
    """
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
    from io import BytesIO

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    # Paleta de colores
    AZUL = colors.HexColor('#0066FF')
    AZUL_OSCURO = colors.HexColor('#1E3A8A')
    GRIS_OSCURO = colors.HexColor('#1E293B')
    GRIS_MEDIO = colors.HexColor('#475569')
    GRIS_CLARO = colors.HexColor('#F1F5F9')
    BLANCO = colors.white
    NEGRO = colors.HexColor('#0F172A')
    VERDE = colors.HexColor('#16A34A')

    styles = getSampleStyleSheet()

    # Estilos personalizados
    titulo_style = ParagraphStyle(
        'TituloEmpresa',
        parent=styles['Normal'],
        fontSize=16,
        fontName='Helvetica-Bold',
        textColor=AZUL_OSCURO,
        spaceAfter=2,
    )
    subtitulo_style = ParagraphStyle(
        'SubtituloEmpresa',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        textColor=GRIS_MEDIO,
        spaceAfter=2,
    )
    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica-Bold',
        textColor=GRIS_MEDIO,
        spaceAfter=1,
    )
    valor_style = ParagraphStyle(
        'Valor',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        textColor=NEGRO,
    )
    encabezado_tabla = ParagraphStyle(
        'EncabezadoTabla',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica-Bold',
        textColor=BLANCO,
        alignment=TA_CENTER,
    )
    celda_style = ParagraphStyle(
        'Celda',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica',
        textColor=NEGRO,
    )
    terminos_style = ParagraphStyle(
        'Terminos',
        parent=styles['Normal'],
        fontSize=7.5,
        fontName='Helvetica',
        textColor=GRIS_MEDIO,
        leading=11,
    )
    total_label_style = ParagraphStyle(
        'TotalLabel',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica-Bold',
        textColor=GRIS_OSCURO,
        alignment=TA_RIGHT,
    )
    total_valor_style = ParagraphStyle(
        'TotalValor',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica-Bold',
        textColor=NEGRO,
        alignment=TA_RIGHT,
    )

    empresa = cotizacion.empresa
    story = []
    ancho_util = letter[0] - 4*cm  # 17.59 cm aprox

    # ─── ENCABEZADO ─────────────────────────────────────────────
    datos_empresa_izq = [
        [Paragraph(empresa.nombre, titulo_style)],
        [Paragraph(f"RIF: {empresa.rif}", subtitulo_style)],
    ]
    if empresa.direccion:
        datos_empresa_izq.append([Paragraph(empresa.direccion, subtitulo_style)])
    if empresa.telefono:
        datos_empresa_izq.append([Paragraph(f"Tel: {empresa.telefono}", subtitulo_style)])
    if empresa.email:
        datos_empresa_izq.append([Paragraph(empresa.email, subtitulo_style)])

    num_cot_style = ParagraphStyle(
        'NumCot',
        parent=styles['Normal'],
        fontSize=22,
        fontName='Helvetica-Bold',
        textColor=AZUL,
        alignment=TA_RIGHT,
    )
    fecha_cot_style = ParagraphStyle(
        'FechaCot',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        textColor=GRIS_MEDIO,
        alignment=TA_RIGHT,
    )
    tabla_encabezado_data = [[
        Table(datos_empresa_izq, colWidths=[ancho_util * 0.6]),
        Table([
            [Paragraph(cotizacion.numero, num_cot_style)],
            [Paragraph(f"Fecha: {cotizacion.fecha_creacion.strftime('%d/%m/%Y')}", fecha_cot_style)],
            [Paragraph(f"Vence: {cotizacion.fecha_vencimiento.strftime('%d/%m/%Y') if cotizacion.fecha_vencimiento else 'N/A'}", fecha_cot_style)],
            [Paragraph(f"Estado: {cotizacion.get_estado_display()}", fecha_cot_style)],
        ], colWidths=[ancho_util * 0.4]),
    ]]
    tabla_encabezado = Table(tabla_encabezado_data, colWidths=[ancho_util * 0.6, ancho_util * 0.4])
    tabla_encabezado.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(tabla_encabezado)
    story.append(HRFlowable(width="100%", thickness=2, color=AZUL, spaceAfter=8))

    # ─── DATOS CLIENTE ───────────────────────────────────────────
    datos_cliente = [
        [Paragraph('CLIENTE:', label_style), Paragraph(cotizacion.cliente_nombre or '—', valor_style)],
        [Paragraph('PROYECTO:', label_style), Paragraph(cotizacion.nombre_proyecto or '—', valor_style)],
    ]
    if cotizacion.cliente_contacto:
        datos_cliente.append([Paragraph('CONTACTO:', label_style), Paragraph(cotizacion.cliente_contacto, valor_style)])
    if cotizacion.ubicacion:
        datos_cliente.append([Paragraph('UBICACIÓN:', label_style), Paragraph(cotizacion.ubicacion, valor_style)])

    tabla_cliente = Table(datos_cliente, colWidths=[2.5*cm, ancho_util - 2.5*cm])
    tabla_cliente.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GRIS_CLARO),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [GRIS_CLARO, BLANCO]),
    ]))
    story.append(tabla_cliente)
    story.append(Spacer(1, 12))

    # ─── DESCRIPCIÓN ─────────────────────────────────────────────
    if cotizacion.descripcion:
        desc_style = ParagraphStyle(
            'Desc',
            parent=styles['Normal'],
            fontSize=8.5,
            fontName='Helvetica',
            textColor=GRIS_OSCURO,
            leading=12,
            spaceAfter=8,
        )
        story.append(Paragraph(cotizacion.descripcion, desc_style))

    # ─── TABLA DE PARTIDAS ────────────────────────────────────────
    col_widths = [1.2*cm, 7.5*cm, 2.0*cm, 1.5*cm, 2.3*cm, 2.7*cm]
    # Ajustar si hay demasiado espacio
    header_data = [
        Paragraph('#', encabezado_tabla),
        Paragraph('DESCRIPCIÓN', encabezado_tabla),
        Paragraph('CATEGORÍA', encabezado_tabla),
        Paragraph('UND', encabezado_tabla),
        Paragraph('CANTIDAD', encabezado_tabla),
        Paragraph('PRECIO UNIT.', encabezado_tabla),
        # No mostramos subtotal por ítem en este diseño simplificado
    ]
    # Incluimos SUBTOTAL
    col_widths = [0.8*cm, 6.5*cm, 2.2*cm, 1.3*cm, 1.8*cm, 2.2*cm, 2.7*cm]
    header_data = [
        Paragraph('#', encabezado_tabla),
        Paragraph('DESCRIPCIÓN', encabezado_tabla),
        Paragraph('CATEGORÍA', encabezado_tabla),
        Paragraph('UND', encabezado_tabla),
        Paragraph('CANT.', encabezado_tabla),
        Paragraph('P. UNIT.', encabezado_tabla),
        Paragraph('SUBTOTAL', encabezado_tabla),
    ]
    tabla_data = [header_data]

    for i, p in enumerate(cotizacion.partidas.all().order_by('orden'), 1):
        fila_style = ParagraphStyle(
            f'CeldaFila{i}',
            parent=celda_style,
            textColor=NEGRO if i % 2 == 1 else GRIS_OSCURO,
        )
        fila_mono = ParagraphStyle(
            f'CeldaMono{i}',
            parent=celda_style,
            fontName='Courier',
            fontSize=8,
            alignment=TA_RIGHT,
        )
        tabla_data.append([
            Paragraph(str(i), ParagraphStyle('num', parent=celda_style, alignment=TA_CENTER)),
            Paragraph(p.descripcion, fila_style),
            Paragraph(p.categoria or '', ParagraphStyle('cat', parent=celda_style, fontSize=7, textColor=GRIS_MEDIO)),
            Paragraph(p.unidad or '', ParagraphStyle('und', parent=celda_style, alignment=TA_CENTER)),
            Paragraph(f"{p.cantidad:,.4f}", fila_mono),
            Paragraph(f"${p.precio_unitario:,.2f}", fila_mono),
            Paragraph(f"${p.subtotal:,.2f}", fila_mono),
        ])

    tabla_partidas = Table(tabla_data, colWidths=col_widths, repeatRows=1)
    tabla_partidas.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), AZUL),
        ('TEXTCOLOR', (0, 0), (-1, 0), BLANCO),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        # Filas alternadas
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLANCO, GRIS_CLARO]),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Borde general
        ('BOX', (0, 0), (-1, -1), 0.5, GRIS_MEDIO),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#E2E8F0')),
    ]))
    story.append(tabla_partidas)
    story.append(Spacer(1, 10))

    # ─── TOTALES ─────────────────────────────────────────────────
    margen_utilidad = cotizacion.margen_utilidad_porcentaje or Decimal('0')
    totales_data = [
        ['', Paragraph('Subtotal:', total_label_style), Paragraph(f"${cotizacion.subtotal:,.2f}", total_valor_style)],
        ['', Paragraph(f"Utilidad ({margen_utilidad}%):", total_label_style), Paragraph(f"${cotizacion.utilidad_monto:,.2f}", total_valor_style)],
        ['', Paragraph('TOTAL USD:', ParagraphStyle('TotalGrande', parent=total_label_style, fontSize=11, textColor=AZUL_OSCURO)), Paragraph(f"${cotizacion.total:,.2f}", ParagraphStyle('TotalGrandeVal', parent=total_valor_style, fontSize=11, textColor=AZUL))],
    ]
    tabla_totales = Table(totales_data, colWidths=[ancho_util - 6.5*cm, 3.5*cm, 3.0*cm])
    tabla_totales.setStyle(TableStyle([
        ('BACKGROUND', (1, 0), (-1, 1), GRIS_CLARO),
        ('BACKGROUND', (1, 2), (-1, 2), colors.HexColor('#EFF6FF')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('LINEABOVE', (1, 2), (-1, 2), 1.5, AZUL),
        ('BOX', (1, 0), (-1, -1), 0.5, GRIS_MEDIO),
    ]))
    story.append(tabla_totales)
    story.append(Spacer(1, 14))

    # ─── TÉRMINOS Y CONDICIONES ───────────────────────────────────
    if cotizacion.terminos_condiciones:
        story.append(HRFlowable(width="100%", thickness=0.5, color=GRIS_MEDIO, spaceAfter=6))
        story.append(Paragraph("TÉRMINOS Y CONDICIONES", label_style))
        story.append(Spacer(1, 3))
        for linea in cotizacion.terminos_condiciones.split('\n'):
            linea = linea.strip()
            if linea:
                story.append(Paragraph(f"• {linea}", terminos_style))

    # ─── PIE DE PÁGINA ────────────────────────────────────────────
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GRIS_MEDIO, spaceAfter=4))
    pie_style = ParagraphStyle(
        'Pie',
        parent=styles['Normal'],
        fontSize=7,
        fontName='Helvetica',
        textColor=GRIS_MEDIO,
        alignment=TA_CENTER,
    )
    story.append(Paragraph(
        f"{empresa.nombre} | RIF: {empresa.rif} | Generado el {datetime.date.today().strftime('%d/%m/%Y')}",
        pie_style,
    ))

    doc.build(story)
    return buffer.getvalue()
