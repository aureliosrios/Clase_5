# Diccionario de Datos — Bases de Datos CSV

## Proyecto: Edificación Residencial "Los Cedros"

Este documento describe la estructura, organización y significado de cada columna de las cuatro bases de datos en formato CSV que alimentan el sistema **RDO - Reporte Diario de Obra con EVM**. Estas bases de datos deben ser cargadas por el usuario a través del botón "Cargar Bases de Datos" en la sección de cabecera del formulario, o bien se sirven desde la carpeta `/data/` si se despliega en GitHub Pages.

---

## 1. BD_EDT.csv — Estructura de Desglose del Trabajo (WBS)

### Descripción general

La base de datos **BD_EDT** contiene la Estructura de Desglose del Trabajo (WBS - Work Breakdown Structure) del proyecto. Define la jerarquía completa de actividades de construcción, desde el nivel raíz del proyecto hasta las actividades de último nivel (hojas), que son las unidades mínimas de control y seguimiento. La jerarquía se representa mediante códigos jerárquicos (id_wbs) y relaciones padre-hijo (padre_id), permitiendo al sistema agrupar costos y avances por capítulos de obra.

Esta es la base de datos principal, ya que de ella dependen tanto el cálculo del PV (Valor Planificado) como la selección de actividades en el formulario de EV (Valor Ganado). Solo las actividades de último nivel (hojas) con presupuesto mayor a cero son seleccionables para el reporte diario.

### Estructura del archivo

| Columna | Tipo de dato | Obligatorio | Descripción |
|---------|-------------|-------------|-------------|
| `id_wbs` | Texto | Sí | Código jerárquico único que identifica cada nodo del WBS. Usa notación decimal separada por puntos (ej: `1.0`, `1.1`, `2.3`, `3.5`). El nodo raíz del proyecto usa `0`. Los nodos de primer nivel usan formato `X.0` (ej: `1.0`, `2.0`), y las actividades hoja usan formato `X.Y` (ej: `1.1`, `2.3`, `3.5`). |
| `nombre_actividad` | Texto | Sí | Nombre descriptivo de la actividad o capítulo. Para nodos padre, describe el capítulo general (ej: "Obras Preliminares", "Cimentación"). Para nodos hoja, describe la actividad específica (ej: "Excavación masiva", "Concreto de columnas"). |
| `unidad` | Texto | Condicional | Unidad de medida de la actividad. Solo aplica para actividades hoja (nivel_wbs = 2). Los nodos padre y raíz dejan este campo vacío. Valores comunes: `m2` (metros cuadrados), `m3` (metros cúbicos), `kg` (kilogramos), `und` (unidades), `pto` (puntos), `glb` (global), `ml` (metros lineales). |
| `presupuesto_total` | Numérico | Sí | Presupuesto total asignado a la actividad en soles (S/). Para actividades hoja, contiene el monto presupuestado real (ej: `45600`, `85000`). Para nodos padre y raíz, el valor es `0` ya que su presupuesto se calcula como la suma de sus actividades hijas. |
| `fecha_inicio` | Fecha (YYYY-MM-DD) | Sí | Fecha de inicio planificada de la actividad. Para nodos padre, corresponde a la fecha de inicio más temprana entre sus hijas. Para nodos hoja, es la fecha en que se prevé iniciar la ejecución física de la actividad. Formato ISO 8601. |
| `fecha_fin` | Fecha (YYYY-MM-DD) | Sí | Fecha de finalización planificada de la actividad. Para nodos padre, corresponde a la fecha de fin más tardía entre sus hijas. Para nodos hoja, es la fecha en que se prevé completar la ejecución. La duración en días se calcula como `fecha_fin - fecha_inicio + 1`. |
| `nivel_wbs` | Entero | Sí | Nivel jerárquico dentro de la estructura WBS. `0` = nodo raíz (proyecto completo), `1` = capítulos principales, `2` = actividades de último nivel (hojas). Solo las actividades con nivel_wbs = 2 y presupuesto_total > 0 se muestran en el formulario de EV. |
| `padre_id` | Texto | Condicional | Código `id_wbs` del nodo padre en la jerarquía. Para el nodo raíz (id_wbs = 0), este campo está vacío. Para nodos de nivel 1, el padre es `0`. Para nodos de nivel 2, el padre es el código del capítulo correspondiente (ej: `1.0`, `2.0`, `3.0`). |

### Jerarquía del proyecto

