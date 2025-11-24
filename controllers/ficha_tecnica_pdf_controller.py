from flask import Blueprint, session, jsonify, send_file
from models.casa_model import Casa
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

ficha_bp = Blueprint('ficha_bp', __name__)

@ficha_bp.route('/api/ficha-tecnica/<int:id_casa>/pdf', methods=['GET'])
def generar_ficha_tecnica_pdf(id_casa):
    try:
        # Obtener la casa
        casa_model = Casa()
        casa = casa_model.obtener_por_id(id_casa)
        
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
            ['Locación:', str(casa['locacion'])],
            ['Código Postal:', str(casa.get('codigo_postal', 'N/A'))],
            ['', ''],
            ['CARACTERÍSTICAS', ''],
            ['Precio:', f"${float(casa['costo']):,.2f} MXN"],
            ['Recámaras:', str(casa['recamaras'])],
            ['Baños:', str(casa['baños'])],
            ['Estatus:', str(casa['estatus_venta'])],
            ['', ''],
            ['UBICACIÓN', ''],
            ['Latitud:', str(casa['latitud'])],
            ['Longitud:', str(casa['longitud'])],
        ]
        
        info_table = Table(info_data, colWidths=[2.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            # Encabezados de sección
            ('BACKGROUND', (0, 4), (1, 4), colors.HexColor('#134563')),
            ('TEXTCOLOR', (0, 4), (1, 4), colors.whitesmoke),
            ('FONTNAME', (0, 4), (1, 4), 'Helvetica-Bold'),
            ('ALIGN', (0, 4), (1, 4), 'CENTER'),
            
            ('BACKGROUND', (0, 10), (1, 10), colors.HexColor('#134563')),
            ('TEXTCOLOR', (0, 10), (1, 10), colors.whitesmoke),
            ('FONTNAME', (0, 10), (1, 10), 'Helvetica-Bold'),
            ('ALIGN', (0, 10), (1, 10), 'CENTER'),
            
            # Etiquetas
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#134563')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            
            # Valores
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#333333')),
            
            # General
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0dde6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            
            # Filas vacías
            ('GRID', (0, 3), (1, 3), 0, colors.white),
            ('GRID', (0, 9), (1, 9), 0, colors.white),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Pie de página
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#999999'),
            alignment=TA_CENTER
        )
        
        elements.append(Paragraph(f"Fecha de emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}", footer_style))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("Bienes Raíces MultiCasa © 2025 - Todos los derechos reservados", footer_style))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("Para más información contacte: 1-800-123-4567 | multicasa@gmail.com", footer_style))
        
        # Construir el PDF
        doc.build(elements)
        
        # Preparar el buffer para enviar
        buffer.seek(0)
        
        # Nombre del archivo
        filename = f"ficha_tecnica_casa_{id_casa}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        print(f"Error al generar ficha técnica PDF: {str(e)}")
        return jsonify({'error': f'Error al generar la ficha técnica: {str(e)}'}), 500