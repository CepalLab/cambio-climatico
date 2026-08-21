import json
import os

data = {
  "documento_parcial": {
    "id": "45023",
    "bloque": "B05_CAP_III_P3_CONCL",
    "fuente": "tramos",
    "rango_pdf": "231-262"
  },
  "resumen_secciones": [
    {
      "seccion": "7. República Dominicana",
      "nivel": 3,
      "paginas": "231-247",
      "resumen": "Analiza en detalle la arquitectura institucional, legal, financiera y operativa de los seguros agropecuarios y la gestión integral del riesgo de desastres en la República Dominicana. El marco legal se fundamenta en la Ley de Seguros y Fianzas (Ley N° 146-02) y la Ley de Seguro Agropecuario (Ley N° 157-09), bajo la supervisión de la Superintendencia de Seguros. La operación del seguro público está a cargo de la Aseguradora Agropecuaria Dominicana S.A. (AGRODOSA, creada por Ley N° 479-08), empresa mixta con 90% de participación estatal y 10% privada. La Dirección General de Riesgos Agropecuarios (DIGERA), órgano colegiado adscrito al Ministerio de Agricultura, gestiona y canaliza un subsidio estatal del 50% al costo de las primas para pequeños y medianos productores, con un presupuesto anual ordinario de más de 165 millones de pesos dominicanos (3,6 millones de dólares) y transferencias acumuladas de 11 millones de dólares hasta 2017. En gestión financiera ante catástrofes, el país cuenta con una línea de crédito contingente con el BID por 100 millones de dólares y la opción de crédito contingente con opción de desembolso diferido (CAT-DDO) con el Banco Mundial. El mercado asegurador administrado por AGRODOSA ha mostrado una fuerte expansión, aumentando la superficie asegurada de 24.409 ha en 2008 a 79.028 ha en 2017 (con proyección de 91.000 ha en 2018) y el capital asegurado de 40,6 millones a 352,2 millones de dólares (estimado en 405 millones en 2018), cediendo el 75-85% del riesgo a reaseguradoras globales como Swiss Re, Munich Re, Partner Re y Hannover Rück. En el ámbito indizado, se analizan los estudios de factibilidad del Banco Mundial sobre índices de huracanes (HTI) y ENSO, destacando el riesgo de base; así como el proyecto piloto pecuario implementado por la Fundación REDDOM, USAID, IRI, Swiss Re, Banco ADOPEM y Mapfre BHD en el noroeste del país (FEDEGANO), el cual utiliza el índice de vegetación satelital NDVI (resolución 250x250 m en períodos decadales) para indemnizar automáticamente por sequía a 2.000 ganaderos lecheros. Finalmente, la red agrometeorológica es gestionada por la Oficina Nacional de Meteorología (ONAMET), que cuenta con 60 estaciones meteorológicas y emite el Boletín Hidrometeorológico diario y el reporte Agroclima mensual.",
      "dimensiones": [
        {
          "dimension": "propuestas_politica",
          "cita": "Las operaciones de seguros y reaseguros están reguladas por la Ley de Seguros y Fianzas en la República Dominicana (Ley N° 146-02, septiembre 2002) y la Ley de Seguro Agropecuario en la República Dominicana (Ley 157-09, abril 2009), que crea una plataforma para garantizar la inversión agropecuaria",
          "pagina": 231
        },
        {
          "dimension": "avances_implementacion",
          "cita": "En la actualidad la única compañía pública que comercializa seguros agropecuarios es la Aseguradora Agropecuaria Dominicana S.A. (AGRODOSA), creada en 2001 por la Ley 479-08, una legislación especial impulsada desde el sector público y el privado.",
          "pagina": 231
        },
        {
          "dimension": "propuestas_politica",
          "cita": "La DIGERA otorga un subsidio del 50% del costo de la póliza, con el objetivo de que los productores aseguren sus cosechas, infraestructuras o existencias de ganado, y así minimicen las pérdidas ante daños ocasionados por variaciones anormales de la naturaleza y por el cambio climático.",
          "pagina": 232
        },
        {
          "dimension": "avances_implementacion",
          "cita": "La República Dominicana cuenta con una línea de crédito contingente con el BID por un monto de 100 millones de dólares con un plazo original de cinco años para atender eventos extremos derivados de terremotos y huracanes.",
          "pagina": 233
        },
        {
          "dimension": "estado_de_situacion",
          "cita": "AGRODOSA ofrece seguros para todos los cultivos, en particular para los tecnificados, que se ubican en plantaciones de arroz, plátanos, bananos, habichuelas, frutales, vegetales en ambientes protegidos y en campo abierto.",
          "pagina": 234
        },
        {
          "dimension": "avances_implementacion",
          "cita": "AGRODOSA tiene contratos con reaseguradoras internacionales como la Swiss Reinsurance America Corporation (Suiza) y Hannover Rückrvershicherung A-G (Alemania) bajo la modalidad de cuota parte, mediante la que estas compañías son responsables del 75% de la suma asegurada.",
          "pagina": 235
        },
        {
          "dimension": "oportunidades",
          "cita": "En 2012 el gobierno dominicano solicitó al Banco Mundial la elaboración de un estudio de factibilidad de seguros agropecuarios basados en índices climáticos.",
          "pagina": 236
        },
        {
          "dimension": "avances_implementacion",
          "cita": "El satélite mide la reflectancia de la vegetación, se transforma en valores y se convierten en valores de salud de la vegetación en la zona. La resolución de los pixeles es de 250 x 250 metros. El índice se utiliza para estimar la cantidad, calidad y desarrollo de la vegetación con base en la medición de la actividad fotosintética expresada en el verdor de la vegetación.",
          "pagina": 241
        },
        {
          "dimension": "estado_de_situacion",
          "cita": "La ONAMET produce diariamente el Boletín Hidrometeorológico, que es un informe sobre las lluvias acumuladas en las últimas 24 horas, se divulga y consulta en línea. Utilizando herramientas de georreferenciación, la ONAMET presenta la precipitación registrada por las 60 estaciones meteorológicas disponibles",
          "pagina": 244
        }
      ],
      "subsecciones": []
    },
    {
      "seccion": "8. Belice",
      "nivel": 3,
      "paginas": "248-250",
      "resumen": "Examina el estado incipiente y los desafíos estructurales de los seguros agropecuarios y el financiamiento del riesgo climático en Belice. A pesar de contar con 9 aseguradoras privadas (4 no-vida, 3 vida y 2 compuestas) que emiten entre 60 y 65 millones de dólares anuales en primas brutas, no existe en el país ningún producto de seguro dirigido específicamente al sector agropecuario, limitándose la respuesta estatal al paradigma tradicional de asistencia posdesastre a través de NEMO. Entre 2000 y 2016, las pérdidas por tormentas y huracanes alcanzaron 737 millones de dólares, habiéndose erogado apenas 10 millones de dólares en fondos de emergencia. El gobierno ha diseñado instrumentos de planificación como el Marco Visión 2030, la Estrategia Nacional de Adaptación y el Plan Nacional de Inversión Resiliente al Clima (NCRIP, 2013), que identifica 430 millones de dólares en necesidades de inversión física con una brecha de 125 millones. Asimismo, se ejecutan proyectos de resiliencia con el Banco Mundial ($30M vial, $11,8M energético) y el FIDA/GCF ($20M en Resilient Rural Belize). A nivel soberano, Belice fue miembro del fondo paramétrico regional CCRIF SPC desde 2007, habiendo recibido 261.073 dólares tras el huracán Earl en 2016 con primas anuales de 650.000 dólares, aunque optó por no renovar su póliza en 2017-2018. En infraestructura agrometeorológica, el Servicio Meteorológico Nacional dispone de 21 estaciones manuales y 23 automáticas, complementadas por redes privadas en las industrias bananera y azucarera, persistiendo dificultades de cobertura en zonas rurales remotas y una marcada falta de cultura y capacidad de pago en los pequeños agricultores.",
      "dimensiones": [
        {
          "dimension": "brechas_implementacion",
          "cita": "A pesar de que Belice cuenta con una industria de seguros establecida que cubre los rubros de vida y no vida, no se han identificado aún seguros dirigidos específicamente al sector agropecuario",
          "pagina": 248
        },
        {
          "dimension": "propuestas_politica",
          "cita": "El Gobierno de Belice ha desarrollado el Plan Nacional de Inversión Resiliente al Clima (NCRIP, por sus siglas en inglés) para abordar los impactos del cambio climático en el desarrollo social y económico.",
          "pagina": 248
        },
        {
          "dimension": "diagnostico_estructural",
          "cita": "El monto de las pérdidas derivadas de las tormentas que han impactado negativamente a Belice entre 2000 y 2016 se estiman en 737 millones de dólares, habiendo sido erogados 10 millones de dólares en la atención de dichas emergencias.",
          "pagina": 249
        },
        {
          "dimension": "estado_de_situacion",
          "cita": "Belice ha sido miembro de la OECS Commission and the Caribbean Catastrophe Risk Insurance Facility (CCRIF SPC) desde 2007, con pólizas para huracanes, exceso de lluvia y eventos de terremotos, pero optó por no renovar sus pólizas en el período de cobertura 2017-2018.",
          "pagina": 249
        },
        {
          "dimension": "avances_implementacion",
          "cita": "CCRIF SPC realizó un pago de 261,073 dólares (BZ $322.146) al Gobierno de Belice como resultado de las fuertes lluvias del huracán Earl del 4 al 5 de agosto de 2016.",
          "pagina": 250
        },
        {
          "dimension": "desafios",
          "cita": "Actualmente hay 21 estaciones meteorológicas manuales y 23 automáticas. No obstante, las estaciones generalmente no se ubican cerca de comunidades agrícolas remotas, lo que crea un desafío para obtener los datos requeridos y proporcionar el pronóstico correspondiente.",
          "pagina": 250
        }
      ],
      "subsecciones": []
    },
    {
      "seccion": "C. Marco estratégico regional",
      "nivel": 2,
      "paginas": "250-254",
      "resumen": "Sistematiza el conjunto de políticas, acuerdos intergubernamentales, fondos e iniciativas regionales impulsados en el marco del SICA para promover la gestión integral del riesgo de desastres, la adaptación climática y el aseguramiento agropecuario en Centroamérica y la República Dominicana. Articula las resoluciones del Consejo Agropecuario Centroamericano (CAC) y la Estrategia EASAC 2018-2030 con los marcos de protección civil (PCGIR, FOCEGIR y CEPREDENAC), medio ambiente (CCAD, PARCA y ERCC), finanzas públicas (COSEFIN y supervisión basada en riesgos de CCSBSO) y seguridad alimentaria (SAN, SIRSAN/PRESISAN), así como las plataformas regionales de monitoreo hidrometeorológico y alerta temprana gestionadas por el CRRH y SATCA.",
      "dimensiones": [],
      "subsecciones": [
        {
          "seccion": "1. Marco de política, gestión integral de riesgos e institucionalidad",
          "nivel": 3,
          "paginas": "250-253",
          "resumen": "Detalla los acuerdos y marcos regulatorios estratégicos regionales aprobados por las cumbres de Jefes de Estado y los consejos de ministros del SICA. Desde principios de los 2000, la Política Agrícola Centroamericana (PACA) y las resoluciones de la Junta Interamericana de Agricultura (JIA/IICA) promovieron los seguros como herramienta para blindar la inversión rural. El CAC aprobó en 2017 la Estrategia EASAC 2018-2030 (Eje 2, Línea Estratégica 7), que prioriza el desarrollo de instrumentos innovadores de transferencia y retención de riesgos para la agricultura sostenible. En materia de protección civil, la Política Centroamericana de Gestión Integral de Riesgo de Desastres (PCGIR, 2010) y el Fondo Centroamericano (FOCEGIR, 2011) articulan el financiamiento preventivo regional coordinado por CEPREDENAC. Asimismo, el COSEFIN evalúa opciones de seguros soberanos regionales ante desastres con el BID, BM y BCIE; el CCSBSO impulsa la supervisión basada en riesgos; y la CCAD, el CAC y el COMISCA integran la gestión agroambiental y de salud mediante la ERAS, la ECADERT y la Estrategia Regional de Cambio Climático (ERCC).",
          "dimensiones": [
            {
              "dimension": "avances_implementacion",
              "cita": "El Consejo Agropecuario Centroamericano (CAC), foro regional de los ministros de agricultura, incluyó el tema de los seguros agropecuarios en sus resoluciones desde principios de la década de 2000.",
              "pagina": 250
            },
            {
              "dimension": "propuestas_politica",
              "cita": "El CAC aprobó en 2017 la Estrategia de agricultura sostenible adaptada al clima para la región del SICA (EASAC 2018-2030) cuyo eje 2 propone la Gestión integral de riesgos y adaptación al clima.",
              "pagina": 251
            },
            {
              "dimension": "avances_implementacion",
              "cita": "En la XXXV Reunión Ordinaria de Jefes de Estado y de Gobierno de los países del SICA, de junio de 2010, se aprueba la Política Centroamericana de Gestión Integral de Riesgo de Desastres (PCGIR)",
              "pagina": 251
            },
            {
              "dimension": "propuestas_politica",
              "cita": "Posteriormente fue creado el Fondo Centroamericano de la Gestión de Riesgo de Desastres (FOCEGIR), aprobado en la XXXVIII Reunión Ordinaria de Jefes de Estado y de Gobierno de los Países del Sistema de la Integración Centroamericana (SICA), en diciembre de 2011.",
              "pagina": 251
            },
            {
              "dimension": "oportunidades",
              "cita": "En la XXXI Reunión de febrero de 2013, el COSEFIN analizó la posibilidad de estructurar una operación de Seguro Regional ante Desastres con la participación de especialistas del BID, Banco Mundial y Banco Centroamericano de Integración Económica (BCIE)",
              "pagina": 252
            }
          ],
          "subsecciones": []
        },
        {
          "seccion": "2. Condiciones de oferta y demanda e inclusión financiera",
          "nivel": 3,
          "paginas": "253-254",
          "resumen": "Analiza las iniciativas multilaterales y redes técnicas para dinamizar el mercado de seguros y robustecer la información hidrometeorológica regional. Destaca el programa BID/FOMIN ejecutado con ministerios de agricultura, BM, BCIE, FIDES y ASSAL para fortalecer la oferta y supervisión de coberturas agropecuarias. El BCIE destaca por su acreditación ante el Fondo Verde del Clima (GCF) para financiar proyectos de adaptación y mitigación. En sistemas de información, el Comité Regional de Recursos Hídricos (CRRH) emite evaluaciones de riesgo agroclimático y alertas tempranas tres veces al año, mientras que el proyecto SATCA (PMA, MARN, COPECO, SMN y CEPREDENAC) consolida una red de alerta temprana multiamenaza. Finalmente, el CAC, FAO y CEPAL avanzan en el diseño de módulos estandarizados de información y estadísticas agropecuarias.",
          "dimensiones": [
            {
              "dimension": "avances_implementacion",
              "cita": "El Banco Interamericano de Desarrollo (BID/Fondo Multilateral de Inversiones (FOMIN) apoyó un proyecto de desarrollo del mercado de seguros agropecuarios en Centroamérica, en colaboración con los ministerios de agricultura, el Banco Mundial y el BCIE, con apoyo del Programa Canadiense de Asistencia Técnica y la Federación Interamericana de Empresas de Seguros (FIDES)",
              "pagina": 253
            },
            {
              "dimension": "estado_de_situacion",
              "cita": "El Comité Regional de Recursos Hídricos (CRRH), organismo técnico del SICA, tiene entre sus objetivos fomentar acciones en los campos de recursos atmosféricos, hídricos y de manejo de cuencas orientados a la protección del medio ambiente y a la prevención y mitigación de desastres naturales.",
              "pagina": 253
            },
            {
              "dimension": "avances_implementacion",
              "cita": "El Sistema de Alerta Temprana para Centroamérica (SATCA) es un proyecto de gestión de riesgo y alerta temprana impulsado por el Programa Mundial de Alimentos (PMA) de Naciones Unidas en colaboración con el Ministerio de Medio Ambiente y Recursos Naturales de El Salvador",
              "pagina": 253
            }
          ],
          "subsecciones": []
        }
      ]
    },
    {
      "seccion": "D. Avance regional de las condiciones de GIR y seguros",
      "nivel": 2,
      "paginas": "254-258",
      "resumen": "Presenta una evaluación sintética y comparativa del cumplimiento de las 23 condiciones institucionales, normativas, de mercado y de información para la gestión integral de riesgos y los seguros agropecuarios en los países del SICA. El componente con mayor avance relativo es el Marco Legal, Reglamentario y de Supervisión, con un cumplimiento promedio superior al 80%, donde al menos cuatro países cuentan con regulaciones completas y supervisión habilitante para seguros paramétricos. Le sigue el componente de Condiciones de Oferta, Demanda e Inclusión Financiera, con más del 60% de cumplimiento, impulsado por alianzas público-privadas como las de MiCRO (Swiss Re) con el BFA en El Salvador y Aseguradora Rural en Guatemala, además de proyectos piloto de CEPAL, FAO, CIAT, IRI y El Zamorano. Por el contrario, los mayores rezagos y brechas se concentran en Gestión Integral de Riesgos e Institucionalidad y en Sistemas de Información Agroclimática. Persiste una escasa articulación entre los programas ministeriales y la gestión prospectiva del riesgo, ausencia de comités interinstitucionales de seguros, falta de clasificadores presupuestarios para el gasto preventivo y altos costos de encuestas y censos agropecuarios, lo que hace imperativo adoptar tecnologías satelitales calibradas in situ y esquemas integrales de inclusión financiera rural.",
      "dimensiones": [
        {
          "dimension": "avances_implementacion",
          "cita": "El componente que más avances ha registrado es el del Marco legal, regulatorio y de supervisión. Al menos cuatro países han logrado completar los requerimientos legales para que los seguros agropecuarios estén debidamente regulados y supervisados",
          "pagina": 254
        },
        {
          "dimension": "desafios",
          "cita": "Uno de los componentes que requerirá mayor atención y programación de acciones es el de la Gestión integral de riesgos e institucionalidad. La CEPAL ha insistido, a través de las reuniones de expertos de la comunidad de práctica con los países SICA, en la necesidad de minimizar la fragilidad económica, social y ambiental en la que se desenvuelven los pequeños productores agropecuarios",
          "pagina": 254
        },
        {
          "dimension": "brechas_implementacion",
          "cita": "En general, se percibe que los países de la región aún no cuentan con una estrategia gubernamental para el desarrollo o fortalecimiento de los seguros agropecuarios desde una perspectiva de gestión integral de riesgos, incluyendo alianzas público-privadas.",
          "pagina": 255
        },
        {
          "dimension": "tendencias",
          "cita": "En cuanto a las condiciones de oferta, demanda e inclusión financiera a favor de los seguros agropecuarios, es con seguridad el componente evaluado que ha reportado los mayores avances en la región SICA en el último quinquenio.",
          "pagina": 255
        },
        {
          "dimension": "avances_implementacion",
          "cita": "Al respecto, la MiCRO filial de Swiss Re ha establecido alianzas estratégicas con el BFA de El Salvador y Aseguradora Rural de Guatemala para lanzar seguros paramétricos que tengan por objetivo proteger a los clientes de dichas instituciones a proteger el capital invertido cuando este se ha obtenido mediante la adquisición de créditos.",
          "pagina": 256
        },
        {
          "dimension": "desafios",
          "cita": "En materia de sistemas de información agropecuaria, de desarrollo rural, cambio climático y gestión de riesgos los países del SICA requieren de la inversión de recursos humanos, tecnológicos y financieros a fin de garantizar que se cuente tanto con sistemas de información de producción, rendimiento y de gestión de riesgos en el sector agropecuario",
          "pagina": 256
        },
        {
          "dimension": "diagnostico_estructural",
          "cita": "el componente de legalidad, normatividad e institucional tendría un cumplimiento arriba del 80%, seguido de las condiciones de oferta, demanda e inclusión financiera por arriba del 60%. En los rangos más bajos de cumplimiento se encontrarían los componentes de datos sobre rendimientos y sistemas de información agroclimáticos, así como el de gestión integral de riesgos e institucionalidad.",
          "pagina": 257
        }
      ],
      "subsecciones": []
    },
    {
      "seccion": "Conclusiones",
      "nivel": 1,
      "paginas": "259-262",
      "resumen": "Sintetiza las conclusiones y recomendaciones estratégicas para consolidar mercados de seguros agropecuarios resilientes en Centroamérica y la República Dominicana dentro del marco de la gestión integral del riesgo de desastres y la adaptación al cambio climático. Subraya que la reducción de las vulnerabilidades socioeconómicas y ambientales en el medio rural es una precondición insoslayable para la viabilidad del aseguramiento, requiriendo la articulación de la banca de desarrollo, microfinancieras, cooperativas y asociaciones de productores como agregadores y retenedores en fuente. Recomienda la creación o fortalecimiento de aseguradoras públicas que lideren la oferta junto con marcos regulatorios modernos que autoricen a aseguradoras y reaseguradoras privadas operar esquemas paramétricos con plena certeza jurídica. Destaca el papel indelegable del Estado en el subsidio directo a las primas de pequeños productores, en la diferenciación de apoyos para evitar el desincentivo a la cobertura privada, en la inversión en bienes públicos de información agroclimática de alta resolución espacial y temporal, y en la utilización de reaseguro soberano de última instancia. Finalmente, compara el Índice Estandarizado de Precipitación (SPI) con el Índice de Estrés Agrícola (ASIS) de la FAO y promueve el aprovechamiento de datos satelitales y tecnologías móviles para mitigar el riesgo de base y abaratar costos operativos en beneficio de la agricultura familiar.",
      "dimensiones": [
        {
          "dimension": "diagnostico_estructural",
          "cita": "La reducción de las vulnerabilidades y por tanto de la probabilidad de riesgo de desastres en la actividad agropecuaria, son un factor clave para el diseño, implementación y éxito de los instrumentos de transferencias de riesgos como los seguros agropecuarios.",
          "pagina": 259
        },
        {
          "dimension": "propuestas_politica",
          "cita": "El sector público participa a través del diseño e implementación de políticas de inclusión financiera, tomando en cuenta instrumentos financieros como depósitos, créditos, garantías, fianzas, almacenamiento y seguros agropecuarios, así como la regulación y supervisión del sistema financiero en general, y de la actividad aseguradora en particular.",
          "pagina": 259
        },
        {
          "dimension": "propuestas_politica",
          "cita": "Sería deseable que en cada país de la región SICA hubiese una institución pública responsable del diseño, desarrollo, diseminación y comercialización de los seguros agropecuarios tradicionales o paramétricos.",
          "pagina": 260
        },
        {
          "dimension": "propuestas_politica",
          "cita": "Se requiere, además, apoyo gubernamental para otorgar subsidios a las primas de los seguros dirigidos a los micros y pequeños productores agropecuarios.",
          "pagina": 260
        },
        {
          "dimension": "oportunidades",
          "cita": "Los seguros agropecuarios indizados tienen la virtud de eliminar la selección adversa y el riesgo moral, aunque deben batallar con el riesgo de base.",
          "pagina": 260
        },
        {
          "dimension": "diagnostico_estructural",
          "cita": "El índice de precipitación estandarizado es ampliamente utilizado en el diseño de los seguros paramétricos. El índice resulta muy intuitivo y fácil de explicar a los productores. No obstante, tiene la desventaja de no incluir un indicador de temperatura, con lo que no es posible contar con una medida que refleje las condiciones probables de evapotranspiración y su incidencia en el crecimiento de los cultivos.",
          "pagina": 261
        },
        {
          "dimension": "oportunidades",
          "cita": "Los elevados costos de los censos y las encuestas, hará más necesaria la formación y adopción de tecnologías de uso de datos de fuentes satelitales con su debida validación en los ámbitos nacionales y locales, así como el uso de aplicaciones para celulares para el intercambio de información con los pequeños productores agropecuarios.",
          "pagina": 262
        }
      ],
      "subsecciones": []
    }
  ],
  "hallazgos_candidatos": [
    "En la República Dominicana, el mercado de seguros agropecuarios administrado por AGRODOSA experimentó un fuerte crecimiento entre 2008 y 2017, elevando la superficie asegurada de 24.409 a 79.028 hectáreas y el capital asegurado de 40,6 a 352,2 millones de dólares, respaldado por un subsidio estatal a las primas del 50% administrado por la DIGERA (pp. 232, 235).",
    "El proyecto piloto pecuario de la Fundación REDDOM, USAID, IRI y Swiss Re en el noroeste dominicano diseñó un seguro paramétrico basado en el índice de vegetación NDVI con píxeles de 250x250 metros en ciclos decadales, asegurando a más de 2.000 ganaderos lecheros de FEDEGANO frente a la sequía (pp. 240-241).",
    "En Belice no existe oferta de seguros agropecuarios comerciales, limitándose la gestión estatal al auxilio de emergencia posdesastre a través de NEMO, habiéndose registrado 737 millones de dólares en pérdidas por tormentas entre 2000 y 2016 frente a 10 millones de dólares erogados en atención directa (pp. 248-249).",
    "Belice integró el fondo de seguro catastrófico regional CCRIF SPC entre 2007 y 2017, recibiendo un pago paramétrico de 261.073 dólares tras el huracán Earl en 2016, aunque no renovó su póliza en el período 2017-2018 (pp. 249-250).",
    "La evaluación regional del SICA muestra que el Marco Legal y Regulatorio presenta el mayor nivel de cumplimiento (>80%), mientras que los Sistemas de Información Agroclimática y la Gestión Integral de Riesgos exhiben los mayores rezagos (<50%) por falta de clasificadores presupuestarios y desarticulación interinstitucional (pp. 254-257).",
    "Las alianzas estratégicas entre MiCRO (Swiss Re) y entidades financieras locales en El Salvador (BFA) y Guatemala (Aseguradora Rural) demostraron la viabilidad de empaquetar microseguros climáticos indizados contra sequía y exceso de lluvia vinculados a créditos productivos rurales (p. 256).",
    "El Índice de Estrés Agrícola (ASIS) de la FAO ofrece ventajas operativas sobre el SPI al integrar temperatura, humedad y sensores NDVI a escala decadal de 1 km², minimizando el riesgo de base en cultivos de maíz y arroz según los ensayos asistidos por CEPAL en el arco seco panameño (pp. 261-262)."
  ],
  "recomendaciones_normativas": [
    "Institucionalizar en los países del SICA comités interinstitucionales permanentes de seguros agropecuarios y gestión integral de riesgos, coordinando a ministerios de agricultura, hacienda, protección civil e intendencias de seguros (pp. 255, 260).",
    "Establecer en los presupuestos nacionales clasificadores y etiquetadores de gasto público dedicados específicamente a la prevención de riesgos climáticos y adaptación del sector agropecuario (pp. 255, 262).",
    "Crear o facultar compañías de seguros públicas o fondos fiduciarios especializados con subsidio estatal directo a las primas (entre 25% y 50%) para pequeños agricultores y ganaderos de subsistencia (pp. 232, 260).",
    "Habilitar marcos regulatorios prudenciales modernos y supervisión basada en riesgos que reconozcan expresamente los contratos de seguros paramétricos e indizados y autoricen su intermediación por cooperativas y microfinancieras (pp. 254, 260).",
    "Adoptar sistemas públicos y abiertos de información agrometeorológica satelital de alta resolución (como ASIS y NDVI) validados con redes locales de estaciones para reducir los costos de tarificación actuarial y cálculo de índices (pp. 256, 261-262)."
  ]
}

target_path = "corpus/intermedios/11362/45023/parcial_B05_CAP_III_P3_CONCL.json"
with open(target_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Generated {target_path} successfully!")
