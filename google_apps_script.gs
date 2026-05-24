/**
 * Google Apps Script - Sincronizador de Reporte Diario de Obra (Dual: Producción & HSE)
 * 
 * Este script actúa como una API Webhook que recibe el payload del RDO móvil.
 * Dependiendo del tipo de reporte ('production' o 'safety'), registra y organiza la
 * información en 4 pestañas profesionales de Google Sheets:
 * 
 * 1. R_Produccion: Datos de cabecera de producción y restricciones ligadas al EDT/WBS.
 * 2. R_Seguridad: Datos de cabecera de seguridad y control general del sitio (HSE).
 * 3. Detalle_Actividades: Desglose de avance físico por actividad del EDT (EV).
 * 4. Detalle_Recursos: Consumo de recursos de Mano de Obra, Materiales y Equipos (AC).
 * 
 * Las pestañas se crean automáticamente si no existen, con formatos premium y colores HSL.
 */

function doPost(e) {
  try {
    // 1. Obtener y parsear los datos recibidos del RDO
    var data = JSON.parse(e.postData.contents);
    var reportType = data.report_type || "production";
    
    // 2. Obtener el Spreadsheet activo
    var sheetApp = SpreadsheetApp.getActiveSpreadsheet();
    
    // 3. Generar ID único para el reporte (REP-YYYYMMDD-HHMMSS)
    var timestamp = new Date();
    var dateString = Utilities.formatDate(timestamp, Session.getScriptTimeZone(), "yyyyMMdd-HHmmss");
    var reportId = (reportType === "production" ? "PROD-" : "SAFE-") + dateString;
    var formattedEnvio = Utilities.formatDate(timestamp, Session.getScriptTimeZone(), "dd/MM/yyyy HH:mm:ss");
    var dateFormatted = formatDateString(data.fecha);

    // 4. Inicializar u obtener las pestañas del sistema
    
    // Pestaña de Cabecera de Producción (Acero Oscuro / Azul)
    var prodHeaderSheet = getOrCreateSheet(sheetApp, "R_Produccion", [
      "ID Reporte", "Fecha Envío", "Fecha Reporte", "Supervisor/Ingeniero", "Turno", 
      "Clima Mañana", "Clima Tarde", "Horas Efectivas", "Capítulo WBS ID", "Capítulo WBS Nombre", 
      "Conflictos/Restricciones", "Trabajos Mañana", "Observaciones Generales"
    ], "#1e293b");
    
    // Pestaña de Cabecera de Seguridad (Esmeralda / Verde)
    var safetyHeaderSheet = getOrCreateSheet(sheetApp, "R_Seguridad", [
      "ID Reporte", "Fecha Envío", "Fecha Reporte", "Supervisor/Ingeniero", "Turno", 
      "Clima Mañana", "Clima Tarde", "Personal Total en Obra", "Inspecciones Realizadas", 
      "Detalle Inspecciones", "Accidentes/Incidentes", "Observaciones Generales"
    ], "#047857");
    
    // Pestaña de Detalle de Actividades (Gris / Azul)
    var actDetailSheet = getOrCreateSheet(sheetApp, "Detalle_Actividades", [
      "ID Reporte", "Fecha Reporte", "Supervisor/Ingeniero", "Capítulo WBS ID", 
      "Actividad WBS ID", "Nombre Actividad", "Unidad", "Meta del Día", "Cantidad Ejecutada", 
      "Avance Estimado", "Observación/Comentario"
    ], "#334155");
    
    // Pestaña de Detalle de Recursos (Índigo)
    var resDetailSheet = getOrCreateSheet(sheetApp, "Detalle_Recursos", [
      "ID Reporte", "Fecha Reporte", "Supervisor/Ingeniero", "Tipo Recurso", 
      "Capítulo WBS ID", "ID Recurso", "Descripción Recurso", "Categoría/Detalle", 
      "Unidad", "Cantidad Registrada"
    ], "#4338ca");

    // 5. Registrar información según el tipo de reporte
    
    if (reportType === "production") {
      // Registrar Cabecera de Producción
      var globalEdt = data.global_edt || { id_wbs: "", nombre_actividad: "" };
      prodHeaderSheet.appendRow([
        reportId,
        formattedEnvio,
        dateFormatted,
        data.responsable || "",
        data.turno || "",
        data.clima_manana || "",
        data.clima_tarde || "",
        data.horas_efectivas || 0,
        globalEdt.id_wbs || "",
        globalEdt.nombre_actividad || "",
        data.conflictos || "",
        data.trabajos_siguiente_dia || "",
        data.observaciones || ""
      ]);
      
      // Registrar fila por fila las Actividades (Físico - EV)
      if (data.actividades && data.actividades.length > 0) {
        data.actividades.forEach(function(act) {
          if (act.id_wbs) {
            actDetailSheet.appendRow([
              reportId,
              dateFormatted,
              data.responsable || "",
              globalEdt.id_wbs || "",
              act.id_wbs,
              act.nombre || "",
              act.unidad || "",
              act.meta_dia || "",
              act.cantidad_ejecutada || 0,
              act.avance_estimado || "0%",
              act.observacion || ""
            ]);
          }
        });
      }
      
      // Registrar Recursos (Mano de Obra, Materiales y Equipos - AC)
      
      // Mano de Obra
      if (data.mano_obra && data.mano_obra.length > 0) {
        data.mano_obra.forEach(function(res) {
          if (res.id_recurso) {
            resDetailSheet.appendRow([
              reportId,
              dateFormatted,
              data.responsable || "",
              "Mano de Obra",
              globalEdt.id_wbs || "",
              res.id_recurso,
              res.descripcion || "",
              res.categoria || "",
              res.unidad || "H-H",
              res.cantidad || 0
            ]);
          }
        });
      }
      
      // Materiales
      if (data.materiales && data.materiales.length > 0) {
        data.materiales.forEach(function(res) {
          if (res.id_recurso) {
            resDetailSheet.appendRow([
              reportId,
              dateFormatted,
              data.responsable || "",
              "Materiales",
              globalEdt.id_wbs || "",
              res.id_recurso,
              res.descripcion || "",
              res.tipo || "",
              res.unidad || "",
              res.cantidad || 0
            ]);
          }
        });
      }
      
      // Equipos
      if (data.equipos && data.equipos.length > 0) {
        data.equipos.forEach(function(res) {
          if (res.id_recurso) {
            resDetailSheet.appendRow([
              reportId,
              dateFormatted,
              data.responsable || "",
              "Equipos",
              globalEdt.id_wbs || "",
              res.id_recurso,
              res.descripcion || "",
              res.tipo || "",
              res.unidad || "",
              res.cantidad || 0
            ]);
          }
        });
      }
      
    } else if (reportType === "safety") {
      // Registrar Cabecera de Seguridad (HSE Global)
      safetyHeaderSheet.appendRow([
        reportId,
        formattedEnvio,
        dateFormatted,
        data.responsable || "",
        data.turno || "",
        data.clima_manana || "",
        data.clima_tarde || "",
        data.personal_total || 0,
        data.inspecciones_seguridad ? "SÍ" : "NO",
        data.detalle_inspecciones || "",
        data.accidentes || "",
        data.observaciones || ""
      ]);
    }

    // 6. Retornar éxito
    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      reportId: reportId,
      reportType: reportType
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    // Retornar error estructurado en caso de falla
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Busca una pestaña por nombre. Si no existe, la crea con las cabeceras y color provistos.
 */
function getOrCreateSheet(sheetApp, name, headers, headerColor) {
  var sheet = sheetApp.getSheetByName(name);
  if (!sheet) {
    sheet = sheetApp.insertSheet(name);
    sheet.appendRow(headers);
    
    // Formato premium a la cabecera
    var headerRange = sheet.getRange(1, 1, 1, headers.length);
    headerRange.setBackground(headerColor || "#1e293b")
               .setFontColor("#ffffff")
               .setFontWeight("bold")
               .setHorizontalAlignment("center");
    
    // Auto-ajustar ancho de las columnas
    for (var i = 1; i <= headers.length; i++) {
      sheet.autoResizeColumn(i);
    }
    
    sheet.setFrozenRows(1);
  }
  return sheet;
}

/**
 * Formatea fechas ISO "YYYY-MM-DD" a "DD/MM/YYYY" para presentación en Sheet
 */
function formatDateString(isoString) {
  if (!isoString) return "";
  var parts = isoString.split("-");
  if (parts.length === 3) {
    return parts[2] + "/" + parts[1] + "/" + parts[0];
  }
  return isoString;
}
