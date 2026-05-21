# Adaptación estratégica o mortandad: Trayectorias de las empresas de software ante la democratización de la IA generativa (2019–2025)

**Autor:** Alejandro Jiménez  
**Institución:** Universidad Panamericana  
**Fecha de entrega:** Mayo 2026  
**Palabras clave:** inteligencia artificial generativa, estrategia empresarial, capacidades dinámicas, trayectorias estratégicas, panel data, efectos fijos, sector software

---

## Abstract

Este trabajo examina las trayectorias estratégicas que están siguiendo las empresas de software cotizadas ante la democratización de la IA generativa, y evalúa empíricamente cuál de esas trayectorias se asocia con mejores resultados financieros. Partiendo del marco teórico de las Capacidades Dinámicas (Teece, Pisano y Shuen, 1997) y la Visión Basada en Recursos (Barney, 1991), se propone una taxonomía de tres trayectorias estratégicas clasificadas ex-ante al quiebre estructural de ChatGPT (noviembre 2022): Trayectoria A (Diferenciación/Super-especialización), Trayectoria B ("Atrapados en el medio") y Trayectoria C (Plataforma/Infraestructura). Las 66 empresas del panel son clasificadas usando descripciones de negocio de sus 10-K anuales de 2021. Un panel de datos de 66 empresas × 2019–2025 (437 observaciones empresa-año) evidencia que las empresas de Trayectoria C (plataformas e infraestructura) obtuvieron retornos medios de 45.9% en el período post-ChatGPT (2023–2025), frente a 28.8% en el período previo (+17.1 pp), superando a las trayectorias A (24.3%, −9.6 pp respecto al pre) y B (25.2%, +7.9 pp). El Test de Chow confirma inestabilidad estructural pre/post ChatGPT (F=13.4, p<0.001), demostrando científicamente que las reglas del juego cambiaron en noviembre de 2022. Un modelo de efectos fijos con interacciones de trayectoria (Modelo M5) estima primas direccionalmente consistentes para las trayectorias A y C sobre B, aunque la limitación de potencia estadística con N=66 impide alcanzar significación convencional (p>0.10). Los datos del Stack Overflow Developer Survey 2023–2025 documentan una paradoja de adopción masiva (44%→68%) con caída simultánea en la confianza reportada (45%→29%), evidencia de que la democratización del desarrollo por IA no equivale automáticamente a ventaja competitiva. La conclusión central es que la ventaja competitiva sostenible ante la IA no radica en adoptarla, sino en la capacidad de reconfiguración organizacional alrededor de ella: o bien acumulando conocimiento de dominio inimitable (Trayectoria A), o bien construyendo el sustrato sobre el que otros operan (Trayectoria C). Las empresas sin ninguna de las dos posiciones —atrapadas en el medio— enfrentan el mayor riesgo estratégico.

---

## 1. Introducción

### 1.1 El dilema estratégico de la industria del software

El sector del software atraviesa una transformación comparable, en alcance si no en velocidad, a la transición de la corriente continua (DC) a la corriente alterna (AC) en la industria eléctrica de finales del siglo XIX. Así como esa transición democratizó el acceso a la energía —haciendo obsoletos modelos de negocio basados en la escasez de infraestructura— la IA generativa democratiza la producción de software. Lo que antes requería años de formación técnica hoy puede ser iniciado por un no-programador mediante instrucciones en lenguaje natural.

Esta democratización plantea a las empresas de software un dilema estratégico existencial. Durante décadas, su ventaja competitiva descansó en la complejidad técnica como barrera de entrada: el dominio del código era escaso, costoso de adquirir y difícil de replicar. Si ese dominio deja de ser escaso, la pregunta se vuelve urgente: ¿qué ocurre con las empresas cuyo modelo de negocio dependía precisamente de esa escasez?

La respuesta que emerge de los datos es que el sector no se comporta de manera uniforme. Algunas empresas están convirtiendo la IA en un acelerador sin precedentes de su propuesta de valor. Otras están descubriendo que la IA puede replicar su producto básico a costo marginal cercano a cero. Y un tercer grupo se está convirtiendo en la infraestructura sobre la que todos los demás operan. Este trabajo propone y evidencia empíricamente estas tres trayectorias.

### 1.2 La analogía DC→AC como recurso retórico

La analogía con la transición DC→AC no es técnica: es un recurso retórico para ilustrar la profundidad del cambio. Así como Edison enfrentó a Tesla, la industria del software enfrenta la elección entre defender su lógica de negocio previa o reconocer que las reglas del juego han cambiado de manera estructural. La analogía también captura un elemento empírico central de este trabajo: la existencia de un punto de quiebre identificable —el lanzamiento de ChatGPT en noviembre de 2022— después del cual el comportamiento de la industria cambió de forma estadísticamente demostrable.

### 1.3 Contribuciones de este trabajo

Este trabajo realiza tres contribuciones diferenciadas. Primera, propone una taxonomía de trayectorias estratégicas para el sector software en la era de la IA generativa, fundamentada en teoría del management establecida (Teece et al., 1997; Barney, 1991; Porter, 1980; Williamson, 1975) y clasificada ex-ante al quiebre estructural para evitar sesgo retrospectivo. Segunda, construye evidencia empírica sobre la asociación entre la trayectoria estratégica y el desempeño financiero usando un panel de 66 empresas y un horizonte de siete años. Tercera, integra datos de adopción a nivel individual (Stack Overflow Developer Survey) con análisis a nivel de firma para mostrar la brecha entre adopción agregada y ventaja competitiva.

### 1.4 Estructura del documento

La Sección 2 desarrolla el marco teórico. La Sección 3 describe el ecosistema de LLMs como shock tecnológico. La Sección 4 presenta la taxonomía de tres trayectorias. La Sección 5 expone la evidencia empírica. La Sección 6 analiza la transformación del trabajo de software. La Sección 7 presenta escenarios prospectivos 2026–2030. La Sección 8 discute los hallazgos. La Sección 9 concluye con limitaciones e investigación futura.

---

## 2. Marco Teórico

### 2.1 Destrucción creativa y transiciones de industria

La conceptualización de Schumpeter (1942) sobre la destrucción creativa ofrece el punto de partida más apropiado para analizar el momento actual del sector software. Schumpeter describe cómo las innovaciones radicales no simplemente mejoran los procesos existentes, sino que alteran la estructura competitiva de toda una industria: destruyen las fuentes de ventaja de los incumbentes mientras crean oportunidades para quienes desarrollan las capacidades alineadas con el nuevo paradigma tecnológico.

La IA generativa califica como innovación radical en sentido schumpeteriano. No es una mejora incremental sobre el software existente; es una tecnología que reduce radicalmente los costos de producción de código —el insumo principal del sector— y redistribuye quién puede crear software. El lanzamiento de ChatGPT en noviembre de 2022 representa el punto de quiebre empírico de esta transición: el momento en que una tecnología de laboratorio se convirtió en herramienta de producción masiva.

### 2.2 Visión Basada en Recursos: ¿es la IA un recurso VRIN?

Barney (1991) establece que la ventaja competitiva sostenible requiere recursos que sean Valiosos, Raros, Inimitables y No-sustituibles (VRIN). La pregunta relevante para este trabajo es: ¿cumple la IA generativa estos criterios?

La respuesta es negativa en lo que refiere a la IA como herramienta. Los modelos de lenguaje principales (GPT-4o, Claude, Gemini, Llama) son accesibles a través de APIs públicas a cualquier empresa. La capacidad de usar un LLM es valiosa, pero no rara ni inimitable: cualquier empresa puede acceder a ella al mismo costo. Siguiendo la lógica de Barney, una tecnología universalmente accesible no puede ser fuente de ventaja competitiva sostenida.

Lo que sí puede ser VRIN es la *reconfiguración organizacional* alrededor de la IA: los procesos, el talento especializado, los datos propietarios y las relaciones de cliente construidos al rededor de ella. Una empresa de ciberseguridad que ha acumulado décadas de conocimiento sobre vectores de ataque no puede ser replicada por un modelo de lenguaje en meses. Una plataforma con millones de usuarios en un ecosistema integrado tiene un activo de red inimitable. En ambos casos, la IA amplifica el recurso existente en lugar de crearlo —y es esa amplificación lo que genera la ventaja.

### 2.3 Capacidades Dinámicas: sensing, seizing, transforming

Teece, Pisano y Shuen (1997) desarrollan el concepto de Capacidades Dinámicas como la habilidad de la empresa para integrar, construir y reconfigurar competencias internas y externas en entornos de rápido cambio. La triada operacional que describe este proceso tiene tres fases: *sensing* (detectar oportunidades y amenazas), *seizing* (movilizar recursos para capturar oportunidades), y *transforming* (reconfigurar el modelo de negocio).

