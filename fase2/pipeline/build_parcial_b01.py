import json
import os
import re

tramos_dir = "corpus/intermedios/11362/45023/tramos"

pages_text = {}
for fname in sorted(os.listdir(tramos_dir)):
    if fname.endswith(".txt") and fname.startswith("tramo_"):
        fpath = os.path.join(tramos_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        parts = re.split(r"=== PÁGINA PDF (\d+) ===", content)
        for i in range(1, len(parts), 2):
            pnum = int(parts[i])
            ptext = parts[i+1]
            pages_text[pnum] = ptext

def check_quote(quote, pnum):
    if pnum not in pages_text:
        return False, f"Page {pnum} missing"
    norm_quote = " ".join(quote.split())
    norm_text = " ".join(pages_text[pnum].split())
    if norm_quote in norm_text:
        return True, "OK"
    return False, f"Quote not found in page {pnum}: '{norm_quote[:40]}...'"

# Define the structure of B01
parcial_b01 = {
    "documento_parcial": {
        "id": "45023",
        "bloque": "B01_INTRO_CAP_I",
        "fuente": "tramos",
        "rango_pdf": "39-68"
    },
    "resumen_secciones": [
        {
            "seccion": "Introducción",
            "nivel": 1,
            "paginas": "39-41",
            "resumen": "Presenta la iniciativa conjunta de la CEPAL y la SE-CAC para promover instrumentos de aseguramiento agropecuario y paramétrico en Centroamérica y República Dominicana bajo un enfoque de gestión integral de riesgos. Plantea el desafío crítico del riesgo de base derivado de fallas en el diseño o modelación con índices como el SPI. Concluye que los seguros no deben operar aisladamente, sino integrados en paquetes de bienes y servicios públicos que reduzcan la vulnerabilidad estructural e incrementen la resiliencia rural.",
            "dimensiones": [
                {
                    "dimension": "gestion_de_riesgos",
                    "cita": "iniciativa para el desarrollo y fortalecimiento de los seguros agropecuarios, incluyendo los basados en índices climáticos2, desde una perspectiva de gestión integral de riesgos y servicios integrales dirigidos a pequeños productores agropecuarios.",
                    "pagina": 39
                },
                {
                    "dimension": "desafios",
                    "cita": "discrepancia entre los daños en las cosechas en los productores y los pagos registrados por las compañías aseguradoras se conoce como riesgo de base y uno de los objetivos de un programa de aseguramiento agropecuario debería ser minimizarlo.",
                    "pagina": 39
                },
                {
                    "dimension": "politicas_publicas",
                    "cita": "a medida que se reducen las vulnerabilidades y se incrementa la resiliencia, se reduce la probabilidad del riesgo de un desastre ante la presencia de una amenaza, lo que reduce las primas y aumenta el mercado para los seguros agropecuarios.",
                    "pagina": 40
                }
            ],
            "subsecciones": []
        },
        {
            "seccion": "I. Marco conceptual y de referencia",
            "nivel": 1,
            "paginas": "43-68",
            "resumen": "Desarrolla el marco conceptual que fundamenta el aseguramiento agropecuario en la región SICA a partir de la gestión integral de riesgos, diferenciando amenazas hidrometeorológicas de vulnerabilidades socioeconómicas. Examina las tipologías de riesgos e instrumentos de transferencia financiera, las precondiciones institucionales y normativas, los sistemas de información agroclimática y los programas de fortalecimiento de capacidades para consolidar la resiliencia de la agricultura familiar campesina.",
            "dimensiones": [
                {
                    "dimension": "marcos_conceptuales",
                    "cita": "La visión de la CEPAL sobre los instrumentos de aseguramiento agropecuario para los países de la región SICA se concibe desde una perspectiva de gestión integral de riesgos y de servicios integrales a los pequeños productores.",
                    "pagina": 43
                },
                {
                    "dimension": "bienes_publicos",
                    "cita": "En países de economías en desarrollo se demandará la participación activa del Estado a través de una gama importante de instituciones públicas para el desarrollo de bienes públicos como la modernización de la normatividad e institucionalidad para el correcto funcionamiento del mercado de seguros",
                    "pagina": 43
                }
            ],
            "subsecciones": [
                {
                    "seccion": "A. Gestión integral de riesgos",
                    "nivel": 2,
                    "paginas": "43-52",
                    "resumen": "Define la gestión integral de riesgos como un proceso social continuo que combina los enfoques prospectivo, correctivo y reactivo para aminorar la probabilidad de desastres resultantes de la interacción entre amenazas naturales y vulnerabilidades estructurales. Establece que los seguros constituyen el último eslabón de la cadena de gestión, debiendo subordinarse a acciones preventivas que reduzcan la fragilidad económica y ambiental campesina.",
                    "dimensiones": [
                        {
                            "dimension": "marcos_conceptuales",
                            "cita": "Von Hess y de la Torre (2009) definen la gestión integral de riesgos como “un proceso social cuyo fin último es la reducción y atención, o la previsión y control permanente del riesgo de desastre en la sociedad, en consonancia con e integrada al logro de pautas de desarrollo humano, económico, ambiental y territorial, sostenibles”",
                            "pagina": 43
                        },
                        {
                            "dimension": "gestion_de_riesgos",
                            "cita": "La gestión del riesgo no se limita a reaccionar ante eventos adversos, sino que se anticipa a su ocurrencia y a efectos potenciales mediante estrategias y medidas de política que aminoren las consecuencias adversas.",
                            "pagina": 51
                        }
                    ],
                    "subsecciones": [
                        {
                            "seccion": "1. Amenazas",
                            "nivel": 3,
                            "paginas": "44-46",
                            "resumen": "Clasifica las amenazas en naturales, socionaturales y antropogénicas, destacando que en Centroamérica y República Dominicana las amenazas hidrometeorológicas (tormentas e inundaciones) representan el 49% de los eventos extremos y el 77% de los desastres que impactan directamente al sector agropecuario. Advierte un incremento notable en la frecuencia decenal de eventos severos que comprometen la estabilidad productiva.",
                            "dimensiones": [
                                {
                                    "dimension": "impactos_climaticos",
                                    "cita": "mayor parte de los eventos extremos de origen natural registrados en Centroamérica y la República Dominicana tienen orígenes hidrometeorológicos, como inundaciones y tormentas (49% del total), seguido por terremotos",
                                    "pagina": 45
                                },
                                {
                                    "dimension": "sector_agropecuario",
                                    "cita": "De los 653 eventos extremos registrados en los últimos 117 años en Centroamérica y la República Dominicana según el EM-DAT, 421 han afectado al sector agropecuario de manera directa. De estos 421 eventos, el 77% corresponde a tormentas e inundaciones",
                                    "pagina": 45
                                }
                            ],
                            "subsecciones": []
                        },
                        {
                            "seccion": "2. Vulnerabilidad",
                            "nivel": 3,
                            "paginas": "47-48",
                            "resumen": "Analiza la vulnerabilidad a partir del grado de exposición territorial, fragilidad socioeconómica y capacidad de resiliencia de las unidades campesinas. Documenta daños acumulados por 23.765 millones de dólares en la región entre 1900 y 2011, concentrándose el 66% de las pérdidas productivas en la agricultura, donde la falta de activos y la ubicación en zonas degradadas intensifican la precariedad ante sequías y crecidas.",
                            "dimensiones": [
                                {
                                    "dimension": "vulnerabilidad_socioeconomica",
                                    "cita": "La vulnerabilidad se expresa en el grado de exposición al daño de las unidades sociales (persona, familia, comunidad o sociedad) y de los activos fijos y actividades económicas (CEPAL y SE-CAC, 2015).",
                                    "pagina": 47
                                },
                                {
                                    "dimension": "impactos_economicos",
                                    "cita": "con base en las evaluaciones económicas realizadas por los gobiernos de Centroamérica y la República Dominicana, la CEPAL y otras agencias de las Naciones Unidas sobre los mayores desastres se estima que, del total de las pérdidas económicas en sectores productivos, el 66% ha recaído en el sector agropecuario.",
                                    "pagina": 48
                                }
                            ],
                            "subsecciones": []
                        },
                        {
                            "seccion": "3. Riesgos climáticos",
                            "nivel": 3,
                            "paginas": "48-50",
                            "resumen": "Examina la incertidumbre climática que condiciona la agricultura de secano y la alta sensibilidad a ciclos de El Niño y La Niña. Advierte que las proyecciones de cambio climático indican aumentos del 5% al 10% en la intensidad de huracanes, mayor aridez en el Corredor Seco y pérdidas económicas acumuladas al 2100 de hasta el 54% del PIB regional en escenarios severos, amenazando la producción de maíz y frijol.",
                            "dimensiones": [
                                {
                                    "dimension": "seguridad_alimentaria",
                                    "cita": "Los déficits de lluvias inciden directamente sobre las actividades agrícolas en virtud de que las cosechas, en su mayor parte, son producidas bajo el régimen de secano.",
                                    "pagina": 49
                                },
                                {
                                    "dimension": "proyecciones_climaticas",
                                    "cita": "estimación de la pérdida acumulada para Centroamérica al año 2100 oscilaría entre el 7% y el 15% del PIB de 2008. Si a esta estimación se añaden los costos acumulados al año 2100 en el sector agrícola, los recursos hídricos y la biodiversidad, la pérdida podría ser equivalente al 32% del PIB regional de 2008 en el escenario menos pesimista (B2), y al 54% del PIB regional de 2008 en el escenario más pesimista (A2)",
                                    "pagina": 50
                                }
                            ],
                            "subsecciones": []
                        },
                        {
                            "seccion": "4. Gestión integral de riesgos",
                            "nivel": 3,
                            "paginas": "50-52",
                            "resumen": "Desarrolla la articulación entre la gestión prospectiva (prevención ex ante), correctiva (mitigación de vulnerabilidades) y reactiva (atención ex post). Destaca que medidas como la diversificación de cultivos, semillas resistentes a sequía, infraestructura de riego blindada y acceso a servicios financieros evitan que los choques climáticos degeneren en trampas de pobreza y pérdida permanente de activos campesinos.",
                            "dimensiones": [
                                {
                                    "dimension": "gestion_de_riesgos",
                                    "cita": "La gestión correctiva es el proceso en el que se toman medidas orientadas a disminuir la vulnerabilidad existente. A estas se agrega la gestión reactiva que es la orientada a minimizar el efecto negativo de una amenaza cuando ha concretado su daño en una población",
                                    "pagina": 51
                                },
                                {
                                    "dimension": "respuestas_adaptacion",
                                    "cita": "diversificar cultivos con diferentes sensibilidades climáticas y utilizar variedades de semillas con menores requerimientos de humedad son estrategias asequibles a los productores y constituyen ejemplos de adaptación al cambio climático.",
                                    "pagina": 51
                                }
                            ],
                            "subsecciones": []
                        }
                    ]
                },
                {
                    "seccion": "B. Bienes y servicios públicos, fragilidad y resiliencia",
                    "nivel": 2,
                    "paginas": "52-54",
                    "resumen": "Fundamenta que los seguros agropecuarios y sus componentes de soporte deben gestionarse como bienes públicos mediante inversión estatal y alianzas público-privadas. Explica que la provisión de infraestructura resiliente, sistemas agrometeorológicos y educación financiera campesina disminuye la fragilidad estructural y genera economías de escala que reducen el valor de las primas comerciales.",
                    "dimensiones": [
                        {
                            "dimension": "bienes_publicos",
                            "cita": "Los seguros agropecuarios pueden ser considerados bienes públicos en los ámbitos subnacional, nacional, regional y global.",
                            "pagina": 52
                        },
                        {
                            "dimension": "politicas_publicas",
                            "cita": "fondos públicos asignados a la inversión pública rural en un marco integral de gestión de riesgos dirigido a la agricultura promueven el desarrollo de infraestructura de transporte, riego, educación y salud para los productores, sus familias y comunidades",
                            "pagina": 53
                        }
                    ],
                    "subsecciones": [
                        {
                            "seccion": "1. Bienes públicos",
                            "nivel": 3,
                            "paginas": "52",
                            "resumen": "Explica que la estructuración de un mercado de aseguramiento indizado requiere precondiciones institucionales, normativas y financieras que las comunidades rurales no pueden costear por sí solas. La inversión pública en marcos regulatorios y catálogos de datos climáticos actúa como un bien público global indispensable para viabilizar la participación del sector asegurador y reasegurador.",
                            "dimensiones": [
                                {
                                    "dimension": "bienes_publicos",
                                    "cita": "sistema de seguro agropecuario indizado requiere un cierto nivel de bienes públicos para lograrse. Si los bienes públicos necesarios no existen o si están en malas condiciones, es probable que las mejoras cuesten tanto que no sería factible que los productores o comunidades individuales puedan financiarlas.",
                                    "pagina": 52
                                },
                                {
                                    "dimension": "marcos_regulatorios",
                                    "cita": "Estas precondiciones se relacionan con el marco normativo y regulatorio, la institucionalidad para la gestión de riesgos, las estructuras financieras para el otorgamiento de subsidios, la modernización de las estructuras de funcionamiento para la atracción de compañías de seguros y reaseguros, y el montaje de sistemas de información de variables climáticas",
                                    "pagina": 52
                                }
                            ],
                            "subsecciones": []
                        },
                        {
                            "seccion": "2. Reduciendo la fragilidad y aumentando la resiliencia",
                            "nivel": 3,
                            "paginas": "53-54",
                            "resumen": "Propone priorizar la inversión pública en investigación y desarrollo de semillas resistentes, infraestructura de riego en zonas áridas y estaciones meteorológicas locales frente a la mera asignación de transferencias de emergencia. Sugiere aprovechar el aprendizaje campesino a campesino y la inclusión financiera formal para fortalecer la capacidad adaptativa comunitaria frente al cambio climático.",
                            "dimensiones": [
                                {
                                    "dimension": "resiliencia_productiva",
                                    "cita": "fomentar la resiliencia económica a través de servicios financieros como créditos, depósitos, garantías y seguros a disposición de los pequeños productores agropecuarios, de forma que puedan echar mano de ellos después de ocurridos siniestros",
                                    "pagina": 53
                                },
                                {
                                    "dimension": "infraestructura_adaptacion",
                                    "cita": "reducir la fragilidad de los pequeños productores significa impulsar la creación de infraestructura de riego en zonas secas o susceptibles a sequías, cuando sea sostenible, a fin de aumentar los rendimientos agrícolas, reducir la dependencia por la precipitación",
                                    "pagina": 53
                                }
                            ],
                            "subsecciones": []
                        }
                    ]
                },
                {
                    "seccion": "C. Instrumentos financieros de transferencias de riesgos",
                    "nivel": 2,
                    "paginas": "54-61",
                    "resumen": "Analiza la taxonomía de los riesgos agropecuarios clasificándolos en independientes, sistémicos e intermedios (climáticos) y compara las características de los seguros tradicionales, microseguros inclusivos e instrumentos indizados. Demuestra que los seguros paramétricos eliminan los peritajes de campo y mitigan la selección adversa y el riesgo moral, requiriendo un riguroso modelado para minimizar el riesgo de base.",
                    "dimensiones": [
                        {
                            "dimension": "instrumentos_financieros",
                            "cita": "transferencia de riesgos mediante seguros agropecuarios es una opción que deberían tener los pequeños productores rurales a fin de aumentar su resiliencia ante eventos climáticos adversos.",
                            "pagina": 54
                        },
                        {
                            "dimension": "tipologia_riesgos",
                            "cita": "tercer tipo de riesgos se conoce como intermedios, ya que no son altamente independientes ni están altamente correlacionados, como los de origen climático. Por ende, la oferta de seguros contra riesgos intermedios es menor y las tasas de las primas tienden a ser mayores",
                            "pagina": 55
                        }
                    ],
                    "subsecciones": [
                        {
                            "seccion": "1. Riesgos y seguros agropecuarios",
                            "nivel": 3,
                            "paginas": "54-55",
                            "resumen": "Examina la falta de acceso de los productores de subsistencia a mecanismos formales de ahorro y crédito, lo que los deja desprotegidos ante eventos climáticos catastróficos. Al ser riesgos intermedios con correlación espacial moderada, el mercado privado no puede asegurarlos sin el concurso de subsidios estatales y esquemas de reaseguro internacional.",
                            "dimensiones": [
                                {
                                    "dimension": "barreras_financieras",
                                    "cita": "Dado que el objetivo principal de los productores rurales de subsistencia es preservar su seguridad alimentaria, verán en los instrumentos de transferencia de riesgos un costo innecesario y en algunos casos, inútil.",
                                    "pagina": 54
                                },
                                {
                                    "dimension": "riesgos_sistemicos",
                                    "cita": "no significa que los riesgos catastróficos sean no asegurables, sino que su cobertura no puede ser garantizada por seguros tradicionales o comerciales, y en muchos casos se requiere la participación de compañías reaseguradoras o respaldos estatales.",
                                    "pagina": 55
                                }
                            ],
                            "subsecciones": []
                        },
                        {
                            "seccion": "2. Seguros agropecuarios tradicionales y catastróficos",
                            "nivel": 3,
                            "paginas": "55-57",
                            "resumen": "Contrasta los seguros tradicionales (agrícolas, pecuarios y acuícolas basados en inspección in situ de la finca) con los seguros catastróficos basados en índices de rendimiento o clima. Señala que los esquemas indizados automatizan la liquidación de pagos sin verificación presencial, exigiendo como condición sine qua non una alta correlación espacial entre el índice y las pérdidas de los predios.",
                            "dimensiones": [
                                {
                                    "dimension": "seguros_tradicionales",
                                    "cita": "estimación de los daños probables en estos seguros se realiza mediante inspección in situ del predio o finca asegurada y se determina con base en una unidad de medida (predio o hectárea)",
                                    "pagina": 56
                                },
                                {
                                    "dimension": "seguros_indizados",
                                    "cita": "contratos estipulan indemnizaciones basadas en la ocurrencia de eventos climáticos extremos que afecten la producción de un área determinada, para la que se cuenta con datos históricos del clima.",
                                    "pagina": 56
                                }
                            ],
                            "subsecciones": []
                        },
                        {
                            "seccion": "3. Seguros agropecuarios tradicionales y microseguros",
                            "nivel": 3,
                            "paginas": "57-58",
                            "resumen": "Diferencia los microseguros de los seguros convencionales a partir de su enfoque exclusivo en clientes de bajos ingresos, la simplicidad de pólizas, pólizas grupales y recolección comunitaria adaptada a flujos de caja irregulares. Resalta la importancia de la educación del consumidor y de una cultura de responsabilidad social para evitar el fraude y consolidar la inclusión.",
                            "dimensiones": [
                                {
                                    "dimension": "microseguros",
                                    "cita": "En el caso de los microseguros debe tomarse en cuenta que la población objetivo es la de más bajos ingresos, lo que implica modelos de comercialización y de recolección y canales de distribución diferentes a los de los seguros convencionales.",
                                    "pagina": 57
                                },
                                {
                                    "dimension": "inclusion_financiera",
                                    "cita": "trámites y documentos relacionados con las pólizas de seguros deben ser más simples y fáciles de entender.",
                                    "pagina": 57
                                }
                            ],
                            "subsecciones": []
                        },
                        {
                            "seccion": "4. Seguros agropecuarios tradicionales y basados en índices",
                            "nivel": 3,
                            "paginas": "58-61",
                            "resumen": "Presenta una matriz comparativa entre seguros tradicionales e indizados, destacando que los indizados reducen la selección adversa y el riesgo moral al monitorear variables objetivas en tiempo real. No obstante, advierte que presentan un riesgo de base moderado a alto si las estaciones meteorológicas están distantes o si el modelo de regresión no refleja adecuadamente los daños en el cultivo.",
                            "dimensiones": [
                                {
                                    "dimension": "asimetria_informacion",
                                    "cita": "problemas de información asimétrica son menores, ya que el productor puede tener prácticamente la misma información que el asegurador con relación al valor del índice, siempre y cuando este se base en una variable objetiva, transparente y verificable de manera independiente.",
                                    "pagina": 60
                                },
                                {
                                    "dimension": "riesgo_de_base",
                                    "cita": "riesgo de base es bajo en los seguros tradicionales debido a que la ocurrencia de un siniestro que impacte negativamente los rendimientos del productor será medida in situ por los ajustadores",
                                    "pagina": 60
                                }
                            ],
                            "subsecciones": []
                        }
                    ]
                },
                {
                    "seccion": "D. Institucionalidad de la actividad de aseguramiento",
                    "nivel": 2,
                    "paginas": "61-64",
                    "resumen": "Analiza las estructuras normativas, institucionales y de reaseguro global indispensables para la viabilidad de los seguros agropecuarios. Sostiene que una política pública preventiva orientada a la gestión integral de riesgos reduce la siniestralidad, abarata las primas y atrae capitales de reaseguro internacional mediante contratos proporcionales o de stop loss.",
                    "dimensiones": [
                        {
                            "dimension": "marcos_regulatorios",
                            "cita": "supervisión de la salud financiera de las sociedades aseguradoras deberá fomentar la adopción y adaptación de los estándares internacionales, en particular los relacionados con suficiencia de capital y los riesgos de mercado, operacionales, de crédito y de liquidez",
                            "pagina": 61
                        },
                        {
                            "dimension": "politicas_publicas",
                            "cita": "Si la estrategia de política pública de las instituciones rectoras del desarrollo rural y de gestión de riesgos promueve un enfoque de gestión del riesgo preventivo, las fragilidades estructurales endógenas se reducirían y la estructura económica e institucional sería más resiliente.",
                            "pagina": 62
                        }
                    ],
                    "subsecciones": [
                        {
                            "seccion": "1. Marco regulatorio",
                            "nivel": 3,
                            "paginas": "61",
                            "resumen": "Demanda leyes y normativas explícitas para autorizar la operación de seguros paramétricos y la constitución de entidades públicas aseguradoras facultadas para canalizar subsidios y absorber costos operativos. Destaca la necesidad de alinear la supervisión con estándares de Basilea para cautelar la solvencia de las compañías y proteger los derechos del consumidor rural.",
                            "dimensiones": [
                                {
                                    "dimension": "marcos_regulatorios",
                                    "cita": "ley para la creación de la compañía de seguros pública debe contener, además, los mecanismos de su operatividad, incluyendo la posibilidad de asignar recursos para subsidiar primas y la absorción por parte del Estado de parte o la totalidad de los gastos operativos y administrativos",
                                    "pagina": 61
                                },
                                {
                                    "dimension": "supervision_financiera",
                                    "cita": "Adoptar legislación específica dará certeza a los negocios con productos de seguros, velando por el cumplimiento de los estándares internacionales por parte de las compañías y por la protección del consumidor de los servicios de aseguramiento.",
                                    "pagina": 61
                                }
                            ],
                            "subsecciones": []
                        },
                        {
                            "seccion": "2. Desarrollo institucional",
                            "nivel": 3,
                            "paginas": "61-63",
                            "resumen": "Propone fortalecer el liderazgo de los Ministerios de Agricultura mediante comités interinstitucionales de seguros y articular planes de prevención diferenciados para pequeños productores. Recomienda la asociatividad regional entre países del SICA para compartir costos de diseño, plataformas agrometeorológicas y negociación colectiva de reaseguros.",
                            "dimensiones": [
                                {
                                    "dimension": "capacidades_institucionales",
                                    "cita": "Para el desarrollo de los seguros agropecuarios se requieren ministerios de agricultura y ganadería líderes en el desarrollo agropecuario. Los ministerios deben contar con planes de trabajo de mediano y largo plazo basados en una visión estratégica",
                                    "pagina": 61
                                },
                                {
                                    "dimension": "cooperacion_regional",
                                    "cita": "se pueden evaluar las opciones de asociatividad regional entre los sistemas y mercados nacionales de seguros para reducir los costos de investigación, diseño y administración de instrumentos, sistemas de información agropecuaria y climática y contratación de reaseguros",
                                    "pagina": 62
                                }
                            ],
                            "subsecciones": []
                        },
                        {
                            "seccion": "3. Reaseguros y capitales internacionales",
                            "nivel": 3,
                            "paginas": "63-64",
                            "resumen": "Explica que el reaseguro internacional es esencial para superar la falla cognitiva y proteger a las aseguradoras locales frente a pérdidas catastróficas. Describe los esquemas proporcionales (cuota parte) y no proporcionales (exceso de pérdida), señalando que un marco regulatorio moderno y predecible brinda certeza a los inversionistas extranjeros.",
                            "dimensiones": [
                                {
                                    "dimension": "reaseguro_internacional",
                                    "cita": "instituciones reaseguradoras diversifican el riesgo a mayor escala mediante la creación de fondos comunes muy grandes y variados. Un reaseguro es el seguro comprado por las aseguradoras para protegerse de sus propios riesgos.",
                                    "pagina": 63
                                },
                                {
                                    "dimension": "mecanismos_financieros",
                                    "cita": "reaseguros proporcionales consisten en ceder una proporción del portafolio de la aseguradora a una compañía reaseguradora. Por ejemplo, una compañía aseguradora podrá convenir con una reaseguradora a ceder el 80% de su portafolio, de tal forma que el 20% del riesgo restante es retenido",
                                    "pagina": 64
                                }
                            ],
                            "subsecciones": []
                        }
                    ]
                },
                {
                    "seccion": "E. Sistemas de información de variables agroclimáticas",
                    "nivel": 2,
                    "paginas": "64-65",
                    "resumen": "Demuestra que la efectividad de los seguros indizados radica en contar con series históricas de clima, rendimientos y pérdidas de alta resolución espacial. Propone combinar redes meteorológicas terrestres con tecnología satelital e impulsar un sistema regional de información agrometeorológica que genere economías de escala y permita evaluar científicamente el impacto en el bienestar rural.",
                    "dimensiones": [
                        {
                            "dimension": "datos_y_sistemas_de_informacion",
                            "cita": "éxito depende de la disponibilidad y calidad de los datos históricos sobre el clima, los cultivos y pérdidas y los socioeconómicos (Hellmuth y otros, 2010). Los datos históricos de clima se usan para el diseño inicial del producto, determinar el precio de las primas y el monitoreo permanente",
                            "pagina": 64
                        },
                        {
                            "dimension": "tecnologias_satelitales",
                            "cita": "En las zonas donde no hay muchos datos históricos de los cultivos y pérdidas podrá utilizarse información satelital de imágenes para que, con el acompañamiento de un agrometeorólogo, se pueda determinar el tipo de cultivo, rendimientos y pérdidas probables.",
                            "pagina": 65
                        },
                        {
                            "dimension": "evaluacion_impacto",
                            "cita": "se requiere de información socioeconómica histórica y reciente con el objetivo de evaluar el impacto de programas de aseguramiento agropecuario. Si bien se parte del supuesto que los seguros agropecuarios son un instrumento de transferencia de riesgos que aumenta la resiliencia y la seguridad alimentaria",
                            "pagina": 65
                        }
                    ],
                    "subsecciones": []
                },
                {
                    "seccion": "F. Servicios integrales y fortalecimiento de capacidades",
                    "nivel": 2,
                    "paginas": "65-68",
                    "resumen": "Sintetiza la directriz estratégica de articular los seguros agropecuarios dentro de paquetes integrales de bienes y servicios (crédito, insumos adaptados, infraestructura, extensión y educación financiera). Concluye que la capacitación técnica y la coordinación multiactor (Estado, banca de desarrollo, reaseguradores y cooperativas) garantizan la sostenibilidad y escalabilidad del aseguramiento frente al cambio climático.",
                    "dimensiones": [
                        {
                            "dimension": "servicios_integrales",
                            "cita": "seguros agropecuarios son una herramienta que podría incluirse dentro de un paquete amplio de bienes y servicios a disposición del pequeño productor agropecuario con el propósito de volverlo más resiliente ante riesgos de desastres, principalmente los de origen hidrometeorológico",
                            "pagina": 65
                        },
                        {
                            "dimension": "educacion_financiera_capacitacion",
                            "cita": "bancos de desarrollo e instituciones públicas para ofrecer capacitación y educación financiera a los productores agropecuarios, promotores y extensionistas agropecuarios, incluyendo los seguros agropecuarios",
                            "pagina": 66
                        },
                        {
                            "dimension": "gobernanza_multiactor",
                            "cita": "desarrollo o fortalecimiento de los seguros agropecuarios requiere la participación de múltiples instituciones públicas, privadas, ONG y pequeños productores. Entre las instituciones se cuentan el sector público por medio de los ministerios de agricultura, los institutos de meteorología, la supervisión del sistema financiero",
                            "pagina": 67
                        }
                    ],
                    "subsecciones": []
                }
            ]
        }
    ],
    "hallazgos_candidatos": [
        "En Centroamérica y República Dominicana, el 77% de los eventos extremos que afectaron directamente al sector agropecuario entre 1900 y 2017 correspondieron a tormentas e inundaciones, sumando pérdidas sectoriales equivalentes al 66% de todos los daños en sectores productivos. (p.45, 48)",
        "Las proyecciones de cambio climático indican que hacia 2100 las pérdidas económicas acumuladas en Centroamérica en agricultura, recursos hídricos y biodiversidad podrían alcanzar entre el 32% (escenario B2) y el 54% (escenario A2) del PIB regional de 2008 si no se implementan medidas de adaptación. (p.50)",
        "Los seguros indizados reducen la selección adversa y el riesgo moral respecto a los seguros tradicionales al operar con índices meteorológicos objetivos y transparentes medidos en tiempo real, aunque presentan riesgo de base moderado o alto si existe heterogeneidad espacial o deficiencias en la densidad de estaciones meteorológicas. (p.59-61)"
    ],
    "recomendaciones_normativas": [
        {
            "recomendacion": "Integrar los seguros agropecuarios indizados dentro de paquetes integrales de bienes y servicios públicos (asistencia técnica, semillas resistentes, riego, crédito y educación financiera) para reducir la vulnerabilidad estructural campesina y garantizar la sostenibilidad del mercado asegurador.",
            "cita": "se inserten en una estrategia integral de apoyo a los micro y pequeños productores. Esta estrategia deberá incluir a otros actores como el Estado, las microfinancieras, las cooperativas, las asociaciones de productores, los agroservicios de insumos, las agroindustrias, las compañías públicas y privadas de seguros y las ONG nacionales e internacionales.",
            "pagina": 66
        },
        {
            "recomendacion": "Actualizar el marco regulatorio y legal nacional para autorizar explícitamente la operación de seguros paramétricos y facultar la creación de entidades públicas de aseguramiento con mecanismos para subsidiar primas y financiar costos operativos.",
            "cita": "La ley para la creación de la compañía de seguros pública debe contener, además, los mecanismos de su operatividad, incluyendo la posibilidad de asignar recursos para subsidiar primas y la absorción por parte del Estado de parte o la totalidad de los gastos operativos y administrativos con el propósito de garantizar su sostenibilidad.",
            "pagina": 61
        },
        {
            "recomendacion": "Reorientar parte de los fondos fiduciarios y de atención a emergencias hacia la inversión preventiva en sistemas de información agrometeorológica satelital y terrestre y reducción de vulnerabilidades, evitando generar desincentivos a la contratación del seguro.",
            "cita": "Si la estrategia de política pública de las instituciones rectoras del desarrollo rural y de gestión de riesgos promueve un enfoque de gestión del riesgo preventivo, las fragilidades estructurales endógenas se reducirían y la estructura económica e institucional sería más resiliente.",
            "pagina": 62
        }
    ]
}

# Verify all citations
citations_checked = 0
all_valid = True

def check_node(node):
    global citations_checked, all_valid
    for dim in node.get("dimensiones", []):
        citations_checked += 1
        ok, msg = check_quote(dim["cita"], dim["pagina"])
        if not ok:
            print(f"FAILED citation in section '{node['seccion']}': {msg}")
            all_valid = False
        else:
            if dim["pagina"] < 39 or dim["pagina"] > 68:
                print(f"PAGE OUT OF RANGE: {dim['pagina']} in section '{node['seccion']}'")
                all_valid = False
    for sub in node.get("subsecciones", []):
        check_node(sub)

for sec in parcial_b01["resumen_secciones"]:
    check_node(sec)

for rec in parcial_b01["recomendaciones_normativas"]:
    citations_checked += 1
    ok, msg = check_quote(rec["cita"], rec["pagina"])
    if not ok:
        print(f"FAILED citation in recomendacion: {msg}")
        all_valid = False
    else:
        if rec["pagina"] < 39 or rec["pagina"] > 68:
            print(f"PAGE OUT OF RANGE in recomendacion: {rec['pagina']}")
            all_valid = False

print(f"Total citations checked: {citations_checked}")
if all_valid:
    print("ALL CITATIONS AND PAGES ARE 100% VALID!")
    out_path = "corpus/intermedios/11362/45023/parcial_B01_INTRO_CAP_I.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(parcial_b01, f, indent=2, ensure_ascii=False)
    print(f"Saved to {out_path}")
else:
    print("ERRORS FOUND! Do not save yet.")
