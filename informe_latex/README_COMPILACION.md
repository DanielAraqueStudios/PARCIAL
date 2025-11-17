# Compilación del Informe IEEE

## Archivos del Proyecto

```
informe_latex/
├── informe_ieee.tex         # Archivo principal (usar este)
├── sprint2_implementacion.tex
├── sprint3_resultados.tex
└── README_COMPILACION.md     # Este archivo
```

## Requisitos

### Distribución LaTeX
- **Windows**: MiKTeX o TeX Live
- **Linux**: TeX Live
- **macOS**: MacTeX

### Paquetes LaTeX Necesarios
El archivo usa la clase `IEEEtran` y los siguientes paquetes:
- `IEEEtran` (clase de documento IEEE)
- `cite`, `amsmath`, `amssymb`, `amsfonts`
- `graphicx`, `xcolor`, `textcomp`
- `listings` (para código)
- `tikz` (para diagramas)
- `hyperref` (para enlaces)
- `babel` con opción `spanish`
- `inputenc` con opción `utf8`
- `float`

## Compilación

### Opción 1: Usando pdflatex (Recomendado)

```powershell
# Navegar al directorio
cd "C:\Users\danie\OneDrive - unimilitar.edu.co\Documentos\UNIVERSIDADDDDDDDDDDDDDDDDDDDDDDDDDD\MECATRÓNICA\SEXTO SEMESTRE\COMUNICACIONES\PARCIAL\informe_latex"

# Compilar (se necesitan 2 pasadas para referencias cruzadas)
pdflatex informe_ieee.tex
pdflatex informe_ieee.tex

# Si hay bibliografía BibTeX (opcional)
bibtex informe_ieee
pdflatex informe_ieee.tex
pdflatex informe_ieee.tex
```

### Opción 2: Usando latexmk (Automático)

```powershell
# Compilación automática con todas las pasadas necesarias
latexmk -pdf informe_ieee.tex

# Limpiar archivos auxiliares después
latexmk -c
```

### Opción 3: Overleaf (Online)