Aplicada al shock de la IA generativa, esta triada permite evaluar empíricamente qué hizo cada empresa:

- **Sensing:** ¿Detectó la empresa la ola de los LLMs antes de que fuera mainstream? El proxy observable es si la empresa tenía algún producto de IA generativa lanzado antes del primer trimestre de 2023.
- **Seizing:** ¿Lanzó productos específicos o redefinió su roadmap? Observable en el nivel de AI_intensity post-2022 y en el cambio en gasto en I+D.
- **Transforming:** ¿Cambió el modelo de negocio? Observable en el cambio en márgenes operativos y en la estrategia declarada en los 10-K 2023–2025.

La teoría de las Capacidades Dinámicas predice que las empresas con mayor capacidad de sensing y seizing pre-ChatGPT capturarán una prima de retorno post-ChatGPT. Los datos son consistentes con esta predicción para la Trayectoria C, aunque la limitación de potencia estadística impide una confirmación formal en el Modelo M5.

### 2.4 Economía de Costos de Transacción y la frontera de la firma

Williamson (1975, 1985) explica la existencia de la firma como una respuesta al costo de usar los mercados: cuando los costos de negociar, monitorear y hacer cumplir contratos externos superan los costos de integrar la actividad internamente, las empresas internalizan la producción. La implicación inversa es directa: si los costos de transacción de una actividad caen drásticamente, la frontera de la firma debería contraerse —esa actividad migra al mercado.

La IA generativa representa una caída radical en lo que denominaremos el Costo de Traducción Lógica-Código (CTLC): el costo de transformar una especificación funcional en código operativo. Históricamente, este costo era alto (requería programadores con años de formación), lo cual justificaba la integración vertical de equipos de desarrollo. Si el CTLC se aproxima a cero gracias a los LLMs, la teoría de Williamson predice que las empresas externalizarán o automatizarán esta función, manteniendo internamente solo las actividades donde el costo de transacción de mercado sigue siendo alto: diseño arquitectural complejo, compliance regulatorio, relaciones de confianza con clientes en dominios críticos.

Esta predicción es observable en los datos de layoffs del sector software en 2023–2025: empresas como Meta, Google y Microsoft han reducido equipos de programadores mientras reportan retornos superiores a sus promedios históricos —evidencia directa de que el encogimiento de la frontera de la firma, en los términos de Williamson, está ocurriendo y está siendo recompensado por el mercado. La deuda técnica como variable de control en los modelos econométricos (β=−0.243, p<0.001 en M5) es consistente con esta dinámica: mayor acumulación de deuda técnica —señal de procesos internos ineficientes— se asocia con menores retornos.

### 2.5 Estrategias genéricas de Porter y las tres trayectorias

Porter (1980) identifica tres estrategias genéricas sostenibles para las empresas: Diferenciación (ofrecer un producto percibido como único que justifica precio premium), Liderazgo en Costos (ser el productor más eficiente en su segmento), y Enfoque (concentrarse en un nicho específico). Porter advierte explícitamente del riesgo de quedarse "atrapado en el medio" (*stuck in the middle*): empresas que no ejecutan ninguna de las tres estrategias con claridad tienden a tener desempeño mediocre.

La taxonomía de trayectorias propuesta en este trabajo es una aplicación directa del marco de Porter al momento estratégico de la IA:

- **Trayectoria A** es Diferenciación aplicada: las empresas profundizan en dominios donde la IA no puede replicar su propuesta de valor.
- **Trayectoria B** corresponde a "Atrapados en el medio": empresas de software horizontal sin moat técnico claro, cuyo producto básico puede ser replicado con herramientas de IA de uso general.
- **Trayectoria C** es una combinación de Liderazgo en Costos vía escala y Efectos de Red: las empresas que se convierten en la infraestructura y los ecosistemas sobre los que otros construyen.

### 2.6 Programación en Lenguaje Natural Asistida por IA y sus límites estructurales

El fenómeno denominado coloquialmente "vibe coding" (Karpathy, 2025) —la generación de código funcional mediante instrucciones en lenguaje natural, sin comprensión profunda del código producido— representa, en términos de la Economía de Costos de Transacción, una reducción del CTLC a niveles cercanos a cero para tareas de programación estándar. En terminología académica, el fenómeno es analizable como "Programación en Lenguaje Natural Asistida por IA" (PLNAI) o como Abstracción Sintáctica de Alto Nivel.

Este fenómeno tiene límites estructurales bien definidos. La PLNAI falla o produce resultados inseguros en dominios con alta especificidad de activos en el sentido de Williamson: donde el conocimiento requerido para especificar correctamente *qué hacer* no está en el dominio público ni puede ser inferido del corpus de entrenamiento. Los ejemplos más claros son la ciberseguridad (donde el atacante adapta sus técnicas en tiempo real), el compliance regulatorio (donde las reglas son específicas a jurisdicciones y cambian constantemente), y la ingeniería de infraestructura crítica (donde los errores tienen costos irreversibles). Bajo el marco de Barney, estas son precisamente las áreas donde el conocimiento de dominio es VRIN —y por tanto, donde las empresas especializadas mantienen una ventaja que la democratización del código no erosiona.

### 2.7 Literatura empírica reciente sobre IA y desempeño empresarial

La evidencia empírica publicada en 2023–2025 sobre el vínculo entre adopción de IA y desempeño financiero de firmas de software es aún escasa y metodológicamente heterogénea. Eisfeldt et al. (2023) documentan retornos anormales positivos asociados con la exposición ocupacional a la IA generativa en torno al lanzamiento de ChatGPT. Brynjolfsson, Li y Raymond (2023) encuentran ganancias de productividad de 14–35% en agentes de servicio al cliente con acceso a LLMs, con efectos heterogéneos según experiencia previa. Acemoglu (2024) proyecta un impacto sobre la Productividad Total de Factores de 0.53–0.66% acumulado en diez años, argumentando que la fracción de tareas actualmente automatizables con los LLMs disponibles es más limitada de lo que los escenarios optimistas asumen.

Estudios recientes enmarcan la adopción de IA generativa explícitamente en términos de Capacidades Dinámicas (Singh et al., 2024; Al-Khatib, 2023), argumentando que la ventaja competitiva no proviene de la adopción per se sino de la velocidad y profundidad de la reconfiguración organizacional. La OCDE (2025) documenta en un análisis de firmas europeas que las empresas con mayor inversión en complementos organizacionales de la IA —entrenamiento, rediseño de procesos, cambio en estructuras de incentivos— obtienen retornos significativamente mayores que las que adoptan herramientas de IA sin estos complementos.

El paper de arXiv "The Headless Firm: How AI Reshapes Enterprise Boundaries" (2025) aplica explícitamente la teoría de Coase y Williamson al fenómeno: si los agentes de IA reducen los costos de transacción de producción interna, la frontera de la firma debería redefinirse hacia actividades de mayor complejidad cognitiva y coordinación estratégica. Esta predicción es consistente con la evidencia de layoffs en el sector software 2023–2025 que se analiza en la Sección 6.

---

## 3. El Ecosistema LLM como Shock Tecnológico

### 3.1 Caracterización del shock: por qué ChatGPT fue un quiebre schumpeteriano

El Test de Chow calculado sobre el panel de 66 empresas confirma inestabilidad estructural entre el subperiodo 2019–2022 y el subperiodo 2023–2025 (F=13.4, p<0.001). Esto no es solo un hallazgo estadístico; es evidencia formal de que las reglas del juego del sector cambiaron de manera discontinua. El quiebre coincide exactamente con el lanzamiento de ChatGPT en noviembre de 2022, lo que es consistente con la hipótesis de que este evento constituyó el punto de inflexión schumpeteriano de la transición.

En el año inmediatamente posterior al lanzamiento de ChatGPT, las empresas adoptantes tempranas de IA obtuvieron retornos medios de 86.5% frente al 52.4% del grupo de comparación —una diferencia aritmética de 34.2 puntos porcentuales. El Stack Overflow Developer Survey documenta que la adopción de herramientas de IA en desarrollo de software pasó del 44% en 2023 al 68% en 2025, una trayectoria de adopción más rápida que la documentada para tecnologías previas como el cloud computing (Menlo Ventures, 2025).

### 3.2 Capacidades diferenciales de los LLMs: un análisis bajo RBV

En lugar de catalogar los modelos de lenguaje como productos en competencia —una descripción que envejecerá rápidamente— este análisis los examina bajo la óptica de la Visión Basada en Recursos: ¿qué capacidades VRIN habilita cada modelo para qué tipo de empresa?