```
0  Edificación Residencial "Los Cedros" (raíz)
├── 1.0  Obras Preliminares (capítulo)
│   ├── 1.1  Trazos y niveles (hoja)
│   ├── 1.2  Limpieza del terreno (hoja)
│   ├── 1.3  Movilización y desmovilización (hoja)
│   └── 1.4  Demoliciones (hoja)
├── 2.0  Cimentación (capítulo)
│   ├── 2.1  Excavación masiva (hoja)
│   ├── 2.2  Concreto de solado (hoja)
│   ├── 2.3  Encofrado de cimentación (hoja)
│   ├── 2.4  Acero de refuerzo cimentación (hoja)
│   └── 2.5  Concreto de cimentación (hoja)
├── 3.0  Estructura (capítulo)
│   ├── 3.1  Encofrado de columnas (hoja)
│   ├── 3.2  Acero de refuerzo columnas (hoja)
│   ├── 3.3  Concreto de columnas (hoja)
│   ├── 3.4  Encofrado de vigas y losas (hoja)
│   ├── 3.5  Acero de vigas y losas (hoja)
│   ├── 3.6  Concreto de vigas y losas (hoja)
│   ├── 3.7  Encofrado de escaleras (hoja)
│   └── 3.8  Concreto de escaleras (hoja)
├── 4.0  Albañilería (capítulo)
│   ├── 4.1  Muros de ladrillo 1er piso (hoja)
│   ├── 4.2  Muros de ladrillo 2do piso (hoja)
│   ├── 4.3  Tarrajeo interior (hoja)
│   └── 4.4  Tarrajeo exterior (hoja)
├── 5.0  Instalaciones (capítulo)
│   ├── 5.1  Instalaciones sanitarias (hoja)
│   ├── 5.2  Instalaciones eléctricas (hoja)
│   └── 5.3  Instalaciones de gas (hoja)
├── 6.0  Acabados (capítulo)
│   ├── 6.1  Pisos cerámicos (hoja)
│   ├── 6.2  Pintura interior (hoja)
│   ├── 6.3  Pintura exterior (hoja)
│   ├── 6.4  Puertas y ventanas (hoja)
│   ├── 6.5  Grifería y sanitarios (hoja)
│   └── 6.6  Cerámica cocinas y baños (hoja)
└── 7.0  Obras Exteriores (capítulo)
    ├── 7.1  Veredas y pavimentos (hoja)
    ├── 7.2  Jardinería (hoja)
    └── 7.3  Tanque elevado y cisterna (hoja)
```

### Reglas de validación

- El campo `id_wbs` debe ser único en toda la base de datos.
- Toda actividad hoja (nivel_wbs = 2) debe tener `presupuesto_total > 0` y `unidad` no vacía.
- La `fecha_inicio` debe ser anterior o igual a `fecha_fin`.
- El campo `padre_id` debe referenciar un `id_wbs` existente en la misma tabla.
- El rango de fechas de un nodo padre debe contener los rangos de todas sus actividades hijas.

---

## 2. BD_PV.csv — Plan de Valor (Planned Value)

### Descripción general

La base de datos **BD_PV** contiene la curva de valor planificado diario para cada actividad hoja del WBS. Este archivo es el corazón del sistema EVM, ya que define la "meta diaria" que el reportador debe cumplir para cada actividad. Cada fila representa el valor planificado de una actividad en un día específico, permitiendo calcular el PV diario (cuánto se debía ejecutar ese día) y el PV acumulado (cuánto se debía haber ejecutado hasta esa fecha).

El PV se calcula con distribución lineal: el presupuesto total de cada actividad se divide equitativamente entre todos los días de su duración (incluyendo fecha_inicio y fecha_fin). Esto genera una meta diaria constante en unidades físicas (metrado) y monetarias.

### Estructura del archivo

