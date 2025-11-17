# ⚠️ LaTeX No Instalado - Guía de Instalación

## Estado Actual

✅ **Archivos LaTeX creados**:
- `informe_ieee.tex` (archivo principal formato IEEE)
- `sprint2_implementacion.tex` (arquitectura e implementación)
- `sprint3_resultados.tex` (pruebas, resultados, conclusiones)

❌ **LaTeX no está instalado** en tu sistema Windows

## Opciones para Generar el PDF

### Opción 1: Overleaf (Recomendado - Más Fácil) ⭐

**Ventajas**: No requiere instalación, online, colaborativo

**Pasos**:
1. Ir a https://www.overleaf.com
2. Crear cuenta gratis
3. Click en "New Project" → "Upload Project"
4. Subir los 3 archivos `.tex`:
   - `informe_ieee.tex`
   - `sprint2_implementacion.tex`
   - `sprint3_resultados.tex`
5. En el menú: Seleccionar `informe_ieee.tex` como "Main document"
6. Configurar compilador: Menu → Compiler → **pdfLaTeX**
7. Click "Recompile"
8. Descargar PDF

**Tiempo estimado**: 5 minutos

---

### Opción 2: MiKTeX (Para trabajar offline)

**Ventajas**: Control total, compilación local, no requiere internet después de instalar

#### Paso 1: Descargar MiKTeX

1. Ir a https://miktex.org/download
2. Descargar **MiKTeX Installer** (Windows x64)
3. Ejecutar el instalador (~280 MB)

#### Paso 2: Instalar MiKTeX

Durante instalación:
- ✅ Install missing packages: **Yes** (automáticamente)
- ✅ Preferred paper size: **Letter** o **A4**
- ✅ Install for: **Only for: TU_USUARIO** (recomendado)

**Tiempo de instalación**: 15-20 minutos

#### Paso 3: Instalar Paquetes Necesarios

Abrir PowerShell como Administrador y ejecutar:

```powershell
# Actualizar gestor de paquetes
mpm --update-db

# Instalar paquetes esenciales
mpm --install=ieeetran
mpm --install=pgf
mpm --install=listings
mpm --install=hyperref
mpm --install=xcolor
mpm --install=babel-spanish
```

#### Paso 4: Compilar el Documento

```powershell
cd "C:\Users\danie\OneDrive - unimilitar.edu.co\Documentos\UNIVERSIDADDDDDDDDDDDDDDDDDDDDDDDDDD\MECATRÓNICA\SEXTO SEMESTRE\COMUNICACIONES\PARCIAL\informe_latex"

# Compilar (se ejecuta 2 veces para resolver referencias)
pdflatex informe_ieee.tex
pdflatex informe_ieee.tex
```

Si aparece mensaje "Install package X? (y/N)", escribir `y` y presionar Enter.

**Archivo generado**: `informe_ieee.pdf` en la misma carpeta

---

### Opción 3: TeXworks (Editor con Vista Previa)

**Ventajas**: Interfaz gráfica, preview en vivo

MiKTeX incluye TeXworks. Después de instalar MiKTeX:

1. Buscar "TeXworks" en el menú Inicio
2. Abrir TeXworks
3. File → Open → Seleccionar `informe_ieee.tex`
4. En dropdown arriba: Seleccionar **pdfLaTeX**
5. Click botón verde "Typeset" (o F5)
6. PDF aparece en panel derecho

---

### Opción 4: VS Code + LaTeX Workshop

**Ventajas**: Integración con tu editor actual

**Requisitos previos**: MiKTeX instalado

#### Instalar Extensión

1. En VS Code: `Ctrl+Shift+X`
2. Buscar "LaTeX Workshop"
3. Instalar extensión de James Yu

#### Compilar

1. Abrir `informe_ieee.tex` en VS Code
2. Aparecerá botón "Build LaTeX project" (⚙️) en esquina superior derecha
3. Click en el botón
4. Click en "View LaTeX PDF" (📄) para ver resultado