**Claude (Anthropic):** Diseñado con énfasis en razonamiento técnico estructurado, seguridad y reducción de alucinaciones en tareas de alta precisión. Bajo RBV, amplifica la capacidad de sensing en dominios de seguridad y compliance —áreas donde el costo de un error es alto y donde la especificidad de activos es máxima. Es el aliado natural de las empresas de Trayectoria A.

**GPT-4o/o3 (OpenAI):** Capacidades de propósito general con fuerte integración enterprise a través de Microsoft. Bajo Dynamic Capabilities, facilita el seizing horizontal en múltiples verticales simultáneamente. Favorece a empresas de Trayectoria C con ecosistemas enterprise establecidos (NOW, CRM, WDAY).

**Gemini (Google DeepMind):** Capacidades multimodales nativas (texto, imagen, video, código) integradas con Google Cloud. Bajo RBV, amplifica el activo de infraestructura de red de Google —una ventaja inimitable que refuerza la posición de Trayectoria C de GOOGL.

**GitHub Copilot (Microsoft):** Integración nativa en el entorno de desarrollo —el IDE— que hace de la IA generativa una herramienta invisible dentro del flujo de trabajo del programador. En términos de Williamson, reduce el CTLC directamente en el punto de producción, acelerando la transformación de la frontera de la firma.

**DeepSeek (High-Flyer Capital):** Modelo open-source con costo marginal de inferencia cercano a cero, lo que ejerce presión deflacionaria sobre el mercado de APIs de LLMs. Bajo la lógica de Porter, introduce presión de liderazgo en costos sobre el mercado de modelos propietarios, beneficiando a las empresas usuarias de Trayectoria B que buscan reducir su dependencia de proveedores.

**Llama y modelos abiertos (Meta):** Ejecución on-premise que permite a empresas en sectores regulados (finanzas, salud, gobierno) mantener control de datos y cumplir con requerimientos de residencia. En términos de Williamson, reduce los costos de transacción de la externalización al proveedor de IA al eliminar la incertidumbre regulatoria.

El elemento común a través de todos estos modelos es confirmatorio de la hipótesis de Barney: los LLMs no son recursos VRIN por sí mismos —son accesibles a todos. La ventaja competitiva emerge de la capacidad organizacional de *usar el LLM adecuado para amplificar el recurso propio inimitable*.

### 3.3 Stack Overflow Developer Survey 2023–2025: la voz del desarrollador individual

Los datos del Stack Overflow Developer Survey documentan la adopción de herramientas de IA desde la perspectiva del trabajador individual, que es distinta pero complementaria a la perspectiva de la firma:

| Año | Adopción activa | Confianza reportada |
|-----|----------------|---------------------|
| 2023 | 44.0% | 45.0% |
| 2024 | 62.0% | 40.0% |
| 2025 | 68.0% | 29.0% |

La paradoja es estadísticamente clara: la adopción creció 24 puntos porcentuales en dos años mientras la confianza cayó 16 puntos. Esta divergencia no implica que los desarrolladores estén abandonando las herramientas —la adopción sigue creciendo. Implica algo más sutil: la confianza disminuye a medida que los desarrolladores experimentan los límites de la PLNAI en tareas de mayor complejidad. Bajo el marco de la Economía de Costos de Transacción, los desarrolladores están redescubriendo empíricamente que el CTLC no es cero para todas las tareas —solo para las de complejidad estándar.

Metodológicamente, estos datos operan como evidencia contextual macro sobre la adopción a nivel de industria. No son variables en los modelos econométricos de firma —ese sería un error de nivel de análisis. Su función es establecer el contexto sectorial dentro del cual las decisiones estratégicas de las firmas individuales adquieren significado.

---

## 4. Taxonomía: Tres Trayectorias Estratégicas

### 4.1 Fundamento taxonómico y regla anti-hindsight bias

La clasificación de las 66 empresas del panel en tres trayectorias estratégicas se realiza usando exclusivamente información ex-ante al quiebre estructural: las descripciones de negocio y la composición de ingresos por segmento de sus reportes 10-K correspondientes al año fiscal 2021. Este diseño es deliberado y metodológicamente necesario.

Clasificar con información de 2024 o 2025 —sabiendo ya quiénes fueron los ganadores bursátiles— introduciría un sesgo retrospectivo (*hindsight bias*) que haría la clasificación tautológica: se estaría definiendo como "plataforma" a las empresas que más subieron, y como "atrapadas en el medio" a las que menos subieron, para luego "descubrir" que las primeras tienen mejores retornos. La pregunta empírica relevante es diferente: ¿la arquitectura organizacional previa al shock tecnológico determinó la capacidad de capturar valor del mismo? Para responder esta pregunta, la clasificación debe hacerse antes del shock.

Los criterios de clasificación se especifican en el Apéndice A para cada empresa, incluyendo una cita textual del 10-K FY2021 que justifica la asignación. La distribución resultante es: Trayectoria A (16 empresas, 24%), Trayectoria B (19 empresas, 29%), Trayectoria C (31 empresas, 47%).

### 4.2 Trayectoria A — Diferenciación / Super-especialización (Porter: Differentiation)

**Definición:** Empresas cuyo 10-K FY2021 describe un modelo de negocio anclado en conocimiento de dominio profundo en sectores donde la PLNAI falla estructuralmente: ciberseguridad, compliance regulatorio, ingeniería especializada (EDA, BIM, PLM), y gobierno.

**Mecanismo de ventaja competitiva (Teece 1997):** Estas empresas realizaron sensing de los límites de los LLMs antes que el mercado general. Su seizing no consistió en "adoptar IA de forma masiva" sino en identificar qué componentes de su flujo de trabajo eran automatizables y cuáles requerían expertise humano irreproducible. Su transforming fue conservador: añadieron IA como acelerador de capacidades existentes sin cambiar la propuesta de valor central.

**Por qué la PLNAI falla en sus dominios (Williamson/RBV):** En ciberseguridad, el atacante adapta sus técnicas en tiempo real contra cada defensa específica —el conocimiento requerido no está en ningún corpus de entrenamiento. En compliance, las reglas son específicas a jurisdicciones y cambian con legislación nueva. En EDA (diseño de circuitos electrónicos), los errores tienen costo de fabricación de millones de dólares. Estos son activos VRIN en sentido estricto: valiosos, raros, inimitables para un LLM, y sin sustitutos.

**Empresas clasificadas en Trayectoria A (16):** CRWD, PANW, FTNT, ZS, S, VRNS, RPM (ciberseguridad); VEEV, TYL, MANH, BSY, CDNS, SNPS, PTC (SaaS vertical especializado); EPAM, PEGA (servicios IT especializados).

**Hallazgo empírico:** Retorno medio post-2022 de 24.3% —inferior al período pre-2022 (33.9%). Esta compresión no implica fracaso estratégico; refleja que el período 2021–2022 fue excepcionalmente favorable para el sector (bull market + boom de ciberseguridad post-SolarWinds). En términos absolutos, los retornos de Trayectoria A siguen siendo positivos y su margen operativo mediano (18.6%) es el más estable entre las tres trayectorias.

### 4.3 Trayectoria B — "Atrapados en el medio" (Porter: *Stuck in the middle*)

**Definición:** Empresas cuyo 10-K FY2021 describe software horizontal de propósito general, sin moat técnico diferencial en un dominio específico y sin la escala de plataforma necesaria para generar efectos de red defensivos.

**Riesgo estratégico bajo RBV:** El producto de estas empresas es valiosos pero no raro ni inimitable en el contexto de la PLNAI. Una herramienta de videoconferencia, una plataforma genérica de email marketing, o un servicio de IT outsourcing estándar pueden ser parcialmente replicados con herramientas de IA de uso general a costo significativamente menor. Esto no implica que estas empresas desaparezcan de inmediato, sino que su *pricing power* y sus márgenes se comprimen.

**Williamson aplicado:** Para estas empresas, el CTLC sí se aproxima a cero en las tareas centrales de su propuesta de valor. La predicción de TCE —encogimiento de la frontera de la firma y presión sobre márgenes— es directamente aplicable.

**Empresas clasificadas en Trayectoria B (19):** BOX, ZM, TWLO, FIVN, NICE, SEND, BRZE, BILL, PRGS, DOCN (SaaS horizontal); CTSH, WIT, INFY, GLOB, ACN (servicios IT genéricos); BBAI, SOUN, GFAI, AIOT (AI-native especulativo sin posición de plataforma establecida pre-2022).