| Columna | Tipo de dato | Obligatorio | Descripción |
|---------|-------------|-------------|-------------|
| `id_wbs` | Texto | Sí | Código de la actividad hoja del WBS a la que pertenece este registro. Debe corresponder a un `id_wbs` de nivel 2 existente en BD_EDT. Una misma actividad tendrá múltiples filas, una por cada día de su duración. |
| `fecha` | Fecha (YYYY-MM-DD) | Sí | Fecha específica del día al que aplica este valor planificado. El rango de fechas para cada actividad va desde su `fecha_inicio` hasta su `fecha_fin` (ambas inclusive). Cada fecha aparece una sola vez por actividad. |
| `porcentaje_planificado_diario` | Numérico (4 decimales) | Sí | Porcentaje del trabajo total de la actividad que se planifica ejecutar en este día específico. Se calcula como `100 / duración_en_días`. Por ejemplo, si una actividad dura 12 días, el porcentaje diario será `8.3333%`. La suma de todos los porcentajes diarios de una actividad debe aproximarse a 100%. |
| `metrado_diario_planificado` | Numérico (4 decimales) | Sí | Cantidad física planificada para ejecutar en este día, expresada en la unidad de la actividad (m2, m3, kg, und, etc.). Se calcula como `metrado_total / duración_en_días`. Este es el valor que se muestra como "Meta del Día" en el formulario de EV, indicando al reportador cuánto se debía ejecutar ese día en términos físicos. |
| `metrado_acumulado_planificado` | Numérico (4 decimales) | Sí | Cantidad física acumulada planificada desde el inicio de la actividad hasta esta fecha (inclusive). Se calcula como la suma progresiva de `metrado_diario_planificado`. En el último día de la actividad, este valor debe coincidir con el `metrado_total` de la actividad. Permite conocer la meta acumulada a cualquier fecha de corte. |
| `pv_diario` | Numérico (2 decimales) | Sí | Valor monetario planificado para este día específico, expresado en soles (S/). Se calcula como `presupuesto_total / duración_en_días`. Representa cuánto valor se debía generar en este día según el cronograma. Este valor se usa en el resumen EVM como "PV del Día" para cada actividad seleccionada. |
| `pv_acumulado` | Numérico (2 decimales) | Sí | Valor monetario planificado acumulado desde el inicio de la actividad hasta esta fecha. Se calcula como la suma progresiva de `pv_diario`. En el último día de la actividad, este valor debe ser igual al `presupuesto_total` de la actividad. Se usa para construir la Curva S de PV acumulado del proyecto. |

### Fórmulas de cálculo

```
duración_en_días = fecha_fin - fecha_inicio + 1

porcentaje_planificado_diario = 100 / duración_en_días

metrado_diario_planificado = metrado_total / duración_en_días

metrado_acumulado_planificado = Σ metrado_diario_planificado (desde fecha_inicio hasta fecha actual)

pv_diario = presupuesto_total / duración_en_días

pv_acumulado = Σ pv_diario (desde fecha_inicio hasta fecha actual)
```

### Ejemplo de datos

Para la actividad `1.1` "Trazos y niveles" (presupuesto = S/ 8,500, duración = 12 días):

| id_wbs | fecha | porcentaje_diario | metrado_diario | metrado_acumulado | pv_diario | pv_acumulado |
|--------|-------|-------------------|----------------|-------------------|-----------|--------------|
| 1.1 | 2026-01-05 | 8.3333 | 141.6667 | 141.6667 | 708.33 | 708.33 |
| 1.1 | 2026-01-06 | 8.3333 | 141.6667 | 283.3333 | 708.33 | 1416.67 |
| ... | ... | ... | ... | ... | ... | ... |
| 1.1 | 2026-01-16 | 8.3333 | 141.6667 | 1700.0000 | 708.33 | 8500.00 |

### Reglas de validación

- El campo `id_wbs` debe existir en BD_EDT como actividad hoja (nivel_wbs = 2, presupuesto_total > 0).
- No debe haber filas duplicadas para la misma combinación de `id_wbs` + `fecha`.
- El `pv_acumulado` del último día debe coincidir con el `presupuesto_total` de la actividad.
- El total de registros por actividad debe ser igual a la duración en días de dicha actividad.

---

## 3. BD_RRHH.csv — Recursos Humanos

### Descripción general

La base de datos **BD_RRHH** contiene el catálogo de recursos humanos disponibles para el registro del costo real (AC - Actual Cost) en la sección de "Mano de Obra" del formulario RDO. Cada recurso tiene un precio unitario por hora-hombre (hh) que se utiliza para calcular automáticamente el monto de costo real al registrar las horas trabajadas.

Esta tabla es exclusiva para el tab de "Mano de Obra" en la sección de Recursos Consumidos. Los recursos se organizan por categoría laboral, lo que permite filtrar y agrupar los costos de personal por tipo de trabajador.

### Estructura del archivo

