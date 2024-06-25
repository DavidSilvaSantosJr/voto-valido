dic_problemas = {
    "Pavimentação": [
        "Buracos no asfalto",
        "Rachaduras e ondulações",
        "Asfalto desgastado",
        "Falta de sinalização horizontal(marcações no chão)",
        "Sinalização viária apagada ou danificada"
    ],
    "Obras": [
        "Desvios mal sinalizados",
        "Faixas interditadas sem aviso prévio",
        "Sinalização de obras incompleta ou inadequada",
        "Atraso na conclusão das obras"
    ],
    "Drenagem": [
        "Pontos de alagamento",
        "elevação/depressão de bueiros",
        "Valetas entupidas",
        "buerio com tampa quebrada"
    ],
    "Pontes e Passarelas": [
        "Pontes danificadas",
        "Passarelas em mau estado",
        "Falta de iluminação em pontes e passarelas",
        "risco de queda"
    ],
    "Transporte Público": [
        "Falta de linhas de ônibus",
        "Ônibus em mau estado",
        "Frota insuficiente",
        "Falta de segurança nos ônibus",
        "Ponto de ônibus em mal estado"
    ],
    "Praças e Parques": [
        "Falta de manutenção",
        "Equipamentos de lazer danificados",
        "Falta de iluminação",
        "Presença de moradores de rua",
        "Presença de usuários de drogas",
        "Mato alto",
        "Árvores encostando em fios elétricos"
    ],
    "Calçadas": [
        "Desníveis e buracos",
        "Falta de rampas de acessibilidade",
        "Calçadas estreitas",
        "Ocupação por vendedores ambulantes"
    ],
    "Áreas Verdes": [
        "Falta de cuidado e manutenção",
        "Risco de incêndios",
        "Invasão por construções irregulares",
        "Árvores muito próximas de fiação elétrica"
    ],
    "Iluminação Pública": [
        "Lâmpadas queimadas",
        "Postes de iluminação danificados",
        "Falta de iluminação em áreas periféricas",
        "fios de poste/alta tensão furtados"
    ],
    "Segurança Pública": [
        "Falta de policiamento",
        "Iluminação pública precária",
        "Presença de pontos de drogas",
        "Vandalismo",
        "Veículos executando manobras perigosas"
    ],
    "Outros": [
        "Falta de coleta de lixo",
        "Rede de esgoto precária"
    ],
    "Prédios do governo/prefeitura": [
        "Mau estado",
        "Funcionários mal educados",
        "Falta de profissionais",
        "Falta de professores",
        "bebedouros/banheiros em má condições"
    ]
}

topicos = []
for k,v in dic_problemas.items():
    topicos.append(k)
#print (topicos)

## retorno botoes para tipo de atualizacao da cidade
buscas = [
    'meus_prob',
    'mais_repercurtidos',
    'busca_categoria'
]

estados = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "SC", "SE", "SP", "TO"
]