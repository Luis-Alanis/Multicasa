from flask import Blueprint, jsonify, send_file
from models.database import SessionLocal
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from services.casa_service import CasaService

ficha_bp = Blueprint('ficha_bp', __name__)

def get_db():
    """Helper para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass

@ficha_bp.route('/api/ficha-tecnica/<int:id_casa>/pdf', methods=['GET'])
def generar_ficha_tecnica_pdf(id_casa):
    casa = CasaService.obtener_por_id(id_casa)
    if not casa:
        return jsonify({'error': 'Casa no encontrada'}), 404
    
    # Crear el PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
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
    elements.append(Paragraph("FICHA TÉCNICA DE PROPIEDAD", title_style))
    elements.append(Paragraph(f"Bienes Raíces MultiCasa", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Información de la propiedad
    info_data = [
        ['Folio:', str(casa['id_casa'])],
        ['Locación:', str(casa.get('locacion', 'N/A'))],
        ['Código Postal:', str(casa.get('codigo_postal', 'N/A'))],
        ['', ''],
        ['CARACTERÍSTICAS', ''],
        ['Recámaras:', str(casa['recamaras'])],
        ['Baños:', str(casa['baños'])],
        ['', ''],
        ['UBICACIÓN', ''],
        ['Latitud:', str(casa.get('latitud', 'N/A'))],
        ['Longitud:', str(casa.get('longitud', 'N/A'))],
        ['', ''],
        ['PRECIO', ''],
        ['Costo:', f"${casa['costo']:,.2f}"],
        ['Estatus:', casa['estatus_venta']],
    ]
    
    # Crear tabla
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#134563')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#e8f4f8')),
        ('BACKGROUND', (0, 8), (-1, 8), colors.HexColor('#e8f4f8')),
        ('BACKGROUND', (0, 11), (-1, 11), colors.HexColor('#e8f4f8')),
        ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
        ('FONTNAME', (0, 8), (-1, 8), 'Helvetica-Bold'),
        ('FONTNAME', (0, 11), (-1, 11), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 4), (-1, 4), colors.HexColor('#134563')),
        ('TEXTCOLOR', (0, 8), (-1, 8), colors.HexColor('#134563')),
        ('TEXTCOLOR', (0, 11), (-1, 11), colors.HexColor('#134563')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0dde6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Pie de página
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph(
        f"Fecha de emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
        footer_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Bienes Raíces MultiCasa - Tu mejor opción en agencia de bienes raíces",
        footer_style
    ))
    elements.append(Paragraph(
        "Teléfono: 1-800-123-4567 | Email: multicasaserviciosbienesraices@gmail.com",
        footer_style
    ))
    
    # Construir el PDF
    doc.build(elements)
    
    # Preparar el buffer para enviar
    buffer.seek(0)
    
    # Nombre del archivo
    filename = f"ficha_tecnica_casa_{id_casa}_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )
    