| Columna | Tipo de dato | Obligatorio | Descripción |
|---------|-------------|-------------|-------------|
| `id_recurso` | Texto | Sí | Código identificador único del recurso humano. Usa el formato `RRHH-XXX` donde XXX es un número secuencial de tres dígitos (ej: `RRHH-001`, `RRHH-024`). Este código se usa internamente para relacionar el recurso con su precio unitario al momento de calcular el monto en el formulario. |
| `descripcion` | Texto | Sí | Nombre descriptivo del puesto o rol del trabajador. Debe ser lo suficientemente claro para que el usuario del formulario pueda identificar rápidamente el tipo de personal (ej: "Ingeniero Residente", "Operario de Encofrado", "Peón"). Este texto aparece en el selector desplegable del formulario. |
| `categoria` | Texto | Sí | Categoría laboral a la que pertenece el recurso. Se usa para agrupar y filtrar los recursos en el formulario. Valores permitidos: `ingeniero` (personal profesional), `capataz` (supervisores de campo), `maestro_obra` (maestros de obra especializados), `operario` (trabajadores calificados con especialidad), `oficial` (trabajadores semi-calificados), `peón` (trabajadores no calificados), `supervisor` (personal de supervisión técnica). |
| `precio_unitario` | Numérico (2 decimales) | Sí | Tarifa horaria del recurso expresada en soles por hora-hombre (S/ /hh). Representa el costo que se carga al proyecto por cada hora de trabajo de este tipo de personal. Los valores son realistas para el mercado de construcción peruano en 2026. Ejemplos: Ingeniero Residente = S/ 85.00/hh, Peón = S/ 25.00/hh. |
| `unidad` | Texto | Sí | Unidad de medida del recurso. Para todos los recursos humanos es `hh` (hora-hombre), que representa una hora de trabajo de una persona. En futuras extensiones podría incluir `hd` (hora-día) o `mes` (contrato mensual). |

### Categorías y rangos de precios

