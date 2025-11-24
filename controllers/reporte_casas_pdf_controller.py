from flask import Blueprint, session, jsonify, send_file
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
from services.casa_service import CasaService

reporte_bp = Blueprint('reporte_bp', __name__)

@reporte_bp.route('/api/reporte/casas-pdf', methods=['GET'])
def generar_reporte_casas_pdf():
    """Generar reporte PDF de todas las casas (solo para admin)"""
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    todas_casas = CasaService.obtener_todas(incluir_vendidas=True)
        
    # Crear el PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Contenedor para los elementos del PDF
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#134563'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#666666'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    # Título
    elements.append(Paragraph("REPORTE DE PROPIEDADES", title_style))
    elements.append(Paragraph(f"Bienes Raíces MultiCasa", subtitle_style))
    elements.append(Paragraph(
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
        subtitle_style
    ))
    elements.append(Spacer(1, 0.3*inch))
    
    # Resumen
    total_casas = len(todas_casas)
    en_venta = sum(1 for c in todas_casas if c['estatus_venta'] == 'En Venta')
    vendidas = total_casas - en_venta
    
    resumen_data = [
        ['RESUMEN GENERAL', ''],
        ['Total de Propiedades:', str(total_casas)],
        ['En Venta:', str(en_venta)],
        ['Vendidas:', str(vendidas)],
    ]
    
    resumen_table = Table(resumen_data, colWidths=[3*inch, 2*inch])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#134563')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0dde6')),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(resumen_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Tabla de casas
    casas_data = [['ID', 'Locación', 'C.P.', 'Recám.', 'Baños', 'Costo', 'Estatus']]
    
    for casa in todas_casas:
        casas_data.append([
            str(casa['id_casa']),
            casa.get('locacion', 'N/A')[:20],
            casa.get('codigo_postal', 'N/A'),
            str(casa['recamaras']),
            str(casa['baños']),
            f"${casa['costo']:,.0f}",
            casa['estatus_venta']
        ])
    
    casas_table = Table(casas_data, colWidths=[0.5*inch, 1.8*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.5*inch, 1*inch])
    casas_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#134563')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d0dde6')),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    # Alternar colores de fila
    for i in range(1, len(casas_data)):
        if i % 2 == 0:
            casas_table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8f9fa'))
            ]))
    
    elements.append(casas_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Pie de página
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER
    )
    
    elements.append(Paragraph("Bienes Raíces MultiCasa © 2025 - Todos los derechos reservados", footer_style))
    
    # Construir el PDF
    doc.build(elements)
    
    # Preparar el buffer para enviar
    buffer.seek(0)
    
    # Nombre del archivo con fecha
    filename = f"reporte_casas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )