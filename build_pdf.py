# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_elements(self, page_count):
        if self._pageNumber == 1:
            return
            
        self.saveState()
        
        # Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0f172a"))
        self.drawString(54, 750, "PROJECT CONTROL AI  |  AUTOMATION ENGINEER")
        
        logo_path = "Logotipo rev1.png"
        if os.path.exists(logo_path):
            self.drawImage(logo_path, 480, 742, height=16, width=80, preserveAspectRatio=True, mask='auto')
        
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 735, 558, 735)
        
        # Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(54, 40, "Guía Metodológica de Clase 4: Reportes Colaborativos en la Nube")
        
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(558, 40, page_str)
        self.line(54, 52, 558, 52)
        
        self.restoreState()


def build_manual_pdf():
    pdf_filename = "Manual_Clase_4_Colaborativo.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=80,
        bottomMargin=80
    )

    styles = getSampleStyleSheet()
    
    # Premium Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#0f172a"),
        alignment=1,
        spaceAfter=20
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#0284c7"),
        alignment=1,
        spaceAfter=40
    )
    
    meta_label_style = ParagraphStyle('MetaLabel', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=colors.HexColor("#475569"))
    meta_value_style = ParagraphStyle('MetaValue', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#0f172a"))
    
    h1_style = ParagraphStyle('SectionH1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor("#0f172a"), spaceBefore=24, spaceAfter=12, keepWithNext=True)
    h2_style = ParagraphStyle('SectionH2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor("#0284c7"), spaceBefore=16, spaceAfter=8, keepWithNext=True)
    h3_style = ParagraphStyle('SectionH3', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=colors.HexColor("#334155"), spaceBefore=12, spaceAfter=6, keepWithNext=True)
    
    body_style = ParagraphStyle('BodyTextCustom', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=15, textColor=colors.HexColor("#334155"), spaceAfter=12)
    bullet_style = ParagraphStyle('BulletCustom', parent=body_style, leftIndent=15, firstLineIndent=-10, spaceAfter=8)
    
    table_header_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.white, alignment=1)
    table_body_style = ParagraphStyle('TableBody', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor("#334155"))
    table_code_style = ParagraphStyle('TableCodeBody', parent=styles['Normal'], fontName='Courier', fontSize=8, leading=11, textColor=colors.HexColor("#1e293b"))
    table_bold_body_style = ParagraphStyle('TableBoldBody', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor("#0f172a"))

    story = []

    # --- COVER PAGE ---
    story.append(Spacer(1, 50))
    logo_path = "Logotipo rev1.png"
    if os.path.exists(logo_path):
        from reportlab.lib.utils import ImageReader
        img = ImageReader(logo_path)
        img_w, img_h = img.getSize()
        target_width = 2.8 * inch
        target_height = (img_h / img_w) * target_width
        story.append(Image(logo_path, width=target_width, height=target_height))
    else:
        story.append(Paragraph("<b>PROJECT CONTROL AI</b>", ParagraphStyle('P', fontSize=22, alignment=1, textColor=colors.HexColor("#0284c7"))))
        
    story.append(Spacer(1, 40))
    
    # Elegant Line
    d_line = Table([[""]], colWidths=[504])
    d_line.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0284c7")),
        ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0)
    ]))
    
    # Title properly wrapped with HTML entities
    story.append(Paragraph("MANUAL METODOL&Oacute;GICO Y<br/>GU&Iacute;A PASO A PASO", title_style))
    story.append(Paragraph("<b>Clase 4:</b> Automatización de Reportes Diarios Colaborativos en la Nube", subtitle_style))
    story.append(d_line)
    story.append(Spacer(1, 80))
    
    meta_data = [
        [Paragraph("Programa:", meta_label_style), Paragraph("Especialidad en Automation Engineer", meta_value_style)],
        [Paragraph("Módulo:", meta_label_style), Paragraph("Ingeniería de Control de Proyectos Aumentada (PCAI)", meta_value_style)],
        [Paragraph("Docente:", meta_label_style), Paragraph("Ing. Aurelio Solórzano Rios", meta_value_style)],
        [Paragraph("Fecha Oficial:", meta_label_style), Paragraph("Mayo de 2026", meta_value_style)],
        [Paragraph("Organización:", meta_label_style), Paragraph("Academia Project Control AI", meta_value_style)]
    ]
    
    meta_table = Table(meta_data, colWidths=[140, 364])
    meta_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    
    story.append(meta_table)
    story.append(PageBreak())

    # --- SECTION 1 ---
    story.append(Paragraph("1. OBJETIVOS DEL NEGOCIO Y TÉCNICOS", h1_style))
    story.append(Paragraph("<b>El Problema Tradicional en Obra</b>", h3_style))
    story.append(Paragraph("En la gestión de proyectos de construcción tradicionales, el flujo de información de campo sufre un grave cuello de botella:", body_style))
    story.append(Paragraph("• Los capataces y subcontratistas anotan el personal, materiales y avances en papeles físicos, libretas o incluso bolsas de cemento vacías al finalizar la jornada laboral (5:00 PM).", bullet_style))
    story.append(Paragraph("• El Ingeniero de Campo recibe estos apuntes físicos y pasa horas de trabajo manual (típicamente de 7:00 PM a 11:00 PM) copiando, digitando y formateando los datos en múltiples hojas de Excel.", bullet_style))
    story.append(Paragraph("• El Jefe de Obra o el Ingeniero de Control de Proyectos recibe estos reportes por separado tarde en la noche, teniendo que consolidarlos manualmente.", bullet_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>La Solución de la Clase 4</b>", h3_style))
    story.append(Paragraph("Desplegar una <b>aplicación web móvil responsiva en formato 9:16</b> alojada de forma gratuita en la nube. Los capataces, ingenieros de seguridad y controladores de calidad llenan sus reportes diarios en vivo directamente desde sus teléfonos móviles.", body_style))
    story.append(Paragraph("Los datos se envían de forma instantánea a una hoja de cálculo unificada en <b>Google Sheets</b> mediante un servicio ligero y gratuito de <b>Google Apps Script</b>. Finalmente, un script local de Python procesa los datos consolidados y genera tableros automatizados en segundos.", body_style))

    # --- SECTION 2 ---
    story.append(Paragraph("2. CRONOLOGÍA MINUTO A MINUTO (DESDE 32:00)", h1_style))
    
    story.append(Paragraph("Fase 1: Configuración Inicial e Interfaz Móvil (Minuto 32:00)", h2_style))
    story.append(Paragraph("• Aurelio guía a los alumnos a estructurar localmente la carpeta del proyecto en Windows (<code>Automation Engineer > 4ta Clase > Reporte diario</code>).", bullet_style))
    story.append(Paragraph("• Utilizando el primer prompt en <b>Antigravity</b>, se autogenera un maquetado responsivo en formato vertical 9:16.", bullet_style))
    story.append(Paragraph("• La interfaz cuenta con selectores de clima y turno, contadores de cuadrilla, sliders de progreso, checklist de incidentes y un canvas HTML5 para firmas digitales.", bullet_style))
    
    story.append(Paragraph("Fase 2: Migración Estratégica a Google Apps Script (Minuto 53:00)", h2_style))
    story.append(Paragraph("• Para evitar los costos y complejidad de las APIs de Google Cloud, el docente enseñó a usar <b>Google Apps Script</b>.", bullet_style))
    story.append(Paragraph("• Se creó un script que actúa como un receptor HTTP POST gratuito, parseando los datos estructurados en JSON e insertándolos fila por fila en tiempo real en un documento unificado de Google Sheets.", bullet_style))
    
    story.append(Paragraph("Fase 3: Alojamiento en la Nube con GitHub Pages (Minuto 01:21:00)", h2_style))
    story.append(Paragraph("• Los estudiantes crearon repositorios públicos en GitHub denominados <code>reporte-diario-obra</code>.", bullet_style))
    story.append(Paragraph("• Se enfatizó la regla de nombrar el archivo principal como <code>index.html</code>.", bullet_style))
    story.append(Paragraph("• Se activó la rama de producción en GitHub Pages para generar un enlace universal seguro.", bullet_style))
    
    story.append(Paragraph("Fase 4: Modularización y WBS desde Excel (Minuto 02:22:00)", h2_style))
    story.append(Paragraph("• A propuesta del alumno Guillermo Franleo, se modificó la app para desvincular el WBS del HTML.", bullet_style))
    story.append(Paragraph("• Antigravity reestructuró el código para integrar la librería <code>xlsx.js</code> y leer dinámicamente el archivo local <code>plantilla_wbs.xlsx</code>.", bullet_style))
    
    story.append(PageBreak())

    # --- SECTION 3 ---
    story.append(Paragraph("3. VAULT DE PROMPTS DE ANTIGRAVITY", h1_style))
    story.append(Paragraph("A continuación se compilan los prompts verbatim utilizados en la clase:", body_style))
    
    prompts_data = [
        [Paragraph("Fase / Objetivo", table_header_style), Paragraph("Prompt Verbatim de Antigravity (Español)", table_header_style)],
        [Paragraph("<b>Fase 1</b><br/>Maquetado UI Móvil", table_bold_body_style), Paragraph("Requiero hacer un reporte diario del avance de obra para un proyecto de edificación de vivienda unifamiliar. La idea es que este reporte sea en HTML y esté diseñado para los smartphones (celulares) de los colaboradores que están en obra. La información se vincule y descargue en Google Drive (Google Sheet). Por ahora, genera primero el archivo HTML con formato profesional, estructurado para celulares en formato 9:16.", table_code_style)],
        [Paragraph("<b>Fase 2</b><br/>Free Backend Sheets", table_bold_body_style), Paragraph("No quiero vincular a una API de pago. Solo quiero que uses Google Apps Script para pasar la información directamente desde el HTML index de GitHub a Google Sheets.", table_code_style)],
        [Paragraph("<b>Fase 3</b><br/>Git & GitHub Pages", table_bold_body_style), Paragraph("¿Puedes ayudarme a crear mi cuenta en GitHub y también a crear mi primer repositorio?", table_code_style)],
        [Paragraph("<b>Fase 4</b><br/>WBS Modular Excel", table_bold_body_style), Paragraph("Deseo que el archivo index trabaje conjuntamente con un archivo Excel (plantilla_wbs.xlsx). Es decir, la aplicación debe ser genérica. En el archivo Excel se tiene que definir el WBS (EDT) y la descripción de las actividades, y el archivo index debe tomar dicha información y mostrarla al equipo del proyecto. De modo que si cambio de proyecto, solo tengo que actualizar el archivo Excel y el index se adaptará a otro proyecto similar. Como entregable, deseo el index actualizado y el Excel formateado (plantilla_wbs.xlsx).", table_code_style)]
    ]
    
    prompt_table = Table(prompts_data, colWidths=[110, 394])
    prompt_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(prompt_table)
    story.append(Spacer(1, 20))

    # --- SECTION 4 ---
    story.append(Paragraph("4. TABLA DE DUDAS Y RESOLUCIONES", h1_style))
    
    qa_data = [
        [Paragraph("Alumno", table_header_style), Paragraph("Consulta / Problema", table_header_style), Paragraph("Resolución del Docente", table_header_style)],
        [Paragraph("<b>César Aguedo</b>", table_bold_body_style), Paragraph("Bloqueo de Antigravity en local con alerta: <i>'Agent Terminated with Error'</i>.", table_body_style), Paragraph("Usar el <b>botón azul de retroceso</b> en el chat para limpiar caché fallida. Si persiste, reiniciar el agente.", table_body_style)],
        [Paragraph("<b>Luis Pariona</b>", table_bold_body_style), Paragraph("Falta del lienzo de firma digital en el código de la IA.", table_body_style), Paragraph("Se explicó el <b>comportamiento estocástico</b> de los LLMs. Se corrige con un prompt de seguimiento.", table_body_style)],
        [Paragraph("<b>Guillermo Franleo</b>", table_bold_body_style), Paragraph("Error `404 Page Not Found` en GitHub Pages.", table_body_style), Paragraph("Subió el archivo en mayúsculas. GitHub busca estrictamente <code>index.html</code> en minúsculas.", table_body_style)],
        [Paragraph("<b>Wilber Carbajal</b>", table_bold_body_style), Paragraph("Zonas sin conexión a Internet.", table_body_style), Paragraph("El HTML es local. El capataz reporta sin internet; el envío a Sheets se sincroniza al recuperar red.", table_body_style)]
    ]
    
    qa_table = Table(qa_data, colWidths=[90, 184, 230])
    qa_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(qa_table)
    story.append(Spacer(1, 20))

    # --- SECTION 5 ---
    story.append(KeepTogether([
        Paragraph("5. CASOS DE APLICACIÓN Y MONETIZACIÓN", h1_style),
        Paragraph("<b>Auditoría Automatizada (Wilber Carbajal):</b> Uso de IA multimodal para leer en bloque 30 PDFs diarios de InfoObras y autogenerar el acumulado de valorizaciones.", body_style),
        Paragraph("<b>Cruce de Planos 3D (Roberto Loayza):</b> Uso de Gemini Robotic para realizar lecturas de planos 2D en planta y elevación, traduciéndolo a un cómputo métrico tridimensional.", body_style)
    ]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Success: PDF manual successfully built.")

if __name__ == "__main__":
    build_manual_pdf()