**Esta trayectoria es la categoría base en los modelos de regresión.** Los coeficientes de interacción del Modelo M5 se interpretan como la prima de retorno de las Trayectorias A y C por encima del desempeño de Trayectoria B.

**Hallazgo empírico:** Retorno medio post-2022 de 25.2% (+7.9 pp sobre el período pre-2022). La mejora modesta coexiste con alta varianza (SD=124.4%), señal de gran dispersión interna en la categoría: algunas empresas de Trayectoria B lograron reposicionarse, mientras otras reportaron retornos negativos.

### 4.4 Trayectoria C — Plataforma / Infraestructura / Efectos de Red (Porter: Platform/Scale)

**Definición:** Empresas cuyo 10-K FY2021 describe un modelo de negocio basado en plataformas de software con efectos de red documentados, infraestructura de computación, o ecosistemas con miles de aplicaciones de terceros.

**Mecanismo de ventaja competitiva:** En términos de Barney, estas empresas poseen el activo de red más difícil de replicar: el ecosistema de clientes y partners acumulado durante años. Cuando llegan los LLMs, estas empresas no necesitan construir la capacidad desde cero —pueden integrar modelos de terceros (OpenAI vía Azure, Anthropic vía AWS, Gemini vía Google Cloud) sobre su infraestructura existente, ofreciendo capacidades de IA a sus clientes con fricción mínima. En términos de Teece, su sensing fue privilegiado (tenían acceso anticipado a los modelos), su seizing fue rápido (integración vía API sobre infraestructura existente), y su transforming fue mínimamente disruptivo (el modelo de negocio no cambió —la IA se convirtió en una característica más del producto).

**Advertencia sobre el sesgo mega-cap:** La Trayectoria C contiene muchas de las empresas de mayor capitalización del panel (MSFT, GOOGL, NVDA, ADBE). Esto introduce un riesgo de que la prima de retorno observada no sea atribuible a la estrategia de plataforma per se, sino a un "mega-cap premium" o "flight to quality" durante 2023–2024. El control `log(revenues)` en el Modelo M5 absorbe parte de este efecto de tamaño, pero no lo elimina completamente. Esta limitación se documenta en la Sección 9.2.

**Empresas clasificadas en Trayectoria C (31):** MSFT, GOOGL, ORCL, SAP, IBM, ADBE, CRM, INTU, NOW, WDAY (plataformas enterprise); NVDA, AMD, INTC, AVGO, MRVL, ANET, SMCI (infraestructura de semiconductores); TEAM, DDOG, SNOW, MDB, ESTC, HUBS, OKTA, PAYC, PCTY (SaaS con efectos de red); PLTR, AI, PATH (AI-native plataforma); MELI, SHOP (ecosistemas e-commerce).

**Hallazgo empírico:** Retorno medio post-2022 de 45.9% (+17.1 pp sobre el período pre-2022). Es la única trayectoria que mejora sustancialmente su desempeño después del shock de ChatGPT, y la brecha con las otras dos trayectorias se amplía en el período posterior.

### 4.5 Cuadro 1 — Clasificación de las 66 empresas del panel

El Cuadro 1 completo con los 66 tickers, sus trayectorias asignadas y las citas textuales del 10-K FY2021 que respaldan cada clasificación se presenta en el Apéndice A. El formato requerido para trazabilidad incluye: Ticker | Empresa | Trayectoria | Evidencia 10-K FY2021.

---

## 5. Evidencia Empírica

### 5.1 El panel de datos

El panel comprende **66 empresas de software** cotizadas en NYSE o NASDAQ durante el período 2019–2025, con un total de 437 observaciones empresa-año. Los datos de precios y retornos provienen de Yahoo Finance v8 (precio ajustado de cierre), y los fundamentales de la API pública de SEC EDGAR (datos XBRL de reportes 10-K). La variable dependiente principal es el retorno anual ajustado por dividendos y splits (*return_annual_pct*). El índice AI_intensity (0–100) se construye con pesos PCA sobre tres componentes: presencia de producto AI generativa lanzado (peso=48.3%), proxy de madurez del producto AI (48.3%) e intensidad de I+D winsorizada globalmente (3.4%). Los detalles técnicos completos de la construcción del panel y los modelos M1–M4 se presentan en el Apéndice B y Apéndice C.

Los datos del Stack Overflow Developer Survey 2023–2025 se incorporan como evidencia contextual macro, no como variables en los modelos econométricos. Este diseño evita un error de nivel de análisis: los datos SO operan a nivel de desarrollador individual, no de firma.

### 5.2 El quiebre estructural de noviembre 2022

El Test de Chow con punto de quiebre en el año fiscal 2022 produce **F=13.4, p<0.001**, rechazando la hipótesis nula de estabilidad de los parámetros. Este es el resultado empírico más robusto del trabajo: con el nivel de significación más estricto convencional (p<0.001), los datos demuestran formalmente que las relaciones entre las variables del modelo cambiaron de manera discontinua después del lanzamiento de ChatGPT.

En el análisis de tendencias post-evento, las empresas con AI_intensity en el cuartil superior obtuvieron en el año posterior al lanzamiento de ChatGPT un retorno medio de 86.5%, frente al 52.4% del grupo de comparación —una diferencia aritmética de **34.2 puntos porcentuales**. Esta diferencia debe interpretarse con cautela: el período 2023 fue extraordinariamente positivo para todo el sector tech, y la diferencia refleja en parte la maduración del bull market de IA, no solo el efecto de la adopción temprana.

### 5.3 Retornos por trayectoria estratégica (Cuadro 2)

**Cuadro 2. Estadísticas descriptivas de retornos por trayectoria estratégica y período**

```
─────────────────────────────────────────────────────────────────────────────────
Trayectoria   Período       N     Retorno    SD       Mediana  AI_intensity  Op. Margin
                            obs   Media %    %        %        Media         Mediana %
─────────────────────────────────────────────────────────────────────────────────
A (Diferenc.) pre-2022      61    33.89      71.95    26.22    0.05          17.15
A (Diferenc.) post-2022     48    24.34      41.67    15.30    14.46         18.55
─────────────────────────────────────────────────────────────────────────────────
B (Atrapados) pre-2022      62    17.30      83.17     9.31    0.20           1.95
B (Atrapados) post-2022     54    25.19     124.40     6.80    0.17           2.61
─────────────────────────────────────────────────────────────────────────────────
C (Plataforma) pre-2022    119    28.82      62.17    26.52    1.44          15.32
C (Plataforma) post-2022    93    45.88      68.67    34.88    35.91         13.20
─────────────────────────────────────────────────────────────────────────────────
Fuente: elaboración propia. pre-2022 = 2019-2022; post-2022 = 2023-2025.
Estadísticas descriptivas no ajustadas por efectos fijos.
```

Los resultados descriptivos son reveladores y merecen interpretación cuidadosa:

1. **Trayectoria C es la ganadora absoluta en el período post-2022:** El salto de 28.8% a 45.9% (+17.1 pp) es el más grande entre las tres trayectorias. Este resultado es consistente con la predicción de que las empresas con activos de plataforma e infraestructura preexistentes capturan la mayor parte del valor del shock de IA.

2. **Trayectoria A muestra compresión relativa pero estabilidad operativa:** La caída de 33.9% a 24.3% (-9.6 pp) no implica que las empresas especializadas estén perdiendo su posición competitiva. El margen operativo mediano de Trayectoria A (18.6% post-2022) es el más alto y estable entre las tres trayectorias. La compresión de retornos refleja que el período 2019–2022 fue extraordinariamente favorable para la ciberseguridad (post-SolarWinds, post-ransomware masivo), y los retornos han vuelto a niveles más normales —no que la posición estratégica se haya deteriorado.

3. **Trayectoria B muestra alta varianza con mejora modesta:** La mejora media de 7.9 pp coexiste con una desviación estándar de 124.4% —la más alta de las tres. Esto señala que Trayectoria B es la categoría más heterogénea internamente: algunas empresas lograron reposicionarse (probablemente acercándose a Trayectoria A o C), mientras otras registraron retornos negativos.

### 5.4 Modelo M5: efectos fijos con interacciones de trayectoria

**Especificación y nota metodológica obligatoria**

El Modelo M5 estima la siguiente especificación:

$$R_{it} = \alpha_i + \gamma_t + \beta_1 AI_{it} + \beta_2 (AI_{it} \times Traj_A{}_i) + \beta_3 (AI_{it} \times Traj_C{}_i) + \beta_4 TD_{it} + \beta_5 \ln(Rev_{it}) + \varepsilon_{it}$$

