import json
import os

# Helper to verify quotes
def verify_quote(quote, page, tramo_dir):
    # Determine which file based on page
    if 226 <= page <= 250:
        filepath = os.path.join(tramo_dir, "tramo_226_250.txt")
    elif 251 <= page <= 268:
        filepath = os.path.join(tramo_dir, "tramo_251_268.txt")
    else:
        print(f"Page {page} out of range!")
        return False
        
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
        
    page_marker = f"=== PÁGINA PDF {page} ==="
    next_page_marker = f"=== PÁGINA PDF {page+1} ==="
    
    pos = text.find(page_marker)
    if pos == -1:
        print(f"ERROR: Page marker {page_marker} not found in {filepath}")
        return False
        
    next_pos = text.find(next_page_marker, pos)
    page_text = text[pos:next_pos] if next_pos != -1 else text[pos:]
    
    norm_quote = " ".join(quote.split())
    norm_page_text = " ".join(page_text.split())
    
    if norm_quote in norm_page_text:
        return True
    else:
        print(f"FAILED [p.{page}]: Quote not found in {filepath}!")
        print(f"Searched: {norm_quote[:80]}...")
        return False

tramo_dir = "corpus/intermedios/11362/45023/tramos"

quotes_to_test = [
    ("Las operaciones de seguros y reaseguros están reguladas por la Ley de Seguros y Fianzas en la República Dominicana (Ley N° 146-02, septiembre 2002) y la Ley de Seguro Agropecuario en la República Dominicana (Ley 157-09, abril 2009), que crea una plataforma para garantizar la inversión agropecuaria", 231),
    ("En la actualidad la única compañía pública que comercializa seguros agropecuarios es la Aseguradora Agropecuaria Dominicana S.A. (AGRODOSA), creada en 2001 por la Ley 479-08, una legislación especial impulsada desde el sector público y el privado.", 231),
    ("La DIGERA otorga un subsidio del 50% del costo de la póliza, con el objetivo de que los productores aseguren sus cosechas, infraestructuras o existencias de ganado, y así minimicen las pérdidas ante daños ocasionados por variaciones anormales de la naturaleza y por el cambio climático.", 232),
    ("La República Dominicana cuenta con una línea de crédito contingente con el BID por un monto de 100 millones de dólares con un plazo original de cinco años para atender eventos extremos derivados de terremotos y huracanes.", 233),
    ("AGRODOSA ofrece seguros para todos los cultivos, en particular para los tecnificados, que se ubican en plantaciones de arroz, plátanos, bananos, habichuelas, frutales, vegetales en ambientes protegidos y en campo abierto.", 234),
    ("AGRODOSA tiene contratos con reaseguradoras internacionales como la Swiss Reinsurance America Corporation (Suiza) y Hannover Rückrvershicherung A-G (Alemania) bajo la modalidad de cuota parte, mediante la que estas compañías son responsables del 75% de la suma asegurada.", 235),
    ("En 2012 el gobierno dominicano solicitó al Banco Mundial la elaboración de un estudio de factibilidad de seguros agropecuarios basados en índices climáticos.", 236),
    ("El satélite mide la reflectancia de la vegetación, se transforma en valores y se convierten en valores de salud de la vegetación en la zona. La resolución de los pixeles es de 250 x 250 metros. El índice se utiliza para estimar la cantidad, calidad y desarrollo de la vegetación con base en la medición de la actividad fotosintética expresada en el verdor de la vegetación.", 241),
    ("La ONAMET produce diariamente el Boletín Hidrometeorológico, que es un informe sobre las lluvias acumuladas en las últimas 24 horas, se divulga y consulta en línea. Utilizando herramientas de georreferenciación, la ONAMET presenta la precipitación registrada por las 60 estaciones meteorológicas disponibles", 244),
    ("A pesar de que Belice cuenta con una industria de seguros establecida que cubre los rubros de vida y no vida, no se han identificado aún seguros dirigidos específicamente al sector agropecuario", 248),
    ("El Gobierno de Belice ha desarrollado el Plan Nacional de Inversión Resiliente al Clima (NCRIP, por sus siglas en inglés) para abordar los impactos del cambio climático en el desarrollo social y económico.", 248),
    ("El monto de las pérdidas derivadas de las tormentas que han impactado negativamente a Belice entre 2000 y 2016 se estiman en 737 millones de dólares, habiendo sido erogados 10 millones de dólares en la atención de dichas emergencias.", 249),
    ("Belice ha sido miembro de la OECS Commission and the Caribbean Catastrophe Risk Insurance Facility (CCRIF SPC) desde 2007, con pólizas para huracanes, exceso de lluvia y eventos de terremotos, pero optó por no renovar sus pólizas en el período de cobertura 2017-2018.", 249),
    ("CCRIF SPC realizó un pago de 261,073 dólares (BZ $322.146) al Gobierno de Belice como resultado de las fuertes lluvias del huracán Earl del 4 al 5 de agosto de 2016.", 250),
    ("Actualmente hay 21 estaciones meteorológicas manuales y 23 automáticas. No obstante, las estaciones generalmente no se ubican cerca de comunidades agrícolas remotas, lo que crea un desafío para obtener los datos requeridos y proporcionar el pronóstico correspondiente.", 250),
    ("El Consejo Agropecuario Centroamericano (CAC), foro regional de los ministros de agricultura, incluyó el tema de los seguros agropecuarios en sus resoluciones desde principios de la década de 2000.", 250),
    ("El CAC aprobó en 2017 la Estrategia de agricultura sostenible adaptada al clima para la región del SICA (EASAC 2018-2030) cuyo eje 2 propone la Gestión integral de riesgos y adaptación al clima.", 251),
    ("En la XXXV Reunión Ordinaria de Jefes de Estado y de Gobierno de los países del SICA, de junio de 2010, se aprueba la Política Centroamericana de Gestión Integral de Riesgo de Desastres (PCGIR)", 251),
    ("Posteriormente fue creado el Fondo Centroamericano de la Gestión de Riesgo de Desastres (FOCEGIR), aprobado en la XXXVIII Reunión Ordinaria de Jefes de Estado y de Gobierno de los Países del Sistema de la Integración Centroamericana (SICA), en diciembre de 2011.", 251),
    ("En la XXXI Reunión de febrero de 2013, el COSEFIN analizó la posibilidad de estructurar una operación de Seguro Regional ante Desastres con la participación de especialistas del BID, Banco Mundial y Banco Centroamericano de Integración Económica (BCIE)", 252),
    ("El Banco Interamericano de Desarrollo (BID/Fondo Multilateral de Inversiones (FOMIN) apoyó un proyecto de desarrollo del mercado de seguros agropecuarios en Centroamérica, en colaboración con los ministerios de agricultura, el Banco Mundial y el BCIE, con apoyo del Programa Canadiense de Asistencia Técnica y la Federación Interamericana de Empresas de Seguros (FIDES)", 253),
    ("El Comité Regional de Recursos Hídricos (CRRH), organismo técnico del SICA, tiene entre sus objetivos fomentar acciones en los campos de recursos atmosféricos, hídricos y de manejo de cuencas orientados a la protección del medio ambiente y a la prevención y mitigación de desastres naturales.", 253),
    ("El Sistema de Alerta Temprana para Centroamérica (SATCA) es un proyecto de gestión de riesgo y alerta temprana impulsado por el Programa Mundial de Alimentos (PMA) de Naciones Unidas en colaboración con el Ministerio de Medio Ambiente y Recursos Naturales de El Salvador", 253),
    ("El componente que más avances ha registrado es el del Marco legal, regulatorio y de supervisión. Al menos cuatro países han logrado completar los requerimientos legales para que los seguros agropecuarios estén debidamente regulados y supervisados", 254),
    ("Uno de los componentes que requerirá mayor atención y programación de acciones es el de la Gestión integral de riesgos e institucionalidad. La CEPAL ha insistido, a través de las reuniones de expertos de la comunidad de práctica con los países SICA, en la necesidad de minimizar la fragilidad económica, social y ambiental en la que se desenvuelven los pequeños productores agropecuarios", 254),
    ("En general, se percibe que los países de la región aún no cuentan con una estrategia gubernamental para el desarrollo o fortalecimiento de los seguros agropecuarios desde una perspectiva de gestión integral de riesgos, incluyendo alianzas público-privadas.", 255),
    ("En cuanto a las condiciones de oferta, demanda e inclusión financiera a favor de los seguros agropecuarios, es con seguridad el componente evaluado que ha reportado los mayores avances en la región SICA en el último quinquenio.", 255),
    ("Al respecto, la MiCRO filial de Swiss Re ha establecido alianzas estratégicas con el BFA de El Salvador y Aseguradora Rural de Guatemala para lanzar seguros paramétricos que tengan por objetivo proteger a los clientes de dichas instituciones a proteger el capital invertido cuando este se ha obtenido mediante la adquisición de créditos.", 256),
    ("En materia de sistemas de información agropecuaria, de desarrollo rural, cambio climático y gestión de riesgos los países del SICA requieren de la inversión de recursos humanos, tecnológicos y financieros a fin de garantizar que se cuente tanto con sistemas de información de producción, rendimiento y de gestión de riesgos en el sector agropecuario", 256),
    ("el componente de legalidad, normatividad e institucional tendría un cumplimiento arriba del 80%, seguido de las condiciones de oferta, demanda e inclusión financiera por arriba del 60%. En los rangos más bajos de cumplimiento se encontrarían los componentes de datos sobre rendimientos y sistemas de información agroclimáticos, así como el de gestión integral de riesgos e institucionalidad.", 257),
    ("La reducción de las vulnerabilidades y por tanto de la probabilidad de riesgo de desastres en la actividad agropecuaria, son un factor clave para el diseño, implementación y éxito de los instrumentos de transferencias de riesgos como los seguros agropecuarios.", 259),
    ("El sector público participa a través del diseño e implementación de políticas de inclusión financiera, tomando en cuenta instrumentos financieros como depósitos, créditos, garantías, fianzas, almacenamiento y seguros agropecuarios, así como la regulación y supervisión del sistema financiero en general, y de la actividad aseguradora en particular.", 259),
    ("Sería deseable que en cada país de la región SICA hubiese una institución pública responsable del diseño, desarrollo, diseminación y comercialización de los seguros agropecuarios tradicionales o paramétricos.", 260),
    ("Se requiere, además, apoyo gubernamental para otorgar subsidios a las primas de los seguros dirigidos a los micros y pequeños productores agropecuarios.", 260),
    ("Los seguros agropecuarios indizados tienen la virtud de eliminar la selección adversa y el riesgo moral, aunque deben batallar con el riesgo de base.", 260),
    ("El índice de precipitación estandarizado es ampliamente utilizado en el diseño de los seguros paramétricos. El índice resulta muy intuitivo y fácil de explicar a los productores. No obstante, tiene la desventaja de no incluir un indicador de temperatura, con lo que no es posible contar con una medida que refleje las condiciones probables de evapotranspiración y su incidencia en el crecimiento de los cultivos.", 261),
    ("Los elevados costos de los censos y las encuestas, hará más necesaria la formación y adopción de tecnologías de uso de datos de fuentes satelitales con su debida validación en los ámbitos nacionales y locales, así como el uso de aplicaciones para celulares para el intercambio de información con los pequeños productores agropecuarios.", 262)
]

all_ok = True
for q, p in quotes_to_test:
    res = verify_quote(q, p, tramo_dir)
    if not res:
        all_ok = False

if all_ok:
    print(f"ALL {len(quotes_to_test)} QUOTES VERIFIED SUCCESSFULLY!")
else:
    print("SOME QUOTES FAILED!")
