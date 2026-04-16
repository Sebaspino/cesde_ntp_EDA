
        # Reporte de Análisis Exploratorio de Datos
        
        ## 1. Identificación y Contexto
        Es un registro de análisis de laboratorio de suelos agrícolas colombianos, generado muy probablemente por una entidad estatal o un laboratorio de servicios agropecuarios (el perfil encaja con instituciones como el ICA o Corpoica/Agrosavia). Cada fila representa una muestra de suelo tomada en un predio, con su contexto agronómico (departamento, municipio, cultivo, topografía, drenaje) y sus resultados químicos (pH, nutrientes, metales disponibles). El propósito es orientar decisiones de fertilización y manejo de suelos para productores agrícolas de todo el país. Cubre desde enero de 2014 hasta septiembre de 2025, con 92,738 muestras de los 32 departamentos.
        
        ## 2. Calidad de los Datos
        Hay dos capas de "vacío" mezcladas, lo cual es el principal problema de calidad:
Los nulos reales (NaN de pandas) son casi inexistentes, solo 3 celdas en todo el dataset. Eso suena bien, pero es engañoso, porque el verdadero "dato faltante" está codificado como texto.
Los "ND" (No Determinado) son la forma real de ausencia. Las columnas más afectadas son críticas: acidez intercambiable y aluminio intercambiable tienen 45,130 NDs cada una (49% del total), y las cuatro columnas de "doble ácido" tienen más de 87,000 NDs, es decir, son prácticamente inutilizables para análisis masivos.
Los "No indica" afectan a las variables contextuales: el 54% de registros no reporta si usa riego, el 44% no informa qué fertilizantes aplica, el 33% no indica el tiempo de establecimiento del cultivo. Esto limita mucho cualquier análisis cruzado entre prácticas agrícolas y resultados del suelo.
Adicionalmente, algunas columnas tienen valores del tipo <0.09, lo que indica que el valor estaba por debajo del límite de detección del laboratorio, y fueron leídas como texto en vez de número, lo que requiere limpieza antes de cualquier análisis estadístico serio.
        
        ## 3. Hallazgos Estadísticos Clave
        El hallazgo más contundente es el pH: la media es 5.71 y la mediana 5.47, lo que ubica al suelo colombiano típico en rango ácido. Más del 52% de las muestras cae entre 4.5 y 5.5, y solo un 12% alcanza rango neutro o alcalino. Esto es consistente con los suelos tropicales de la región andina.
La materia orgánica tiene una media de 4.41% pero una mediana de 2.75%, señal de que hay muchos suelos pobres con algunos valores muy altos jalando la media hacia arriba. Un suelo con menos de 3% de MO se considera bajo en Colombia.
El fósforo es el nutriente con mayor dispersión: media de 28.96 mg/kg pero mediana de solo 8.40 mg/kg. Hay predios con niveles muy altos (posiblemente por sobreabonado con fosfatos) que distorsionan el promedio. La mayoría de los suelos tiene niveles bajos a moderados.
El hierro disponible (Olsen) con media de 240 mg/kg es llamativamente alto, consistente con suelos ácidos donde el hierro se solubiliza y puede volverse tóxico para algunos cultivos.
En cuanto a cultivos, cacao es el más muestreado (11,104 registros), seguido por pastos, aguacate y café, lo que refleja los rubros de mayor expansión agrícola en el país en la última década.
Geográficamente, Cundinamarca concentra el 15% de todas las muestras, seguido por Valle del Cauca, Meta y Antioquia.
        
        ## 4. Conclusión Final
        El mensaje central es que la gran mayoría del suelo agrícola colombiano es ácido y requiere intervención correctiva (principalmente encalamiento) antes de poder optimizar la fertilización. Un pH entre 4.5 y 5.5 no solo es desfavorable para la mayoría de cultivos, sino que en ese rango el aluminio y el manganeso se vuelven solubles y tóxicos, y los nutrientes como el fósforo, calcio y magnesio quedan bloqueados químicamente aunque estén presentes en el suelo.
El dataset también revela una brecha de información agronómica importante: más de la mitad de los productores no reporta qué fertilizantes usa ni si tiene riego, lo que dificulta correlacionar las condiciones del suelo con las prácticas de manejo. Es un dataset robusto en química pero pobre en contexto, lo que limita su uso para recomendaciones personalizadas más allá del diagnóstico puntual.
        
        ---
        *Generado por el módulo de Reportes - Proyecto Integrador*
        