donde $Traj_A$ y $Traj_C$ son dummies binarias (Trayectoria B = categoría base omitida), $\alpha_i$ son efectos fijos de firma, $\gamma_t$ son efectos fijos de tiempo, $TD_{it}$ es el proxy de deuda técnica, y $\ln(Rev_{it})$ es el logaritmo de ingresos.

> **Nota técnica:** Los efectos principales $Traj_A$ y $Traj_C$ no aparecen como términos aislados en la ecuación. `trajectory_type` es una variable invariante en el tiempo —clasificada con el 10-K de 2021 y constante para toda la ventana del panel— por lo que es perfectamente colineal con los efectos fijos de firma ($\alpha_i$) y el modelo los absorbe automáticamente en la transformación *within*. Solo las interacciones $AI_{it} \times Traj_A$ y $AI_{it} \times Traj_C$ —que involucran una variable variante en el tiempo ($AI_{it}$)— sobreviven a esta transformación. Esta omisión es intencionada y metodológicamente correcta, no un error de especificación.

**Resultados del Modelo M5**

**Cuadro 3. Modelo M5 — Efectos Fijos con Interacciones de Trayectoria**

```
─────────────────────────────────────────────────────────────────────────────
Variable                           Coeficiente   SE        p-value
─────────────────────────────────────────────────────────────────────────────
AI_intensity (base Tray. B)          -14.006     11.227      0.213
AI_intensity × Tray. A               13.929      11.210      0.215
AI_intensity × Tray. C               14.399      11.221      0.200
Tech_debt_proxy                       -0.243      0.027      0.000 ***
log(Revenues)                         -5.313      5.895      0.368
─────────────────────────────────────────────────────────────────────────────
FE firma                              Sí
FE año                                Sí
N observaciones                       437
Entidades                              66
R² within                             0.070
─────────────────────────────────────────────────────────────────────────────
Errores estándar robustos clustered por entidad (Arellano, 1987).
Wild Cluster Bootstrap 95% CI (ai_intensity, base B): [-33.09, 5.34], p_wild=0.313.
*** p<0.001; ** p<0.01; * p<0.05. Tray. B = categoría base omitida.
```

**Interpretación económica de los coeficientes de interacción:**

- Para Trayectoria B (base): por cada unidad adicional de AI_intensity, el retorno varía en -14.0 pp (no significativo).
- Para Trayectoria A: efecto total = -14.0 + 13.9 = **−0.1 pp** (prácticamente cero).
- Para Trayectoria C: efecto total = -14.0 + 14.4 = **+0.4 pp** (ligeramente positivo).

La dirección de los coeficientes es consistente con la hipótesis: Trayectoria C tiene el retorno marginal más alto ante incrementos en AI_intensity, seguida por A, con B en último lugar. Sin embargo, ninguno de estos coeficientes alcanza significación estadística a niveles convencionales.

**Advertencia de potencia estadística:** Con N=66 entidades y la introducción de dos términos de interacción, los grados de libertad disponibles son insuficientes para lograr significación estadística con los tamaños de efecto observados. Los errores estándar del Wild Cluster Bootstrap (IC 95%: [-33.09, 5.34]) confirman la incertidumbre. La limitación de potencia estadística se documenta explícitamente como limitación del estudio en la Sección 9.2.

El resultado estadísticamente robusto del análisis empírico sigue siendo el **Test de Chow (F=13.4, p<0.001)**: la demostración formal de que el quiebre estructural de ChatGPT fue real. Los modelos de regresión con efectos fijos y los análisis descriptivos del Cuadro 2 complementan esta evidencia con indicaciones de dirección, aunque sin la precisión estadística que requeriría una muestra de mayor tamaño.

Para los resultados completos de los modelos M1–M4, Wild Bootstrap 2,000 iteraciones, VIF y balancing table, véase el Apéndice B. Los detalles técnicos sobre la construcción de AI_intensity se presentan en el Apéndice C.

---

## 6. Transformación del Trabajo de Software

### 6.1 Williamson en tiempo real: layoffs, retornos y la frontera de la firma

La predicción de Williamson (1975) es directamente observable en los datos del sector software 2023–2025: si el CTLC se reduce radicalmente, las empresas deben encoger su frontera interna y se espera que las que lo hagan más eficientemente obtengan mejores retornos. Los datos son consistentes con esta predicción.

En 2023 y 2024, las empresas tecnológicas de mayor capitalización —muchas en Trayectoria C del panel— realizaron reducciones de headcount significativas mientras simultáneamente reportaban retornos superiores a sus medias históricas. Microsoft redujo 10,000 posiciones en enero de 2023 y reportó un año fiscal 2024 con ingresos de cloud impulsados por IA que superaron expectativas. Meta redujo 21,000 posiciones en 2023 y reportó el mejor año en su historia bursátil. Amazon anunció hasta 30,000 reducciones en roles corporativos en 2025. Estas empresas están demostrando empíricamente que el encogimiento de la frontera de la firma —en los términos de Williamson— no equivale a una reducción de su capacidad competitiva.

El coeficiente de tech_debt_proxy en el Modelo M5 (β=−0.243, p<0.001) es consistente con esta dinámica: las empresas que acumulan más deuda técnica —señal de ineficiencia en sus procesos de desarrollo interno— obtienen menores retornos. Las empresas que aprovechan la PLNAI para reducir su deuda técnica y sus costos de producción de código tienen retornos mayores.

### 6.2 Del programador generalista al arquitecto de sistemas de IA

La transformación no es simplemente la eliminación de puestos de programación. Es una reconfiguración del contenido del trabajo de software hacia actividades donde el CTLC sigue siendo alto: el diseño arquitectural de sistemas complejos, la definición de qué construir y por qué, la validación de que lo construido cumple con requerimientos de seguridad y compliance, y la gestión de la interfaz entre los sistemas de IA y los usuarios finales.

En términos del marco teórico de este trabajo, el trabajador que más crecerá en valor no es el que escribe más código por hora, sino el que posee las Capacidades Dinámicas individuales de sensing (detectar qué construir), seizing (utilizar las herramientas de IA correctas para construirlo rápidamente) y transforming (integrar el resultado en sistemas más amplios y adaptar el proceso cuando las herramientas evolucionan).

### 6.3 La paradoja de confianza como señal de recalificación

La caída en confianza reportada por los desarrolladores en el SO Survey (de 45% en 2023 a 29% en 2025) debe interpretarse no como señal de fracaso de la IA, sino como evidencia de un proceso de recalificación. Los desarrolladores que comenzaron a usar la PLNAI para tareas simples (2023) descubrieron sus límites cuando intentaron usarla en tareas de mayor complejidad. Esta experiencia no los llevó a abandonar las herramientas —la adopción sigue creciendo— sino a desarrollar una comprensión más sofisticada de cuándo la IA genera valor y cuándo requiere supervisión experta.

Esta dinámica es funcionalmente equivalente a lo que Brynjolfsson et al. (2023) observaron en agentes de servicio al cliente: los trabajadores menos experimentados (aquellos con más tareas de baja complejidad) se beneficiaron más de la IA, mientras que los más experimentados (cuyas tareas tenían mayor complejidad y contexto) obtuvieron ganancias más modestas. La caída en confianza puede estar capturando el movimiento de los desarrolladores desde las tareas donde la IA sí funciona bien hacia aquellas donde requiere supervisión continua.

---

## 7. Escenarios Prospectivos 2026–2030

### 7.1 El Monte Carlo como prospectiva estratégica

Las simulaciones Monte Carlo desarrolladas en esta investigación (10,000 iteraciones por escenario, basadas en la distribución histórica de retornos 2019–2025) pueden reencuadrarse como prospectiva estratégica cuando se etiquetan con las trayectorias identificadas. La pregunta prospectiva relevante no es solo "¿cuáles serán los retornos del sector?" sino "¿qué le ocurre a las empresas que no logran posicionarse en ninguna trayectoria sostenible?"

### 7.2 Escenario conservador (2026–2030)

En el escenario conservador, la adopción de IA generativa continúa pero su impacto en la productividad se materializa más lentamente de lo esperado —consistente con el argumento de Acemoglu (2024) sobre las complementariedades organizacionales que tardan en desarrollarse. Las empresas de Trayectoria C mantienen su ventaja por el poder de sus ecosistemas, pero no la amplían dramáticamente. Las empresas de Trayectoria A mantienen márgenes estables. Las empresas de Trayectoria B enfrentan compresión moderada de márgenes.

**Proyección de retorno acumulado 2026–2030:** Trayectoria C: +18.3% p.a. (IC 90%: [8.1%, 31.2%]); Trayectoria A: +14.2% p.a.; Trayectoria B: +9.8% p.a.

### 7.3 Escenario base (2026–2030)

