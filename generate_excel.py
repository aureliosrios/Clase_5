import xlsxwriter

def create_wbs_template():
    # 1. Create a workbook
    workbook = xlsxwriter.Workbook("plantilla_wbs.xlsx")
    
    # 2. Define Styles / Formats
    # Header format for Title
    title_format = workbook.add_format({
        'bold': True,
        'font_name': 'Outfit',
        'font_size': 14,
        'font_color': '#ffffff',
        'bg_color': '#0f172a',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#1e293b'
    })
    
    # Header format for tables
    header_format = workbook.add_format({
        'bold': True,
        'font_name': 'Inter',
        'font_size': 11,
        'font_color': '#ffffff',
        'bg_color': '#0284c7',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#e2e8f0'
    })
    
    # Label format (bold slate)
    label_format = workbook.add_format({
        'bold': True,
        'font_name': 'Inter',
        'font_size': 10,
        'font_color': '#0f172a',
        'bg_color': '#f1f5f9',
        'align': 'left',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#cbd5e1'
    })
    
    # Value format (normal)
    value_format = workbook.add_format({
        'font_name': 'Inter',
        'font_size': 10,
        'font_color': '#0f172a',
        'align': 'left',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#e2e8f0'
    })

    # Code format (centered)
    code_format = workbook.add_format({
        'font_name': 'Inter',
        'font_size': 10,
        'font_color': '#475569',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#e2e8f0'
    })

    # Instruction format
    instruction_format = workbook.add_format({
        'font_name': 'Inter',
        'font_size': 10,
        'font_color': '#64748b',
        'italic': True,
        'align': 'left',
        'valign': 'top'
    })

    # 3. SHEET 1: CONFIGURACIÓN PROYECTO
    sheet_proj = workbook.add_worksheet("Proyecto")
    sheet_proj.set_zoom(110)
    sheet_proj.set_column("B:B", 26)
    sheet_proj.set_column("C:C", 38)
    
    # Grid lines visible
    sheet_proj.hide_gridlines(2)
    
    # Header block
    sheet_proj.merge_range("B2:C2", "CONFIGURACIÓN GENERAL DEL PROYECTO", title_format)
    sheet_proj.set_row(1, 35) # Height for header
    
    # General parameters
    proj_rows = [
        ("Nombre del Proyecto", "Vivienda Unifamiliar - Casa Campestre"),
        ("Frente / Sector General", "Frente Estructuras - Módulo A"),
        ("Supervisor Responsable", "Ing. Carlos Mendoza"),
        ("Google Apps Script WebApp URL", "SU_URL_DE_APPS_SCRIPT_AQUI")
    ]
    
    current_row = 3
    for label, val in proj_rows:
        sheet_proj.write(current_row, 1, label, label_format)
        sheet_proj.write(current_row, 2, val, value_format)
        sheet_proj.set_row(current_row, 24)
        current_row += 1
        
    # Instructions in sheet
    sheet_proj.write(8, 1, "Instrucciones de Uso:", label_format)
    sheet_proj.merge_range("B10:C13", 
        "1. Edite los campos superiores con los datos específicos de su nueva edificación.\n" +
        "2. En la pestaña 'WBS_Actividades' defina el listado oficial de tareas y ubicaciones.\n" +
        "3. Guarde este archivo Excel con el nombre exacto 'plantilla_wbs.xlsx' en su repositorio de GitHub.\n" +
        "4. El archivo index.html cargará automáticamente la información al iniciar la aplicación.", 
        instruction_format
    )

    # 4. SHEET 2: WBS ACTIVIDADES
    sheet_wbs = workbook.add_worksheet("WBS_Actividades")
    sheet_wbs.set_zoom(100)
    sheet_wbs.set_column("A:A", 14)
    sheet_wbs.set_column("B:B", 42)
    sheet_wbs.set_column("C:C", 28)
    sheet_wbs.set_column("D:D", 28)
    
    sheet_wbs.hide_gridlines(2)
    
    # Headers
    sheet_wbs.write(0, 0, "Código WBS", header_format)
    sheet_wbs.write(0, 1, "Descripción de la Actividad / Tarea", header_format)
    sheet_wbs.write(0, 2, "Sector / Ubicación Predeterminada", header_format)
    sheet_wbs.write(0, 3, "Notas de Control", header_format)
    sheet_wbs.set_row(0, 28)
    
    # Sample data representing residential housing WBS
    wbs_data = [
        ("1.1", "Limpieza y desbroce de terreno", "Terreno / Áreas Exteriores", "Preparación de la zona"),
        ("1.2", "Trazo, nivelación y replanteo", "Terreno / Áreas Exteriores", "Ejes y cotas oficiales"),
        ("2.1", "Excavación manual de zanjas", "Cimentaciones", "Profundidad según planos"),
        ("2.2", "Vaciado de solado e=2\"", "Cimentaciones", "Nivelación para zapatas"),
        ("2.3", "Habilitación e inst. de acero de zapatas", "Cimentaciones", "Acero corrugado grado 60"),
        ("2.4", "Vaciado de concreto en cimientos corridos", "Cimentaciones", "Concreto f'c=210 kg/cm2"),
        ("3.1", "Asentado de ladrillos de arcilla (Muro)", "Primer Piso", "Muro portante soga/cabeza"),
        ("3.2", "Encofrado de columnas de amarre", "Primer Piso", "Estanqueidad y plomada"),
        ("3.3", "Vaciado de columnas de amarre", "Primer Piso", "Vibrado mecánico"),
        ("4.1", "Instalaciones sanitarias de desagüe", "Pisos e Interiores", "Pendiente mínima de 1%"),
        ("4.2", "Canalización e inst. de cajas eléctricas", "Pisos y Muros", "Tuberías de PVC Conduit"),
        ("5.1", "Encofrado de vigas y losa aligerada", "Segundo Piso", "Apuntalamiento completo"),
        ("5.2", "Colocación de ladrillos de techo", "Segundo Piso", "Aligerado de 15cm"),
        ("5.3", "Instalaciones eléctricas en losa", "Segundo Piso", "Cajas octogonales y centros"),
        ("5.4", "Vaciado de concreto en losa aligerada", "Segundo Piso", "Curado inmediato con agua")
    ]
    
    row_idx = 1
    for wbs_code, desc, sector, notes in wbs_data:
        sheet_wbs.write(row_idx, 0, wbs_code, code_format)
        sheet_wbs.write(row_idx, 1, desc, value_format)
        sheet_wbs.write(row_idx, 2, sector, value_format)
        sheet_wbs.write(row_idx, 3, notes, value_format)
        sheet_wbs.set_row(row_idx, 22)
        row_idx += 1
        
    # Close Workbook
    workbook.close()
    print("Success: plantilla_wbs.xlsx has been created and styled successfully.")

if __name__ == "__main__":
    create_wbs_template()