1. Crear nuevo proyecto en [Overleaf](https://www.overleaf.com)
2. Subir los 3 archivos `.tex`
3. Configurar compilador: **pdfLaTeX**
4. Compilar automáticamente

## Estructura del Documento

El documento IEEE generado tendrá:

1. **Página 1-2**: 
   - Título, autores, abstract en inglés
   - Keywords
   - Sección I: Introducción
   - Sección II: Marco Teórico (MQTT, TLS, X.509, AWS services)

2. **Páginas 3-5**:
   - Sección III: Arquitectura del Sistema (sprint2)
   - Diagramas TikZ de arquitectura
   - Descripción de componentes

3. **Páginas 6-8**:
   - Sección IV: Implementación (sprint2)
   - Código fuente Python
   - Configuraciones JSON/YAML

4. **Páginas 9-11**:
   - Sección V: Pruebas y Validación (sprint3)
   - Casos de prueba
   - Procedimientos de testing

5. **Páginas 12-14**:
   - Sección VI: Resultados y Evidencias (sprint3)
   - Métricas, gráficas
   - Screenshots y logs

6. **Páginas 15-16**:
   - Sección VII: Conclusiones (sprint3)
   - Referencias bibliográficas
   - Anexos

## Formato IEEE

El documento usa la clase `IEEEtran` con formato `conference`:
- **Columnas**: 2 columnas por página
- **Tamaño de papel**: Letter (8.5" x 11")
- **Márgenes**: Estándar IEEE
- **Fuente**: Times Roman, 10pt para texto principal
- **Encabezados de sección**: Numeración romana (I, II, III, IV...)
- **Subsecciones**: Letras mayúsculas (A, B, C...)

## Problemas Comunes

### Error: "File IEEEtran.cls not found"
**Solución**: Instalar paquete IEEEtran:
```powershell
# MiKTeX
mpm --install=ieeetran

# TeX Live
tlmgr install ieeetran
```

### Error: "Package tikz not found"
**Solución**: Instalar paquete pgf:
```powershell
# MiKTeX
mpm --install=pgf

# TeX Live
tlmgr install pgf
```

### Error: "Undefined control sequence \rowcolor"
**Solución**: El paquete `colortbl` no está incluido. Agregar al preámbulo:
```latex
\usepackage{colortbl}
```

### Warnings sobre "Overfull \hbox"
**Información**: Normales en formato de 2 columnas IEEE. LaTeX está advirtiendo que algunas líneas de código son demasiado anchas. Usar `breaklines=true` en lstlistings (ya incluido).

### Imágenes/Figuras no aparecen
**Causa**: Placeholders para screenshots sin archivo real.
**Solución**: Las figuras marcadas como "placeholder" tienen solo texto explicativo. Para agregar imágenes reales:
```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.48\textwidth]{ruta/a/imagen.png}
\caption{Descripción de la imagen}
\label{fig:mi-figura}
\end{figure}
```

## Personalización

### Cambiar Autor
Editar en `informe_ieee.tex` líneas 117-125:
```latex
\author{
\IEEEauthorblockN{Tu Nombre}
\IEEEauthorblockA{\textit{Tu Programa} \\
\textit{Tu Universidad}\\
Ciudad, País \\
tu.email@universidad.edu}
}
```

### Agregar Coautores
```latex
\author{
\IEEEauthorblockN{Autor 1}
\IEEEauthorblockA{...}
\and
\IEEEauthorblockN{Autor 2}
\IEEEauthorblockA{...}
}
```

### Cambiar Colores
Los colores corporativos están definidos en líneas 25-29:
```latex
\definecolor{azulumng}{RGB}{0,51,102}
\definecolor{azulclaro}{RGB}{41,128,185}
% etc.
```

### Modificar Estilo de Código
Los estilos de listings están en líneas 34-93. Personalizar:
```latex
\lstdefinestyle{python}{
    basicstyle=\ttfamily\footnotesize,  % Cambiar tamaño
    keywordstyle=\color{purple},        % Cambiar color de keywords
    % ...
}
```

## Exportar a Word (si es necesario)

```powershell
# Convertir PDF a DOCX usando pandoc
pandoc informe_ieee.pdf -o informe_ieee.docx
```

**Nota**: La conversión PDF→Word pierde formato. Si se requiere Word desde el inicio, considerar usar plantilla IEEE para Word en lugar de LaTeX.

## Archivos Generados

Después de compilar exitosamente:
- `informe_ieee.pdf` ← **Archivo final para entregar**
- `informe_ieee.aux` (auxiliar)
- `informe_ieee.log` (registro de compilación)
- `informe_ieee.out` (hyperref)
- `informe_ieee.bbl` (bibliografía, si se usa bibtex)
- `informe_ieee.blg` (log de bibtex)

Puedes eliminar archivos auxiliares manteniendo solo el PDF:
```powershell
latexmk -c  # Elimina temporales
```

## Verificación de Formato IEEE

Lista de verificación IEEE:
- ✅ Dos columnas
- ✅ Abstract en inglés (max 150-200 palabras)
- ✅ Keywords (5-10 términos)
- ✅ Secciones numeradas con romanos (I, II, III...)
- ✅ Referencias en formato IEEE (numeradas [1], [2], [3]...)
- ✅ Ecuaciones numeradas
- ✅ Figuras y tablas referenciadas en texto
- ✅ Captions bajo figuras, sobre tablas
- ✅ Fuente Times Roman 10pt

## Tamaño Esperado

- **Páginas**: 12-16 páginas (típico para conference IEEE)
- **Tamaño PDF**: ~500 KB sin imágenes, ~2-5 MB con screenshots
- **Tiempo de compilación**: 10-30 segundos por pasada

## Soporte

Para problemas con LaTeX:
- [TeX StackExchange](https://tex.stackexchange.com/)
- [Overleaf Documentation](https://www.overleaf.com/learn)
- [CTAN IEEEtran](https://ctan.org/pkg/ieeetran)

Para problemas con el contenido técnico:
- Ver repositorio: https://github.com/DanielAraqueStudios/COMUNICACIONES-IOT-AWS

---

**Última actualización**: Noviembre 16, 2025  
**Autor**: Daniel Araque  
**Universidad**: Universidad Militar Nueva Granada