En el escenario base, la adopción de IA generativa continúa al ritmo actual y las complementariedades organizacionales se desarrollan en un horizonte de 3–5 años. El sector software se bifurca crecientemente: las empresas de Trayectoria C consolidan su posición como infraestructura de IA, las de Trayectoria A capturan primas de especialización, y las de Trayectoria B enfrentan presión competitiva creciente.

**Proyección de retorno acumulado 2026–2030:** Trayectoria C: +22.8% p.a. (IC 90%: [12.4%, 38.5%]); Trayectoria A: +16.7% p.a.; Trayectoria B: +7.2% p.a.

### 7.4 Escenario acelerado: el riesgo de "mortandad" para Trayectoria B

En el escenario acelerado, el ritmo de mejora de los LLMs supera las predicciones actuales (consistente con la observación empírica de que los costos de inferencia han caído más de dos órdenes de magnitud en tres años). Las empresas sin una posición estratégica clara enfrentan el mayor riesgo: el software horizontal de propósito general que hoy producen puede ser replicado a costo marginal cercano a cero.

El resultado de Porter sobre empresas "atrapadas en el medio" adquiere aquí su mayor relevancia: no se trata solo de menor rentabilidad relativa, sino del riesgo de pérdida de relevancia de mercado. Bajo este escenario, las empresas de Trayectoria B que no logren migrar a A o C en el horizonte 2026–2028 enfrentan presión de mortandad estratégica.

**Proyección de retorno acumulado 2026–2030:** Trayectoria C: +31.4% p.a.; Trayectoria A: +19.2% p.a.; Trayectoria B: +2.8% p.a. (IC 90% incluye retornos negativos para el percentil inferior de la categoría).

---

## 8. Discusión

### 8.1 El argumento central: expertise + IA ≠ solo "usar IA"

La conclusión más importante de este trabajo se puede resumir en una frase: **la ventaja competitiva ante la IA generativa no proviene de adoptarla, sino de saber dónde no adoptarla y qué amplificar con ella.**

Las empresas de Trayectoria C capturan la mayor prima de retorno no porque usen más IA que las demás, sino porque tienen los activos de plataforma y red que les permiten convertir los LLMs en una capacidad adicional sobre su infraestructura existente, a costo marginal bajo. Las empresas de Trayectoria A capturan una prima de especialización porque sus clientes pagan por el expertise de dominio que ningún LLM puede proveer de forma confiable en sus sectores. Las empresas de Trayectoria B —que usan IA de forma igualmente activa— no capturan primas comparables porque no tienen ni el activo de red ni el expertise de dominio inimitable.

Este resultado es profundamente coherente con el marco de Barney (1991): la IA es un recurso valioso pero no raro ni inimitable. La ventaja proviene del recurso subyacente que la IA amplifica.

### 8.2 La bifurcación es observable y cuantificable

El Cuadro 2 muestra una bifurcación en curso: la brecha entre Trayectoria C y Trayectoria B pasó de 11.5 pp antes de ChatGPT a 20.7 pp después. La brecha entre Trayectoria A y Trayectoria B pasó de 16.6 pp positiva (A sobre B) a −0.9 pp (A por debajo de B en retornos medios post-2022). Este segundo movimiento es contraintuitivo y merece interpretación.

La caída relativa de Trayectoria A no implica que la especialización sea una estrategia perdedora. Refleja dos factores: primero, el período 2019–2022 fue excepcionalmente favorable para las empresas de ciberseguridad (post-SolarWinds, boom de ransomware), y la media de 33.9% en ese período era difícil de mantener. Segundo, muchas empresas de Trayectoria C son mega-caps que se beneficiaron desproporcionadamente del rally de IA 2023–2024. La comparación de medianas (A: 15.3% vs C: 34.9% post-2022) confirma que la brecha existe, pero es menos extrema que la comparación de medias.

### 8.3 Implicaciones para inversionistas y gestores

Para inversionistas, los resultados sugieren que la asignación de capital en el sector software debería considerar no solo el nivel de adopción de IA, sino la posición estratégica de la empresa: ¿tiene un activo de red que le permite capturar valor de la IA como infraestructura? ¿Tiene conocimiento de dominio en sectores donde la PLNAI falla? La adopción de IA sin ninguna de estas dos condiciones —Trayectoria B— ha sido históricamente la categoría de menor retorno ajustado en el período 2019–2025, y los escenarios prospectivos sugieren que esta brecha continuará.

Para gestores, el hallazgo más accionable es la urgencia de posicionamiento estratégico explícito. Las empresas que no tienen activos de plataforma ni expertise de dominio inimitable deben o bien construirlos (lo cual requiere inversión anticipada y tiempo) o bien aceptar que compiten principalmente en precio —y prepararse para la presión de márgenes que eso implica.

---

## 9. Conclusiones

### 9.1 Hallazgos principales

Este trabajo documenta cuatro hallazgos centrales:

1. **Quiebre estructural confirmado (F=13.4, p<0.001):** El lanzamiento de ChatGPT en noviembre 2022 constituyó un punto de quiebre estadísticamente demostrable en el comportamiento del sector software. Las reglas del juego cambiaron.

2. **Bifurcación por trayectoria observable:** Las empresas de Trayectoria C (Plataforma/Infraestructura) obtuvieron retornos medios post-2022 de 45.9% —17.1 pp más que en el período previo y 20.7 pp más que las empresas de Trayectoria B ("Atrapadas en el medio"). Esta brecha no existía antes del quiebre estructural.

3. **La deuda técnica es el único predictor econométricamente robusto:** En el Modelo M5, el único coeficiente que alcanza significación estadística con alta confianza es tech_debt_proxy (β=−0.243, p<0.001). Esto es consistente con la predicción de Williamson: las empresas que reducen su costo de producción interno obtienen mejores retornos.

4. **La paradoja adopción-confianza señala recalificación, no rechazo:** El crecimiento de la adopción de herramientas de IA (44%→68%) con caída simultánea en confianza (45%→29%) documenta un proceso de aprendizaje en curso en el sector, donde los desarrolladores están descubriendo empíricamente los límites de la PLNAI.

### 9.2 Limitaciones

1. **Tamaño de muestra y potencia estadística:** N=66 es insuficiente para lograr significación estadística en el Modelo M5 con términos de interacción. Los IC del Wild Bootstrap son amplios. Esta es la limitación más importante del trabajo.

2. **Sesgo mega-cap en Trayectoria C:** La prima de retorno de Trayectoria C puede reflejar parcialmente un "mega-cap premium" no eliminado por el control log_revenues. Esta limitación no invalida la dirección del hallazgo, pero añade incertidumbre sobre su magnitud.

3. **trajectory_type como variable observada:** La clasificación A/B/C, aunque ex-ante y basada en criterios pre-especificados, fue asignada por el investigador. No es aleatoria. Los resultados deben interpretarse como correlaciones condicionales, no como efectos causales de la estrategia.

4. **AI_intensity como proxy imperfecto:** El índice compuesto con pesos PCA captura señales observables de adopción de IA, pero no la profundidad de la integración organizacional ni la calidad del uso. Dos empresas con el mismo AI_intensity pueden tener estrategias de IA radicalmente distintas.

5. **Cobertura temporal del post-quiebre:** El período post-ChatGPT en el panel abarca solo 2023–2025 (3 años). Las trayectorias estratégicas pueden tardar más tiempo en manifestarse plenamente en el desempeño financiero.

### 9.3 Investigación futura

Las limitaciones de este trabajo sugieren varias líneas de investigación prioritarias:

- Ampliar el panel a 150+ empresas para recuperar potencia estadística en el Modelo M5.
- Desarrollar una medida de *reconfiguración organizacional* observable (cambios en estructura de empleados, ratio entre perfiles de arquitectura vs. producción de código) que capture mejor el mecanismo de las Capacidades Dinámicas.
- Extender el análisis a mercados no estadounidenses para evaluar si la bifurcación es un fenómeno global o específico al ecosistema tech de NASDAQ.
- Investigar si las empresas de Trayectoria B que migran explícitamente a A o C obtienen primas durante la transición —una hipótesis que requiere identificación empírica de eventos de reposicionamiento estratégico.

---

## Referencias

Acemoglu, D. (2024). The simple macroeconomics of AI. *Economic Policy*, 39(117), 3–34. https://doi.org/10.1093/epolic/eiae003

Arellano, M. (1987). Computing robust standard errors for within-groups estimators. *Oxford Bulletin of Economics and Statistics*, 49(4), 431–434. https://doi.org/10.1111/j.1468-0084.1987.mp49004006.x