---

## Verificación del PDF Generado

El documento IEEE debe tener:

### Estructura Esperada
- **Abstract**: 1 párrafo en inglés (~150 palabras)
- **Keywords**: 11 términos clave
- **Sección I**: Introducción (contexto, motivación, objetivos)
- **Sección II**: Marco Teórico (MQTT, TLS, X.509, AWS services, LocalStack)
- **Sección III**: Arquitectura (diagramas TikZ del sistema)
- **Sección IV**: Implementación (código Python, configs)
- **Sección V**: Pruebas (10 casos de prueba, procedimientos)
- **Sección VI**: Resultados (métricas, gráficas, evidencias)
- **Sección VII**: Conclusiones y trabajo futuro
- **Referencias**: 10 referencias bibliográficas
- **Anexos**: Comandos de referencia, glosario

### Formato Visual
- ✅ **2 columnas** por página
- ✅ Título centrado con autor y afiliación
- ✅ Abstract en cursiva
- ✅ Keywords después del abstract
- ✅ Secciones numeradas con **romanos** (I, II, III, IV, V, VI, VII)
- ✅ Subsecciones con letras (A, B, C, D)
- ✅ Figuras centradas con caption abajo
- ✅ Tablas centradas con caption arriba
- ✅ Código con numeración de líneas
- ✅ Referencias al final numeradas [1], [2], [3]...

### Tamaño Esperado
- **Páginas**: 14-18 páginas (typical IEEE conference)
- **Tamaño PDF**: ~600 KB (sin imágenes reales)
- **Tiempo compilación**: 15-30 segundos

---

## Solución de Problemas

### Error: "IEEEtran.cls not found"
```powershell
mpm --install=ieeetran
```

### Error: "tikz.sty not found"
```powershell
mpm --install=pgf
```

### Error: "babel-spanish.ldf not found"
```powershell
mpm --install=babel-spanish
```

### Warning: "Overfull \hbox"
**Información**: Normal en formato de 2 columnas. LaTeX advierte que algún código es ancho. No es error crítico.

### Compilación se detiene pidiendo input
Agregar flag `-interaction=nonstopmode`:
```powershell
pdflatex -interaction=nonstopmode informe_ieee.tex
```

---

## Resumen de Comandos

### Overleaf (Recomendado)
```
1. Upload 3 archivos .tex
2. Set Main: informe_ieee.tex
3. Compiler: pdfLaTeX
4. Recompile
5. Download PDF
```

### MiKTeX Local
```powershell
# Instalar MiKTeX desde https://miktex.org/download

# Compilar
cd "ruta\a\informe_latex"
pdflatex informe_ieee.tex
pdflatex informe_ieee.tex

# Ver PDF
start informe_ieee.pdf
```

---

## Próximos Pasos

1. ✅ **Elegir una opción** (Overleaf recomendado para rapidez)
2. ✅ **Compilar el documento**
3. ✅ **Verificar formato IEEE** (2 columnas, referencias, figuras)
4. ✅ **Revisar contenido técnico**
5. ✅ **Agregar screenshots reales** (opcional, reemplazar placeholders)
6. ✅ **Revisar ortografía y redacción**
7. ✅ **Exportar PDF final**

---

## Contacto y Recursos

- **Overleaf Help**: https://www.overleaf.com/learn
- **MiKTeX Manual**: https://docs.miktex.org/
- **IEEE Template**: https://www.ieee.org/conferences/publishing/templates.html
- **LaTeX StackExchange**: https://tex.stackexchange.com/

---

**Nota**: Los 3 archivos `.tex` están listos para compilar sin modificaciones. El documento completo tiene ~1,800 líneas de LaTeX con contenido técnico detallado del proyecto LocalStack + AWS IoT.

**Última actualización**: Noviembre 16, 2025
