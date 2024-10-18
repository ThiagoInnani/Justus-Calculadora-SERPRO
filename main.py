# Tabela de preços conforme as faixas
preco_consulta = [(300, 0.24), (1000, 0.21), (3000, 0.18), (7000, 0.16), (15000, 0.14), (23000, 0.11), (30000, 0.09), (float('inf'), 0.06)]
preco_emissao = [(500, 0.32), (5000, 0.29), (10000, 0.26), (15000, 0.22), (25000, 0.19), (35000, 0.17), (50000, 0.12), (float('inf'), 0.06)]
preco_declaracao = [(100, 0.40), (500, 0.36), (1000, 0.32), (3000, 0.28), (5000, 0.24), (10000, 0.20), (float('inf'), 0.12)]

def calcular_preco_e_faixas(consumo, tabela_precos):
    faixas_utilizadas = []
    custo_total = 0
    consumo_restante = consumo

    for faixa, preco in tabela_precos:
        if consumo_restante <= 0:
            break
        if consumo_restante <= faixa:
            custo = consumo_restante * preco
            faixas_utilizadas.append((consumo_restante, preco))
            custo_total += custo
            break
        else:
            custo = faixa * preco
            faixas_utilizadas.append((faixa, preco))
            custo_total += custo
            consumo_restante -= faixa

    return custo_total, faixas_utilizadas

# Função principal para calcular o custo do Integra Contador
def calcular_custo_integra(num_empresas, consultas_por_empresa, emissoes_por_empresa, declaracoes_por_empresa):
    consumo_total_consultas = num_empresas * consultas_por_empresa
    consumo_total_emissoes = num_empresas * emissoes_por_empresa
    consumo_total_declaracoes = num_empresas * declaracoes_por_empresa
    
    custo_consultas, faixas_consultas = calcular_preco_e_faixas(consumo_total_consultas, preco_consulta)
    custo_emissoes, faixas_emissoes = calcular_preco_e_faixas(consumo_total_emissoes, preco_emissao)
    custo_declaracoes, faixas_declaracoes = calcular_preco_e_faixas(consumo_total_declaracoes, preco_declaracao)
    
    custo_total = custo_consultas + custo_emissoes + custo_declaracoes
    
    return {
        'Custo Consultas': custo_consultas,
        'Custo Emissões': custo_emissoes,
        'Custo Declarações': custo_declaracoes,
        'Custo Total': custo_total,
        'Faixas Consultas': faixas_consultas,
        'Faixas Emissões': faixas_emissoes,
        'Faixas Declarações': faixas_declaracoes
    }

def formatar_detalhes_faixa(faixas):
    detalhes = []
    for quantidade, preco in faixas:
        detalhes.append(f"{quantidade} requisições a R$ {preco:.2f}")
    return " e ".join(detalhes)

def simular_custo_integra():
    print("Simulador de Custos do Integra Contador")
    print("----------------------------------------")
    
    while True:
        try:
            num_empresas = int(input("Número de empresas clientes: "))
            consultas_por_empresa = int(input("Número de consultas por empresa/mês: "))
            emissoes_por_empresa = int(input("Número de emissões por empresa/mês: "))
            declaracoes_por_empresa = int(input("Número de declarações por empresa/mês: "))
            
            resultado = calcular_custo_integra(num_empresas, consultas_por_empresa, emissoes_por_empresa, declaracoes_por_empresa)
            
            print("\nResultado da simulação:")
            print(f"Custo total: R$ {resultado['Custo Total']:.2f}")
            print(f"Custo Consultas: R$ {resultado['Custo Consultas']:.2f} ({formatar_detalhes_faixa(resultado['Faixas Consultas'])})")
            print(f"Custo Emissões: R$ {resultado['Custo Emissões']:.2f} ({formatar_detalhes_faixa(resultado['Faixas Emissões'])})")
            print(f"Custo Declarações: R$ {resultado['Custo Declarações']:.2f} ({formatar_detalhes_faixa(resultado['Faixas Declarações'])})")
            
            continuar = input("\nDeseja fazer outra simulação? (s/n): ").lower()
            if continuar != 's':
                break
        except ValueError:
            print("Por favor, insira apenas números inteiros.")

if __name__ == "__main__":
    simular_custo_integra()