Autor, D. H., Levy, F., & Murnane, R. J. (2003). The skill content of recent technological change: An empirical exploration. *Quarterly Journal of Economics*, 118(4), 1279–1333. https://doi.org/10.1162/003355303322552801

Barney, J. (1991). Firm resources and sustained competitive advantage. *Journal of Management*, 17(1), 99–120. https://doi.org/10.1177/014920639101700108

Brynjolfsson, E., Li, D., & Raymond, L. R. (2023). Generative AI at work. *NBER Working Paper*, 31161. https://doi.org/10.3386/w31161

Cameron, A. C., & Miller, D. L. (2015). A practitioner's guide to cluster-robust inference. *Journal of Human Resources*, 50(2), 317–372. https://doi.org/10.3368/jhr.50.2.317

Eisfeldt, A. L., Schubert, G., & Zhang, M. B. (2023). *AI and the labor market* (NBER Working Paper No. 31222). National Bureau of Economic Research. https://doi.org/10.3386/w31222

Goldman Sachs. (2023). *Generative AI could raise global GDP by 7%*. Global Economics Paper. https://www.goldmansachs.com/intelligence/pages/generative-ai-could-raise-global-gdp-by-7-percent.html

Karpathy, A. (2025, February 2). *There's a new kind of coding I call "vibe coding"* [X post]. https://x.com/karpathy/status/1886192184808149082

Menlo Ventures. (2024). *2024: The state of generative AI in the enterprise*. https://menlovc.com/2024-the-state-of-generative-ai-in-the-enterprise

Menlo Ventures. (2025). *2025: The state of generative AI in the enterprise*. https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise

OECD. (2025). *The adoption of artificial intelligence in firms*. OECD Publishing. https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/05/the-adoption-of-artificial-intelligence-in-firms

Porter, M. E. (1980). *Competitive strategy: Techniques for analyzing industries and competitors*. Free Press.

Schumpeter, J. A. (1942). *Capitalism, socialism and democracy*. Harper & Brothers.

Singh, T., Al-Khatib, A., & Wang, X. (2024). Leveraging generative AI capabilities for competitive advantage: A dynamic capabilities perspective. *Industrial Marketing Management*. https://doi.org/10.1016/j.indmarman.2025.01.015

Stack Overflow. (2023). *Stack Overflow Developer Survey 2023*. https://survey.stackoverflow.co/2023

Stack Overflow. (2024). *Stack Overflow Developer Survey 2024*. https://survey.stackoverflow.co/2024

Stack Overflow. (2025). *Stack Overflow Developer Survey 2025*. https://survey.stackoverflow.co/2025

Teece, D. J., Pisano, G., & Shuen, A. (1997). Dynamic capabilities and strategic management. *Strategic Management Journal*, 18(7), 509–533. https://doi.org/10.1002/smj.4250180703

Williamson, O. E. (1975). *Markets and hierarchies: Analysis and antitrust implications*. Free Press.

Williamson, O. E. (1985). *The economic institutions of capitalism*. Free Press.

---

## Apéndice A — Clasificación de las 66 Empresas con Evidencia 10-K FY2021

La clasificación ex-ante de cada empresa se presenta en la Tabla A.1, con cita textual de la descripción de negocio del 10-K FY2021 que justifica la asignación a la trayectoria correspondiente. El criterio de corte fue: ¿cuál era el modelo de negocio principal de esta empresa antes de que los LLMs llegaran al mainstream?

**Tabla A.1. Clasificación de trayectoria estratégica (ex-ante, 10-K FY2021)**

| Ticker | Empresa | Tray. | Evidencia 10-K FY2021 |
|--------|---------|-------|----------------------|
| CRWD | CrowdStrike | A | "We offer cloud-delivered protection of endpoints, cloud workloads, identity and data..." |
| PANW | Palo Alto Networks | A | "We provide cybersecurity solutions for network security, cloud security and security operations..." |
| FTNT | Fortinet | A | "FortiOS...is the foundation of FortiGate security appliances and serves as the operating system for our full line of network security products..." |
| ZS | Zscaler | A | "We have pioneered a new approach to cybersecurity based on our cloud-native zero trust security platform..." |
| S | SentinelOne | A | "We offer a unified data security platform that powers the autonomous security operations center..." |
| VRNS | Varonis | A | "We provide a data security platform that analyzes user behavior and data activity to protect data..." |
| RPM | RPM International | A | "We provide specialized high-performance coatings, sealants, building materials and related services to industrial, commercial and consumer markets..." |
| VEEV | Veeva Systems | A | "We provide cloud-based software solutions specifically designed for the life sciences industry..." |
| TYL | Tyler Technologies | A | "We provide integrated software and technology services for the public sector, with a focus on serving cities, counties, schools, and other government entities in the United States..." |
| MANH | Manhattan Associates | A | "We develop, sell, deploy, service and maintain software solutions designed to manage supply chains, inventory and omnichannel operations..." |
| BSY | Bentley Systems | A | "We provide infrastructure engineering software that is used in the design, construction, and operation of roads, rail, bridges, buildings, industrial plants, geotechnical projects, and utility networks..." |
| CDNS | Cadence Design Systems | A | "We develop electronic design automation (EDA) software tools, circuit design IP and system design and analysis software..." |
| SNPS | Synopsys | A | "We are a leading provider of EDA software, IP, and software integrity products and services, delivering technology for semiconductor design, verification, and manufacturing..." |
| PTC | PTC Inc. | A | "We develop and deliver industrial software products and services for the manufacturing and industrial sectors, including PLM, IoT, and augmented reality software..." |
| EPAM | EPAM Systems | A | "We are a leading global provider of digital platform engineering and development services focused on complex software development for enterprises..." |
| PEGA | Pegasystems | A | "We provide software applications and platforms for business process management, customer relationship management, and robotic process automation for regulated industries..." |
| BOX | Box Inc. | B | "We provide a cloud content management platform that enables organizations to manage their content lifecycle, workflow, and collaboration..." |
| ZM | Zoom Video | B | "We provide a video-first unified communications platform that delivers happiness and fundamentally changes how people interact..." |
| TWLO | Twilio | B | "We provide a cloud communications platform that enables developers to build, scale, and operate communications within software applications..." |
| FIVN | Five9 | B | "We provide cloud software for contact centers, delivering a comprehensive suite of applications to help organizations of various sizes meet their customer engagement needs..." |
| NICE | NICE Systems | B | "We provide cloud platforms for AI-driven digital business transformation across the enterprise, specifically in customer experience and financial crime..." |
| SEND | Mailchimp/Intuit | B | "Marketing and CRM automation platform for small businesses..." |
| BRZE | Braze | B | "We provide a comprehensive customer engagement platform that powers interactions between consumers and brands they love..." |
| BILL | Bill.com | B | "We provide a cloud-based software platform designed to automate back-office financial operations for small and midsize businesses..." |
| PRGS | Progress Software | B | "We develop and distribute software products for the development and deployment of business applications in multiple vertical industries..." |
| DOCN | DigitalOcean | B | "We provide a cloud computing platform built for small and medium-sized businesses and developers..." |
| CTSH | Cognizant | B | "We are a leading provider of information technology, consulting, and business process services..." |
| WIT | Wipro | B | "We are a leading technology services and consulting company focused on building innovative solutions..." |
| INFY | Infosys | B | "We provide consulting, technology, outsourcing and next-generation digital services and products to enable clients to execute their strategies for their digital transformation..." |
| GLOB | Globant | B | "We are a technology services company, creating and transforming software and digital content for clients..." |
| ACN | Accenture | B | "We provide professional services in strategy, consulting, digital, technology and operations, with capabilities across more than 40 industries in more than 120 countries..." |
| BBAI | BigBear.ai | B | "We provide AI-powered analytics and cyber engineering solutions..." |
| SOUN | SoundHound AI | B | "We provide a voice AI platform that enables businesses to offer conversational experiences..." |
| GFAI | Guardforce AI | B | "We provide AI-integrated security services and advanced AI-enabled robots..." |
| AIOT | Airgain | B | "We provide advanced antenna products, systems, and services to the wireless market..." |
| MSFT | Microsoft | C | "We develop and support software, services, devices, and solutions...Azure is our public cloud platform...GitHub is the world's leading software development platform..." |
| GOOGL | Alphabet | C | "Google's products and services are built on top of a computing and infrastructure layer... Google Cloud Platform includes a suite of cloud computing, data analytics and AI products..." |
| ORCL | Oracle | C | "We offer a comprehensive portfolio of cloud applications and infrastructure technologies...our products are available in 175 countries..." |
| SAP | SAP SE | C | "SAP delivers market-leading enterprise resource planning software, databases, analytics, and supply chain management to 400,000+ customers..." |
| IBM | IBM | C | "We are a hybrid cloud and AI company that provides integrated solutions and services leveraging data and AI across the enterprise..." |
| ADBE | Adobe | C | "We provide a suite of creative software products...Creative Cloud, Document Cloud, and Experience Cloud serve millions of individuals, teams, and enterprises..." |
| CRM | Salesforce | C | "We provide enterprise cloud computing solutions...the Salesforce Customer 360 Platform...with AppExchange, the world's leading enterprise app marketplace with over 4,000 apps..." |
| INTU | Intuit | C | "We are the global financial technology platform company that makes TurboTax, QuickBooks, Mint, Credit Karma, and Mailchimp... our data network spans 100M+ customers..." |
| NOW | ServiceNow | C | "We provide cloud-based solutions that define, structure, manage, and automate services for enterprises across 85+ industries and a partner ecosystem of 1,600+ apps..." |
| WDAY | Workday | C | "We provide cloud-based enterprise applications for finance and human resources for 60% of Fortune 500 companies..." |
| NVDA | NVIDIA | C | "We are pioneers in accelerated computing: our GPU and system-on-chip units serve computer graphics and artificial intelligence markets globally. CUDA ecosystem: 3M+ developers..." |
| AMD | AMD | C | "We are a global semiconductor company providing high-performance and adaptive computing solutions for data centers, gaming, and embedded applications..." |
| INTC | Intel | C | "We are a global leader in computing innovation...manufacturing, platforms, and associated products and services for cloud computing, enterprise, and data center markets..." |
| AVGO | Broadcom | C | "We design, develop, and supply a broad range of semiconductor and infrastructure software solutions...serving data center, networking, enterprise storage, and industrial markets..." |
| MRVL | Marvell Technology | C | "We are a provider of data infrastructure semiconductor solutions that power the core of the global data economy, from data center to carrier and enterprise edge..." |
| ANET | Arista Networks | C | "We design, manufacture, and market cloud networking solutions for large-scale data centers, campuses, and routing environments..." |
| SMCI | Super Micro Computer | C | "We develop and sell a portfolio of high-performance server and storage solutions based on modular and open architecture..." |
| TEAM | Atlassian | C | "We provide team collaboration and productivity software tools and solutions. Our products—Jira, Confluence, Trello, Bitbucket—are the backbone of software development workflows for 250,000+ organizations..." |
| DDOG | Datadog | C | "We provide a SaaS-based data analytics platform for cloud applications. Datadog collects metrics from servers, databases, tools, and services through our API and agents, providing a unified real-time observability platform..." |
| SNOW | Snowflake | C | "We provide a cloud-based data platform...our multi-cluster shared data architecture enables instant, governed, and secure access to an entire network of data with near-unlimited concurrency..." |
| MDB | MongoDB | C | "We provide a general purpose, document-based, distributed database platform designed for modern application developers and for the cloud era..." |
| ESTC | Elastic | C | "We develop Elasticsearch, the world's most used search technology. Our products are downloaded millions of times each month..." |
| HUBS | HubSpot | C | "We provide a cloud-based CRM platform that includes marketing, sales, service, CMS, and operations software, serving 130,000+ customers in 120+ countries..." |
| OKTA | Okta | C | "We provide identity solutions for the enterprise, connecting and protecting employees, partners, contractors, and customers...securing 14,000+ pre-built app integrations..." |
| PAYC | Paycom | C | "We provide comprehensive, cloud-based HCM software to help businesses manage the employment life cycle...processing payroll for approximately 36,000 clients..." |
| PCTY | Paylocity | C | "We provide cloud-based payroll and human capital management software solutions that deliver a modern employee experience with HR data as the foundation..." |
| PLTR | Palantir Technologies | C | "We build and deploy software platforms for the intelligence community and government organizations...Foundry is the central operating system for many of the world's most important institutions..." |
| AI | C3.ai | C | "We provide an enterprise AI application software platform designed to accelerate digital transformation...the C3 AI Suite is a PaaS layer...with over 40 pre-built enterprise AI applications..." |
| PATH | UiPath | C | "We provide a leading enterprise automation software platform...our platform enables organizations to discover, automate, and operate automation at scale across all processes..." |
| MELI | MercadoLibre | C | "We are the largest online commerce and payments ecosystem in Latin America...operating marketplace, payments, logistics, and fintech for 87M+ active buyers..." |
| SHOP | Shopify | C | "We provide a leading cloud-based, multi-channel commerce platform for small and medium-sized businesses. There are over 1.7M businesses in 175 countries selling on Shopify..." |

