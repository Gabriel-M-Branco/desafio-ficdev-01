import logging
import os

from src.leitura import garantir_diretorios, ler_categorias, ler_configuracoes
from src.processamento import processar_dados
from src.relatorios import exportar_graficos, exportar_resultados, gerar_indicadores
from src.validacao import extrair_dados_observacoes


def configurar_logging(dir_saida):
    """Configura o sistema de log para escrever em arquivo."""

    caminho_log = os.path.join(dir_saida, "erros.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(caminho_log, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def main():
    print("Iniciando Sistema de Análise de Atendimentos...")

    try:
        config = ler_configuracoes()
        dir_saida = garantir_diretorios(config)
        configurar_logging(dir_saida)

        logging.info("Carregando mapa de categorias...")
        mapa_categorias = ler_categorias(config.get("arquivo_categorias"))

        logging.info("Extraindo informações do TXT...")
        telefones_extraidos = extrair_dados_observacoes(config.get("arquivo_observacoes"))

        logging.info(f"Telefones/Protocolos extraídos: {len(telefones_extraidos)}")

        logging.info("Processando base de dados CSV...")
        df_processado, total_originais = processar_dados(config, mapa_categorias)

        if df_processado is not None and not df_processado.empty:
            indicadores = gerar_indicadores(df_processado, total_originais)

            logging.info("Gerando gráficos (Matplotlib)...")
            exportar_graficos(df_processado, dir_saida)

            logging.info("Exportando dados limpos e resumo JSON...")
            exportar_resultados(df_processado, indicadores, dir_saida)

            logging.info("Processamento concluído com sucesso. Cheque a pasta /output.")
        else:
            logging.warning("Não há dados válidos para gerar relatórios.")

    except Exception as e:
        logging.critical(f"Erro inesperado no sistema: {e}")


if __name__ == "__main__":
    main()