| Categoría | Cantidad | Rango de PU (S//hh) | Descripción |
|-----------|----------|---------------------|-------------|
| `ingeniero` | 3 | 65.00 - 85.00 | Personal profesional: residente, supervisión, costos |
| `capataz` | 2 | 52.00 - 55.00 | Supervisores de campo: general, estructuras |
| `maestro_obra` | 2 | 48.00 - 52.00 | Maestros de obra: general, especializado |
| `operario` | 7 | 36.00 - 70.00 | Trabajadores calificados: encofrado, acero, concreto, maquinaria, topografía |
| `oficial` | 6 | 32.00 - 38.00 | Trabajadores semi-calificados: albañilería, pintura, eléctrico, sanitario, electricista, gasfitero |
| `peón` | 2 | 25.00 - 28.00 | Trabajadores no calificados: peón, peón especializado |
| `supervisor` | 2 | 42.00 - 45.00 | Personal de supervisión técnica: seguridad, calidad |

### Fórmula de cálculo en el formulario

```
Monto_Mano_de_Obra = cantidad_horas × precio_unitario
```

Ejemplo: Si se registran 8 horas de Ingeniero Residente: `8 × S/ 85.00 = S/ 680.00`

### Reglas de validación

- El campo `id_recurso` debe ser único.
- El `precio_unitario` debe ser mayor a cero.
- La `categoria` debe ser uno de los valores permitidos.

---

## 4. BD_Almacen.csv — Almacén (Materiales y Equipos)

### Descripción general

La base de datos **BD_Almacen** contiene el catálogo de materiales y equipos disponibles para el registro del costo real (AC - Actual Cost) en las secciones de "Materiales" y "Equipos" del formulario RDO. A diferencia de BD_RRHH que solo maneja mano de obra, esta tabla gestiona los recursos físicos del proyecto, divididos en dos tipos según el campo `tipo`.

Los materiales se usan en el tab de "Materiales" y los equipos en el tab de "Equipos" de la sección de Recursos Consumidos. Cada recurso tiene un precio unitario real que representa el costo de adquisición o alquiler en el mercado peruano para el año 2026.

### Estructura del archivo

| Columna | Tipo de dato | Obligatorio | Descripción |
|---------|-------------|-------------|-------------|
| `id_recurso` | Texto | Sí | Código identificador único del recurso. Usa dos formatos según el tipo: `MAT-XXX` para materiales (ej: `MAT-001`, `MAT-030`) y `EQP-XXX` para equipos (ej: `EQP-001`, `EQP-009`). Este código se usa para filtrar los recursos por tipo y para calcular el monto en el formulario. |
| `descripcion` | Texto | Sí | Nombre descriptivo del material o equipo, incluyendo especificaciones técnicas relevantes. Para materiales, incluye dimensiones o presentaciones (ej: "Cemento Portland (bolsa 42.5kg)", "Ladrillo king kong 18 huecos", "Tubo PVC SAP 4"). Para equipos, indica el tipo de maquinaria (ej: "Excavadora", "Grúa", "Concretera"). Este texto aparece en el selector desplegable del formulario. |
| `tipo` | Texto | Sí | Clasificación del recurso en una de dos categorías: `material` para materiales de construcción consumibles (cemento, acero, ladrillos, tuberías, pintura, etc.) o `equipo` para equipos y maquinaria de construcción (excavadora, grúa, concretera, andamio, etc.). Este campo determina en qué tab del formulario aparece el recurso: los de tipo `material` en el tab "Materiales" y los de tipo `equipo` en el tab "Equipos". |
| `unidad` | Texto | Sí | Unidad de medida del recurso. Varía según el tipo de material o equipo. Para materiales: `bolsa`, `kg`, `millar`, `m3`, `m2`, `ml`, `plancha`, `galón`, `und`. Para equipos: `hr` (hora de operación), `día` (jornada de alquiler). La unidad es crucial porque determina cómo se mide la cantidad consumida en el formulario. |
| `precio_unitario_real` | Numérico (2 decimales) | Sí | Precio unitario real del recurso expresado en soles (S/). Para materiales, es el precio de compra en el mercado. Para equipos, es la tarifa de alquiler por hora o por día. Representa el costo que se carga al proyecto por cada unidad consumida o utilizada. Los valores son realistas para el mercado peruano de construcción en 2026. |

### Distribución por tipo

#### Materiales (tipo = "material") — 30 ítems

| ID | Recurso | Unidad | PU (S/) |
|----|---------|--------|---------|
| MAT-001 | Cemento Portland (bolsa 42.5kg) | bolsa | 22.00 |
| MAT-002 | Acero de refuerzo fy=4200 kg/cm2 | kg | 4.80 |
| MAT-003 | Ladrillo king kong 18 huecos | millar | 850.00 |
| MAT-004 | Ladrillo pandereta | millar | 920.00 |
| MAT-005 | Arena gruesa | m3 | 65.00 |
| MAT-006 | Piedra chancada 1/2" | m3 | 75.00 |
| MAT-007 | Agua | m3 | 3.50 |
| MAT-008 | Madera tornillo | pie2 | 12.00 |
| MAT-009 | Contrachapado 4x8 1/2" | plancha | 85.00 |
| MAT-010 | Clavos 3" | kg | 6.50 |
| MAT-011 | Alambre negro #16 | kg | 5.80 |
| MAT-012 | Alambre recocido | kg | 5.20 |
| MAT-013 | Tubo PVC SAP 4" | ml | 18.00 |
| MAT-014 | Tubo PVC SAP 2" | ml | 9.50 |
| MAT-015 | Cable THW 2.5mm2 | ml | 4.20 |
| MAT-016 | Cable THW 4mm2 | ml | 6.80 |
| MAT-017 | Interruptor simple | und | 12.00 |
| MAT-018 | Tomacorriente bipolar | und | 15.00 |
| MAT-019 | Cerámico pisos 30x30 | m2 | 35.00 |
| MAT-020 | Cerámico pared 20x30 | m2 | 28.00 |
| MAT-021 | Pintura látex | galón | 65.00 |
| MAT-022 | Pintura esmalte | galón | 78.00 |
| MAT-023 | Puerta cedro 0.80x2.10 | und | 450.00 |
| MAT-024 | Ventana aluminio 1.00x1.20 | und | 380.00 |
| MAT-025 | Grifería lavadero | und | 120.00 |
| MAT-026 | Inodoro completo | und | 280.00 |
| MAT-027 | Lavadero acero inoxidable | und | 180.00 |
| MAT-028 | Tubo de gas 1/2" | ml | 15.00 |
| MAT-029 | Yeso | bolsa | 18.00 |
| MAT-030 | Impermeabilizante | galón | 55.00 |

#### Equipos (tipo = "equipo") — 9 ítems

| ID | Recurso | Unidad | PU (S/) |
|----|---------|--------|---------|
| EQP-001 | Excavadora | hr | 280.00 |
| EQP-002 | Grúa | hr | 350.00 |
| EQP-003 | Concretera | hr | 45.00 |
| EQP-004 | Vibrador de concreto | hr | 35.00 |
| EQP-005 | Compactora | hr | 55.00 |
| EQP-006 | Andamio | día | 25.00 |
| EQP-007 | Winche | hr | 85.00 |
| EQP-008 | Mezcladora 1saco | hr | 40.00 |
| EQP-009 | Grupo electrógeno | hr | 65.00 |

### Fórmulas de cálculo en el formulario

```
Monto_Material = cantidad × precio_unitario_real
Monto_Equipo = cantidad × precio_unitario_real
Subtotal_Materiales = Σ Monto_Material (por todas las filas de materiales)
Subtotal_Equipos = Σ Monto_Equipo (por todas las filas de equipos)
AC_Total = Subtotal_Mano_de_Obra + Subtotal_Materiales + Subtotal_Equipos
```

Ejemplo: Si se registran 50 bolsas de cemento: `50 × S/ 22.00 = S/ 1,100.00`

### Reglas de validación

- El campo `id_recurso` debe ser único en toda la tabla.
- El campo `tipo` solo acepta los valores `material` o `equipo`.
- El `precio_unitario_real` debe ser mayor a cero.
- La `unidad` debe ser consistente con el tipo de recurso.

---

## Relaciones entre bases de datos

Las cuatro bases de datos se relacionan de la siguiente manera dentro del sistema RDO-EVM:

```
BD_EDT (WBS)
  ├── id_wbs ──────────► BD_PV.id_wbs (1 a N: cada actividad tiene múltiples días)
  ├── padre_id ─────────► BD_EDT.id_wbs (autoreferencia para jerarquía)
  └── actividades hoja ──► Seleccionables en formulario EV

BD_RRHH (Mano de Obra)
  └── id_recurso ───────► Seleccionable en tab "Mano de Obra" del formulario AC

BD_Almacen (Materiales y Equipos)
  ├── tipo = "material" ─► Seleccionable en tab "Materiales" del formulario AC
  └── tipo = "equipo" ───► Seleccionable en tab "Equipos" del formulario AC
```

### Flujo de cálculo EVM

1. **PV del día**: Se consulta BD_PV filtrando por las actividades seleccionadas y la fecha del reporte, sumando los valores de `pv_diario`.
2. **EV del día**: Se calcula a partir de la cantidad ejecutada real ingresada por el usuario, usando la fórmula `EV = (cantidad_real / metrado_total) × presupuesto_total`. El metrado_total se obtiene del valor máximo de `metrado_acumulado_planificado` en BD_PV para esa actividad.
3. **AC del día**: Se calcula sumando todos los recursos consumidos: Mano de Obra (de BD_RRHH), Materiales y Equipos (de BD_Almacen), cada uno como `cantidad × precio_unitario`.
4. **SPI = EV acumulado / PV acumulado**: Usa datos históricos almacenados en localStorage más el reporte actual.
5. **CPI = EV acumulado / AC acumulado**: Usa datos históricos almacenados en localStorage más el reporte actual.

---

## Convenciones de nomenclatura de archivos

El sistema detecta automáticamente el tipo de base de datos según el nombre del archivo cargado:

| Patrón en el nombre del archivo | Base de datos asignada |
|-------------------------------|----------------------|
| Contiene `edt` o `wbs` | BD_EDT (Estructura de Desglose del Trabajo) |
| Contiene `pv` o `planificado` | BD_PV (Plan de Valor) |
| Contiene `rrhh` o `recurso` | BD_RRHH (Recursos Humanos) |
| Contiene `almacen`, `material` o `equipo` | BD_Almacen (Almacén) |

Ejemplos de nombres válidos:
- `BD_EDT.csv` → EDT/WBS
- `BD_PV.csv` → Plan de Valor
- `BD_RRHH.csv` → Recursos Humanos
- `BD_Almacen.csv` → Almacén
- `datos_wbs.json` → EDT/WBS
- `planificado.csv` → Plan de Valor

---

## Almacenamiento local (localStorage)

Una vez cargadas, las bases de datos se almacenan en caché en el navegador del usuario usando localStorage con las siguientes claves:

| Clave de localStorage | Contenido | Fuente |
|----------------------|-----------|--------|
| `rdo_edt` | Array JSON con los datos de BD_EDT | BD_EDT.csv |
| `rdo_pv` | Array JSON con los datos de BD_PV | BD_PV.csv |
| `rdo_rrhh` | Array JSON con los datos de BD_RRHH | BD_RRHH.csv |
| `rdo_almacen` | Array JSON con los datos de BD_Almacen | BD_Almacen.csv |
| `rdo_historial` | Array JSON con reportes históricos enviados | Generado por la app |

Esto permite que el usuario no necesite cargar los archivos en cada sesión; el sistema los recupera automáticamente del caché local al abrir la aplicación.