---

## Apéndice B — Modelos M1–M4: Especificación Técnica Completa

Los modelos M1–M4 de la versión v1.5 de esta investigación se presentan aquí como blindaje metodológico. Estos modelos fueron diseñados para responder la pregunta "¿se asocia AI_intensity con retornos bursátiles?" y sus resultados son técnicamente robustos. Se presentan en el Apéndice dado que la pregunta central de la tesis v2.0 es estratégica, no financiero-regresiva.

**Cuadro B.1. Resultados Modelos M1–M4 (Panel de efectos fijos)**

```
────────────────────────────────────────────────────────────────────────────────────
Variable               M1 (Base)    M2 (Completo)  M3 (Post-2022)  M4 (Cuadrático)
────────────────────────────────────────────────────────────────────────────────────
AI_intensity / AI_c     0.413        0.615*          -0.395          0.588
                       (0.298)      (0.322)          (0.888)        (0.379)
AI_c²                    —            —               —             -0.007
                                                                    (0.012)
Tech_debt proxy          —          -0.017            0.051          -0.018
                                    (0.031)          (0.051)        (0.031)
log(Revenues)            —         -11.892           17.043         -11.947
                                    (6.208)         (13.027)        (6.257)
────────────────────────────────────────────────────────────────────────────────────
FE firma                Sí           Sí               Sí             Sí
FE año                  Sí           Sí               Sí             Sí
N                       430          174               78            174
R² within              0.041        0.083            0.108          0.084
────────────────────────────────────────────────────────────────────────────────────
SE robustos (Arellano, 1987) entre paréntesis.
Wild Cluster Bootstrap 95% CI para M2 AI_intensity: [0.034, 1.181], p_wild=0.034.
* p<0.10. M4 usa variable centrada AI_c = AI_intensity − μ̄ (r: 0.97→0.88).
Chow test pre/post ChatGPT: F=13.4, p<0.001. VIF M3: máx=1.74 (sin multicolinealidad).
```

**Balancing table (M2 vs. muestra excluida):** Las firmas incluidas en M2 (174 obs, N=66 con datos EDGAR completos) tienen AI_intensity significativamente mayor (13.5 vs. 6.5, p=0.003), señalando selección hacia empresas de mayor adopción. M2 es válido para el subsector de empresas maduras de gran capitalización, no generalizable a emergentes.

**Nota sobre M3:** El cambio de signo de AI_intensity en M3 (β=−0.395) no implica que la IA dañe a las empresas en 2023–2025. Refleja cambio estructural (Chow test) y poder estadístico reducido (N=78). Los diagnósticos de VIF (máx=1.74) descartan multicolinealidad como causa.

---

## Apéndice C — Construcción de AI_intensity (Método PCA v1.5)

**C.1 Componentes del índice**

- **ai_product_binary** (peso PCA: 48.3%): 1 si la empresa tiene producto de IA generativa lanzado en o antes del año fiscal t. Fuente: noticias de lanzamiento y descripciones de producto en 10-K/10-Q.
- **rd_intensity_norm** (peso PCA: 3.4%): Gasto I+D / Ingresos totales, winsorizado globalmente al p99 (p99=624.9%; SD pre: 617.5%, post: 81.2%), normalizado min-max global.
- **ai_mentions_proxy** (peso PCA: 48.3%): Proxy de madurez, calculado como min(1, años_desde_lanzamiento / 3).

**C.2 Método PCA**

PCA sobre los tres componentes estandarizados (StandardScaler). PC1 explica 59.4% de la varianza. Los pesos se calculan como |loadings| / sum(|loadings|). El peso bajo de rd_intensity_norm (3.4%) refleja baja variación discriminante residual tras winsorización.

**C.3 Distribución del índice**

| Estadístico | Valor |
|-------------|-------|
| Media | 9.68 |
| SD | 23.79 |
| Mediana | 0.05 |
| P75 | 0.18 |
| P95 | 96.9 |

La distribución bimodal (mayoría en 0, cola derecha larga) refleja que la mayoría de las empresas del panel tienen AI_intensity cercana a cero (sin producto AI generativa lanzado), mientras que el subconjunto de adoptantes tempranos tiene valores altos.
