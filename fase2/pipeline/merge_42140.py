import json

# Load partial files
with open('corpus/intermedios/11362/42140/parcial_modulos_1_3.json', 'r', encoding='utf-8') as f:
    part1 = json.load(f)

with open('corpus/intermedios/11362/42140/parcial_modulos_4_6.json', 'r', encoding='utf-8') as f:
    part2 = json.load(f)

# Merge resumen_secciones
resumen_secciones_merged = part1['resumen_secciones'] + part2['resumen_secciones']

# Construct the final JSON structure
final_json = {
  "documento": {
    "num_muestra": 53,
    "titulo": "Energía, cambio climático y desarrollo sostenible: los desafíos para América Latina",
    "autoria": None,
    "handle": "https://hdl.handle.net/11362/42140",
    "simbolo": "LC/MEX/TS.2017/22",
    "isbn": None,
    "fecha": "2017-09",
    "tipo_documento": "Compilación de estudios técnicos",
    "paginas_cuerpo": 534,
    "paginas_totales": 534,
    "idioma": "es",
    "tiene_resumen_ejecutivo": False
  },
  "resumen_enriquecido": {
    "pregunta_investigacion": "¿Cuáles son los principales desafíos regulatorios, institucionales y tecnológicos que enfrenta América Latina para transformar su matriz energética y lograr un desarrollo sostenible compatible con la mitigación y adaptación al cambio climático?",
    "alcance": {
      "ambito_aplicacion": "América Latina y el Caribe (con especial enfoque en México, Cuba, Costa Rica, Honduras y Centroamérica)",
      "referentes_dependencias": "Naciones Unidas (Agenda 2030, SCAEI); Unión Europea (ExternE, EcoSense); OIEA (SIMPACTS); Estados Unidos (BenMAP, importaciones de vehículos usados); India (Ministerio de Energías Renovables, Misión Solar India)",
      "sectorial": "Energía, electricidad, transporte terrestre, biocombustibles, regulación jurídica, finanzas públicas y contabilidad ambiental",
      "temporal": "Descriptivo (análisis histórico y de tendencias 1980-2010) y prospectivo (propuestas de políticas, marcos regulatorios y escenarios de transición para 2020 y 2030)"
    },
    "hallazgos_principales": [
      "La producción de agrocombustibles en los Estados Unidos y el Brasil genera graves dilemas socioecológicos, tales como la brecha metabólica por el uso intensivo de insumos petroquímicos y la deforestación indirecta (p.31, 35).",
      "En México, la Ley de Promoción y Desarrollo de los Bioenergéticos creó la Comisión Intersecretarial de Bioenergéticos, pero las políticas sufren de ambigüedad y falta de metas concretas, conviviendo con una reducción de reservas petroleras del 26% entre 2000 y 2010 (p.57, 58, 60).",
      "Cuba fue pionera a nivel mundial en la eliminación total de la iluminación ineficiente al sustituir 9.5 millones de bombillas incandescentes por lámparas fluorescentes y CFL, además de descentralizar su generación para resistir huracanes (p.279).",
      "El primer estudio de externalidades en Cuba aplicando el modelo SIMPACTS estimó los costos externos de centrales termoeléctricas mayores a 50 MW entre 0.56 y 1.22 centavos de dólar por kWh (p.359).",
      "La participación de fuentes renovables en la generación eléctrica de Centroamérica retrocedió notablemente al bajar del 75% en la década de 1980 al 50% en la actualidad debido al auge de plantas térmicas de hidrocarburos (p.415).",
      "En Honduras, la biomasa tradicional (leña) representa el 42.8% de la matriz energética nacional, superando la participación de hidrocarburos y concentrándose en el sector residencial rural ineficiente (p.431).",
      "Guatemala se posicionó como el referente centroamericano en contabilidad ambiental al estructurar e implementar sistemáticamente las Cuentas de Energía bajo el marco del SCAEI desde el año 2006 (p.493)."
    ],
    "conclusiones_recomendaciones": {
      "conclusiones": [
        "La descarbonización de la matriz energética regional es urgente para mitigar la alta vulnerabilidad climática de América Latina, requiriendo un cambio estructural que trascienda la petrodependencia e incorpore la valoración macroeconómica de externalidades ambientales en la planificación estatal.",
        "La eficiencia de las políticas de transición y diversificación energética depende críticamente de la coherencia institucional y la creación de marcos regulatorios específicos (como para biocombustibles o cogeneración) que eviten la ambigüedad y los incentivos cortoplacistas del mercado desregulado."
      ],
      "recomendaciones": [
        "Establecer un marco regulatorio específico y de largo plazo para incentivar la inyección a la red de la cogeneración de energía eléctrica a partir de biomasa o procesos industriales (como en la industria azucarera cubana) (p.135).",
        "Fortalecer el rol de los Bancos Centrales en el monitoreo de indicadores energéticos y ambientales para evaluar shocks de oferta externa y garantizar la estabilidad macroeconómica ante fluctuaciones de precios del petróleo (p.512-513).",
        "Adoptar e implementar sistemáticamente el Sistema de Contabilidad Ambiental y Económica Integrada (SCAEI) para estructurar Cuentas de Energía físicas y monetarias sector por sector, permitiendo orientar las políticas públicas hacia eficiencias reales (p.492).",
        "Promover la flexibilización de los derechos de propiedad intelectual y patentes en tecnologías limpias mediante licencias obligatorias para acelerar la transferencia tecnológica hacia países en desarrollo ante la crisis ambiental (p.311)."
      ],
      "nota": None
    },
    "resumen_narrativo": "Esta compilación de 534 páginas analiza los desafíos de América Latina en materia de energía, cambio climático y desarrollo sostenible mediante 22 estudios de caso y propuestas analíticas. Evalúa las políticas de biocombustibles en México y Brasil, contrastando las metas de diversificación con la soberanía alimentaria y la brecha metabólica rural. Detalla experiencias exitosas de transición energética, como la Revolución Energética cubana basada en eficiencia masiva e iluminación eficiente, y contrasta los mercados eléctricos privatizados de Centroamérica con el modelo integrado de Costa Rica. Propone incorporar la valoración de externalidades atmosféricas y el Sistema de Cuentas de Energía para guiar el diseño de políticas públicas integradas que fortalezcan la sostenibilidad ambiental regional."
  },
  "resumen_secciones": resumen_secciones_merged,
  "interpelacion": {
    "gran_impulso_ambiental_concreto": {
      "veredicto": "Parcial",
      "evidencia": "El documento es una compilación de 22 artículos técnicos que evalúan de manera sectorial la transición energética (como biocombustibles, eficiencia, generación fotovoltaica distribuida, cogeneración y externalidades macroeconómicas). No propone un único paquete unificado y coordinado de inversiones masivas a escala del modelo de desarrollo de la región (lo que descarta un 'Sí' bajo el Test 1 de la metodología del Big Push). Sin embargo, formula y detalla instrumentos y sectores específicos de descarbonización y transición tecnológica en el ámbito analizado.",
      "citas": [
        {
          "cita": "En este marco, la política pública con respecto a los agrocombustibles se debe enfocar en la optimización simultánea de: i) las ganancias de energía; y ii) la reducción de emisiones de gases de efecto invernadero, a la vez que iii) se preserve la diversidad biológica y iv) se asegure la autosuficiencia alimentaria.",
          "pagina": 31
        },
        {
          "cita": "La evaluación de las externalidades ambientales asociadas a la producción de combustibles fósiles ofrece en los estudios elaborados o auspiciados por la CEPAL, criterios para justificar los costos y beneficios sociales de las fuentes renovables de energía.",
          "pagina": 329
        }
      ],
      "nota": "Se asigna Parcial porque el documento es un compilador analítico que no diseña una hoja de ruta de inversiones unificadas, pero detalla profusamente los instrumentos sectoriales de transición."
    },
    "articulacion_actores": {
      "veredicto": "Sí",
      "evidencia": "El documento detalla de manera explícita y empírica varios mecanismos, plataformas e instancias de coordinación con nombre propio que se encuentran activos dentro del ámbito de estudio. En México, analiza la creación de la Comisión Intersecretarial de Bioenergéticos bajo el artículo 8 de la Ley de Promoción y Desarrollo de los Bioenergéticos para coordinar las políticas públicas intersectoriales (p.58). A nivel regional centroamericano, describe y analiza el Sistema de Interconexión Eléctrica para los Países de América Central (SIEPAC) como una plataforma multinacional activa de integración física y regulatoria del sector eléctrico (p.429).",
      "citas": [
        {
          "cita": "Para lograr este objetivo, en el artículo 8 de la Ley de Promoción y Desarrollo de los Bioenergéticos se estableció que debería crearse la Comisión Intersecretarial de Bioenergéticos como la institución responsable del diseño de la legislación y los programas públicos pertinentes",
          "pagina": 58
        },
        {
          "cita": "Otra posibilidad de abastecimiento energético es mediante el mercado eléctrico centroamericano, a través del Sistema de Interconexión Eléctrica de los Países de América Central (SIEPAC), en el cual los cinco países de Centroamérica se interconectan entre sí",
          "pagina": 429
        }
      ],
      "nota": None
    },
    "oportunidades_productivas_sostenibles": {
      "veredicto": "Sí",
      "evidencia": "El documento identifica y enumera múltiples oportunidades productivas y tecnológicas que ofrece la transición sostenible (como la generación de bioetanol rural, proyectos de cogeneración azucarera, desarrollo de redes fotovoltaicas residenciales distribuidas y el Sistema de Contabilidad SCAEI), y las vincula directamente con el empleo rural, la productividad sectorial y la reducción de desigualdades de gasto (p.55, 68, 131, 229, 492).",
      "citas": [
        {
          "cita": "os países de América Latina y el Caribe tienen el potencial para producir biocombustibles y condiciones favorables para el aprovechamiento de la agro-energía, lo que representa una oportunidad para diversificar su matriz energética.",
          "pagina": 55
        },
        {
          "cita": "En Cuba, los resultados validan la tendencia de reducción de la intensidad energética que se ha venido observando en los últimos años, coincidiendo con el desarrollo e implementación del programa de la Revolución Energética.",
          "pagina": 458
        }
      ],
      "nota": None
    },
    "como_hacerlo_concreto": {
      "veredicto": "Sí",
      "evidencia": "El documento, a través de las conclusiones y propuestas normativas de sus diversos artículos constitutivos, presenta recomendaciones sumamente precisas y ejecutables. Al someterlas al test de concreción, la gran mayoría de los ítems analizados (7 de 8) califican como CONCRETO al especificar entregables, figuras jurídicas, metas u organismos responsables con nombre propio (como la creación de un Ministerio de Energías Renovables, tarifas específicas de cogeneración, licencias obligatorias de patentes y metas de contabilidad SCAEI) en lugar de limitarse a exhortaciones genéricas.",
      "citas": [
        {
          "cita": "Habría ventajas de diversos tipos al tener un Ministerio de Estado que atienda las Energías Renovables en cada país de la región latinoamericana con esa misma visión.",
          "pagina": 177
        },
        {
          "cita": "La licencia obligatoria: es una posibilidad que se ha venido utilizando, mayormente, en el área de la salud pública, aunque no se conocen ejemplos recientes en lo que respecta a las medidas para combatir el cambio climático. Pero atendiendo a la magnitud que va cobrando este, deberá considerarse por parte de los operadores del Derecho el recurrir a esta institución.",
          "pagina": 311
        }
      ],
      "desglose_items": [
        {
          "item": "La política pública de biocombustibles debe enfocarse en la optimización simultánea de ganancias de energía y reducción de gases de efecto invernadero, preservando la diversidad biológica y la autosuficiencia alimentaria.",
          "clasificacion": "CONCRETO",
          "pagina": 31
        },
        {
          "item": "Establecer un marco de regulación jurídica específico para la cogeneración de energía en Cuba, definiendo tarifas, incentivos y derechos de inyección a la red.",
          "clasificacion": "CONCRETO",
          "pagina": 135
        },
        {
          "item": "Adoptar una visión de Estado a largo plazo para el desarrollo de energías renovables, mediante la creación de un Ministerio de Energías Renovables.",
          "clasificacion": "CONCRETO",
          "pagina": 177
        },
        {
          "item": "Articular políticas sinérgicas entre el desarrollo de fuentes renovables, la sostenibilidad ambiental y la adaptación al cambio climático mediante un manejo integral de cuencas.",
          "clasificacion": "CONCRETO",
          "pagina": 182
        },
        {
          "item": "Construir las bases del nuevo paradigma energético y del desarrollo sostenible desde las etapas de crisis actuales para facilitar su futura maduración.",
          "clasificacion": "GENERICO",
          "pagina": 273
        },
        {
          "item": "Establecer un regulador público independiente con verdadera autoridad en materia de política energética para orientar a las entidades estatales hacia metas concretas de reducción de GEI.",
          "clasificacion": "CONCRETO",
          "pagina": 303
        },
        {
          "item": "Emplear la figura jurídica de la licencia obligatoria para facilitar el acceso colectivo y la transferencia sin trabas de tecnologías limpias frente a la magnitud del cambio climático.",
          "clasificacion": "CONCRETO",
          "pagina": 311
        },
        {
          "item": "Diseñar mecanismos de cuotas obligatorias o participación garantizada para promover la diversificación e integración de nuevas fuentes renovables en sistemas propensos a oligopolios térmicos.",
          "clasificacion": "CONCRETO",
          "pagina": 404
        }
      ],
      "tally": "7 de 8 ítems pasan el test de concreción",
      "nota": None
    }
  },
  "tipologia": {
    "transformacion_primaria": {
      "numero": 6,
      "nombre": "Sostenibilidad ambiental",
      "certeza": "Alta"
    },
    "transformacion_secundaria": {
      "numero": 11,
      "nombre": "Capacidades del Estado",
      "certeza": "Alta"
    },
    "razonamiento_5_pasos": {
      "tension_dialectica": "El documento aborda la contradicción entre la creciente demanda de energía para impulsar el desarrollo socioeconómico en América Latina y la imperativa necesidad de mitigar y adaptarse al cambio climático mediante la descarbonización. Esta tensión se procesa proponiendo un cambio estructural en la matriz energética y regulatoria para sustituir la petrodependencia tradicional por fuentes limpias y eficientes.",
      "filtro_categoria_primaria": "Se clasifica como Sostenibilidad ambiental como objetivo primario porque el fin primordial del texto es guiar la transformación climática y la descarbonización del sector energético regional. Se descarta Capacidades del Estado como primaria ya que la arquitectura institucional y regulatoria propuestas actúan como medios o instrumentos facilitadores para lograr este fin ambiental fundamental.",
      "secundaria_obligatoria": "Se selecciona Capacidades del Estado como transformación secundaria obligatoria porque el documento demuestra consistentemente que cualquier transición energética y descarbonización sectorial requiere el fortalecimiento de la regulación pública (como la regulación de cogeneración en Cuba, la creación de ministerios dedicados en ALC, y la gestión de externalidades en la planificación estatal).",
      "justificacion_anti_copia": "La clasificación se fundamenta específicamente en el análisis comparativo del Sistema de Interconexión Eléctrica para los Países de América Central (SIEPAC), el modelo integrado de la Revolución Energética cubana (que sustituyó 9.5 millones de bombillas ineficientes), y la evaluación del marco regulatorio de la Ley de Promoción de Bioenergéticos en México con su Comisión Intersecretarial. Estos elementos empíricos demuestran cómo la política energética de descarbonización (#6) se viabiliza mediante la intervención e institucionalidad estatal (#11).",
      "validacion_anclas": "Al igual que el caso ancla Doc09 (Building a climate resilient power sector...), este documento sitúa la sostenibilidad de los sistemas energéticos y la transición a bajas emisiones como el núcleo central (#6), delegando la reforma de gobernanza y capacidades institucionales a la dimensión secundaria (#11). Se diferencia de Doc08 (Reflexiones sobre la gestión del agua...) y Doc12 (Acción climática en la agricultura...) donde la arquitectura de gobernanza y la evaluación institucional copaban el objeto analítico principal."
    },
    "tipo_documento_climatico": "Compilación de estudios técnicos",
    "nivel_aplicacion": "Regional (América Latina y el Caribe) / Nacional",
    "ambiguedad_pendiente_validacion": None
  }
}

# Write final consolidated JSON
with open('corpus/intermedios/11362/42140/borrador_preprueba.json', 'w', encoding='utf-8') as f:
    json.dump(final_json, f, indent=2, ensure_ascii=False)

print("borrador_preprueba.json has been written successfully!")
