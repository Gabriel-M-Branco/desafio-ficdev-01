import os
import json
import pandas as pd
import matplotlib.pyplot as plt

def gerar_indicadores(df, total_linhas_originais):
    """Calcula estatísticas do dataframe processado."""
    if df is None or df.empty:
        return {}
    
    total_validos = len(df[df['registro_valido']])
    total_invalidos = len(df[~df['registro_valido']])
    percentual_invalidos = (total_invalidos / total_linhas_originais * 100) if total_linhas_originais > 0 else 0
    
    # Utilizando Pandas para agrupar e resumir
    cat_counts = df['categoria_padronizada'].value_counts().to_dict()
    status_counts = df['status'].value_counts().to_dict()
    tempo_medio = float(df['tempo_minutos'].mean()) if pd.notna(df['tempo_minutos'].mean()) else 0.0
    
    cat_mais_solicitada = df['categoria_padronizada'].mode()
    cat_mais_solicitada = cat_mais_solicitada[0] if not cat_mais_solicitada.empty else "Nenhuma"
    
    return {
        "total_atendimentos_processados": len(df),
        "total_originais": total_linhas_originais,
        "registros_validos": total_validos,
        "percentual_invalidos": round(percentual_invalidos, 2),
        "quantidade_por_categoria": cat_counts,
        "quantidade_por_status": status_counts,
        "tempo_medio_atendimento_minutos": round(tempo_medio, 2),
        "categoria_mais_solicitada": cat_mais_solicitada
    }

def exportar_graficos(df, dir_saida):
    """Gera dois gráficos com Matplotlib e salva em PNG."""
    if df is None or df.empty:
        return
        
    dir_graficos = os.path.join(dir_saida, "graficos")
    
    # 1. Gráfico de Atendimentos por Categoria
    plt.figure(figsize=(10, 6))
    contagem_cat = df['categoria_padronizada'].value_counts()
    contagem_cat.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Quantidade de Atendimentos por Categoria')
    plt.xlabel('Categoria')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(dir_graficos, 'atendimentos_por_categoria.png'))
    plt.close()

    # 2. Histograma da Distribuição dos Tempos de Atendimento
    plt.figure(figsize=(10, 6))
    df['tempo_minutos'].dropna().plot(kind='hist', bins=10, color='lightgreen', edgecolor='black')
    plt.title('Distribuição dos Tempos de Atendimento (minutos)')
    plt.xlabel('Tempo (min)')
    plt.ylabel('Frequência')
    plt.tight_layout()
    plt.savefig(os.path.join(dir_graficos, 'distribuicao_tempos.png'))
    plt.close()

def exportar_resultados(df, indicadores, dir_saida):
    """Exporta CSV limpo e JSON de resumo."""
    if df is not None and not df.empty:
        caminho_csv = os.path.join(dir_saida, "atendimentos_processados.csv")
        df.to_csv(caminho_csv, index=False, sep=';', encoding='utf-8')
    
    caminho_json = os.path.join(dir_saida, "resumo.json")
    with open(caminho_json, 'w', encoding='utf-8') as f:
        json.dump(indicadores, f, ensure_ascii=False, indent=4)