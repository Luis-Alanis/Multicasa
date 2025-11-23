from flask import Blueprint, session, jsonify, send_file
from models.casa_model import Casa
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

reporte_bp = Blueprint('reporte_bp', __name__)

@reporte_bp.route('/api/reporte/casas-pdf', methods=['GET'])
def generar_reporte_casas_pdf():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        # Obtener todas las casas
        casa = Casa()
        todas_casas = casa.obtener_todas()
        
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
            fontSize=12,
            textColor=colors.HexColor('#666666'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        # Título del reporte
        elements.append(Paragraph("REPORTE DE PROPIEDADES", title_style))
        elements.append(Paragraph(f"Bienes Raíces MultiCasa", subtitle_style))
        elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", subtitle_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Estadísticas generales
        total_casas = len(todas_casas)
        en_venta = sum(1 for c in todas_casas if c['estatus_venta'] == 'En Venta')
        vendidas = sum(1 for c in todas_casas if c['estatus_venta'] == 'Vendida')
        
        stats_data = [
            ['Total de Propiedades:', str(total_casas)],
            ['En Venta:', str(en_venta)],
            ['Vendidas:', str(vendidas)]
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 1.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#134563')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2a9fd6')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0dde6'))
        ]))
        
        elements.append(stats_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Tabla de casas
        # Encabezados
        data = [['ID', 'Locación', 'C.P.', 'Costo', 'Rec.', 'Baños', 'Estatus']]
        
        # Datos de las casas
        for casa_item in todas_casas:
            costo_formato = f"${float(casa_item['costo']):,.2f}"
            data.append([
                str(casa_item['id_casa']),
                str(casa_item['locacion'])[:25],  # Limitar longitud
                str(casa_item.get('codigo_postal', 'N/A')),
                costo_formato,
                str(casa_item['recamaras']),
                str(casa_item['baños']),
                str(casa_item['estatus_venta'])
            ])
        
        # Crear tabla
        table = Table(data, colWidths=[0.5*inch, 2.2*inch, 0.8*inch, 1.3*inch, 0.6*inch, 0.7*inch, 1.1*inch])
        
        # Estilo de la tabla
        table_style = TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#134563')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            
            # Cuerpo de la tabla
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # ID centrado
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Locación a la izquierda
            ('ALIGN', (2, 1), (-1, -1), 'CENTER'), # Resto centrado
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d0dde6')),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
        ])
        
        # Aplicar colores según estatus
        for i, casa_item in enumerate(todas_casas, start=1):
            if casa_item['estatus_venta'] == 'En Venta':
                table_style.add('TEXTCOLOR', (6, i), (6, i), colors.HexColor('#28a745'))
                table_style.add('FONTNAME', (6, i), (6, i), 'Helvetica-Bold')
            else:  # Vendida
                table_style.add('TEXTCOLOR', (6, i), (6, i), colors.HexColor('#dc3545'))
                table_style.add('FONTNAME', (6, i), (6, i), 'Helvetica-Bold')
        
        table.setStyle(table_style)
        elements.append(table)
        
        # Pie de página
        elements.append(Spacer(1, 0.4*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#999999'),
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
        
    except Exception as e:
        print(f"Error al generar PDF: {str(e)}")
        return jsonify({'error': f'Error al generar el reporte: {str(e)}'}), 500