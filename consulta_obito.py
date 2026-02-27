#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ferramenta CLI para Consulta de Óbito
Integra múltiplas APIs brasileiras de dados de falecimentos
"""

import sys
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import urllib.parse

class ConsultaObitoAPI:
    """Classe para gerenciar consultas de óbito em múltiplas fontes"""
    
    def __init__(self):
        self.resultados = []
        self.timeout = 10
        
    def consultar_cnf_brasil(self, nome: str) -> Optional[Dict]:
        """
        Consulta o Cadastro Nacional de Falecidos (CNF Brasil)
        
        Args:
            nome: Nome da pessoa a buscar
            
        Returns:
            Dicionário com dados encontrados ou None
        """
        try:
            # Limpar nome: apenas letras e espaços
            nome_limpo = ''.join(c for c in nome if c.isalpha() or c.isspace()).strip()
            
            if not nome_limpo:
                return None
            
            # URL da API CNF Brasil
            url = "https://www.falecidosnobrasil.org.br/api/search"
            params = {
                "nome": nome_limpo,
                "exato": False
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                dados = response.json()
                if dados and isinstance(dados, list) and len(dados) > 0:
                    return {
                        "fonte": "CNF Brasil",
                        "encontrado": True,
                        "dados": dados,
                        "total_resultados": len(dados)
                    }
            
            return None
            
        except Exception as e:
            print(f"[ERRO] Erro ao consultar CNF Brasil: {str(e)}", file=sys.stderr)
            return None
    
    def consultar_registro_civil(self, nome: str, data_nascimento: Optional[str] = None) -> Optional[Dict]:
        """
        Consulta o Portal Registro Civil
        
        Args:
            nome: Nome da pessoa
            data_nascimento: Data de nascimento (opcional)
            
        Returns:
            Dicionário com dados encontrados ou None
        """
        try:
            # O Portal Registro Civil oferece busca pública
            url = "https://www.registrocivil.org.br/search"
            params = {
                "nome": nome,
                "tipo": "obito"
            }
            
            if data_nascimento:
                params["data_nascimento"] = data_nascimento
            
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                return {
                    "fonte": "Portal Registro Civil",
                    "encontrado": True,
                    "url": response.url
                }
            
            return None
            
        except Exception as e:
            print(f"[AVISO] Erro ao consultar Registro Civil: {str(e)}", file=sys.stderr)
            return None
    
    def consultar_sim_datasus(self, nome: str) -> Optional[Dict]:
        """
        Consulta dados do Sistema de Informação sobre Mortalidade (SIM) do DATASUS
        
        Args:
            nome: Nome da pessoa
            
        Returns:
            Dicionário com dados encontrados ou None
        """
        try:
            # DATASUS oferece dados abertos sobre mortalidade
            url = "http://sim.saude.gov.br/api/search"
            params = {
                "nome": nome,
                "tipo": "obito"
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                return {
                    "fonte": "SIM DATASUS",
                    "encontrado": True,
                    "url": response.url
                }
            
            return None
            
        except Exception as e:
            print(f"[AVISO] Erro ao consultar SIM DATASUS: {str(e)}", file=sys.stderr)
            return None
    
    def consultar_todas_fontes(self, nome: str, cpf: Optional[str] = None, 
                               data_nascimento: Optional[str] = None) -> List[Dict]:
        """
        Consulta todas as fontes disponíveis
        
        Args:
            nome: Nome da pessoa
            cpf: CPF (opcional)
            data_nascimento: Data de nascimento (opcional)
            
        Returns:
            Lista com resultados de todas as fontes
        """
        resultados = []
        
        # Consultar CNF Brasil (principal fonte)
        resultado_cnf = self.consultar_cnf_brasil(nome)
        if resultado_cnf:
            resultados.append(resultado_cnf)
        
        # Consultar Registro Civil
        resultado_rc = self.consultar_registro_civil(nome, data_nascimento)
        if resultado_rc:
            resultados.append(resultado_rc)
        
        # Consultar SIM DATASUS
        resultado_sim = self.consultar_sim_datasus(nome)
        if resultado_sim:
            resultados.append(resultado_sim)
        
        return resultados
    
    def formatar_resultado(self, resultados: List[Dict]) -> str:
        """
        Formata os resultados para exibição no terminal
        
        Args:
            resultados: Lista de resultados
            
        Returns:
            String formatada para exibição
        """
        if not resultados:
            return "❌ Nenhum registro de óbito encontrado nas bases de dados consultadas."
        
        output = []
        output.append("\n" + "="*70)
        output.append("RESULTADO DA CONSULTA DE ÓBITO")
        output.append("="*70)
        output.append(f"Data/Hora da consulta: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        output.append(f"Total de fontes com resultado: {len(resultados)}")
        output.append("-"*70)
        
        for i, resultado in enumerate(resultados, 1):
            output.append(f"\n📋 Fonte {i}: {resultado['fonte']}")
            output.append(f"   Status: {'✅ ENCONTRADO' if resultado['encontrado'] else '❌ NÃO ENCONTRADO'}")
            
            if 'dados' in resultado and resultado['dados']:
                if isinstance(resultado['dados'], list):
                    output.append(f"   Total de registros: {len(resultado['dados'])}")
                    for j, dado in enumerate(resultado['dados'][:3], 1):  # Mostrar até 3 registros
                        output.append(f"   Registro {j}:")
                        if isinstance(dado, dict):
                            for chave, valor in dado.items():
                                output.append(f"      • {chave}: {valor}")
                        else:
                            output.append(f"      {dado}")
                    
                    if len(resultado['dados']) > 3:
                        output.append(f"   ... e mais {len(resultado['dados']) - 3} registros")
            
            if 'url' in resultado:
                output.append(f"   URL: {resultado['url']}")
        
        output.append("\n" + "="*70)
        output.append("CONCLUSÃO:")
        
        if resultados:
            output.append("✅ PESSOA POSSIVELMENTE EM ÓBITO - Registros encontrados em bases de dados")
            output.append("   Recomendação: Verificar detalhes nos portais oficiais")
        else:
            output.append("❌ NÃO ENCONTRADO - Nenhum registro de óbito nas bases consultadas")
            output.append("   Nota: Ausência de registro não garante que a pessoa esteja viva")
        
        output.append("="*70 + "\n")
        
        return "\n".join(output)


def exibir_ajuda():
    """Exibe mensagem de ajuda"""
    help_text = """
╔════════════════════════════════════════════════════════════════════╗
║         FERRAMENTA DE CONSULTA DE ÓBITO - VERSÃO 1.0              ║
║                                                                    ║
║  Uso: python3 consulta_obito.py [opções]                          ║
║                                                                    ║
║  Opções:                                                           ║
║    -n, --nome <nome>           Nome da pessoa a consultar          ║
║    -c, --cpf <cpf>             CPF (opcional)                      ║
║    -d, --data <DD/MM/YYYY>     Data de nascimento (opcional)       ║
║    -h, --help                  Exibe esta mensagem de ajuda        ║
║    -v, --version               Exibe versão                        ║
║                                                                    ║
║  Exemplos:                                                         ║
║    python3 consulta_obito.py -n "João Silva"                      ║
║    python3 consulta_obito.py -n "Maria Santos" -c "12345678901"   ║
║    python3 consulta_obito.py -n "Pedro Costa" -d "15/03/1950"     ║
║                                                                    ║
║  Fontes de dados consultadas:                                      ║
║    • CNF Brasil (Cadastro Nacional de Falecidos)                   ║
║    • Portal Registro Civil                                         ║
║    • SIM DATASUS (Sistema de Informação sobre Mortalidade)         ║
║                                                                    ║
║  ⚠️  AVISO LEGAL:                                                  ║
║    Este sistema consulta bases de dados públicas. O uso deve       ║
║    estar em conformidade com a LGPD e legislação vigente.          ║
║    Uso exclusivo para fins legítimos e autorizados.                ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """
    print(help_text)


def main():
    """Função principal"""
    
    # Processar argumentos
    nome = None
    cpf = None
    data_nascimento = None
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg in ['-h', '--help']:
            exibir_ajuda()
            sys.exit(0)
        
        elif arg in ['-v', '--version']:
            print("Consulta de Óbito v1.0")
            sys.exit(0)
        
        elif arg in ['-n', '--nome']:
            if i + 1 < len(sys.argv):
                nome = sys.argv[i + 1]
                i += 2
            else:
                print("❌ Erro: -n/--nome requer um argumento", file=sys.stderr)
                sys.exit(1)
        
        elif arg in ['-c', '--cpf']:
            if i + 1 < len(sys.argv):
                cpf = sys.argv[i + 1]
                i += 2
            else:
                print("❌ Erro: -c/--cpf requer um argumento", file=sys.stderr)
                sys.exit(1)
        
        elif arg in ['-d', '--data']:
            if i + 1 < len(sys.argv):
                data_nascimento = sys.argv[i + 1]
                i += 2
            else:
                print("❌ Erro: -d/--data requer um argumento", file=sys.stderr)
                sys.exit(1)
        
        else:
            print(f"❌ Erro: Argumento desconhecido: {arg}", file=sys.stderr)
            exibir_ajuda()
            sys.exit(1)
    
    # Validar entrada
    if not nome:
        print("❌ Erro: Nome é obrigatório. Use -n ou --nome", file=sys.stderr)
        exibir_ajuda()
        sys.exit(1)
    
    # Executar consulta
    print("\n🔍 Consultando bases de dados de óbito...")
    print("Aguarde...\n")
    
    consulta = ConsultaObitoAPI()
    resultados = consulta.consultar_todas_fontes(nome, cpf, data_nascimento)
    
    # Exibir resultado
    print(consulta.formatar_resultado(resultados))
    
    # Retornar código de saída apropriado
    if resultados:
        sys.exit(0)  # Encontrado
    else:
        sys.exit(1)  # Não encontrado


if __name__ == "__main__":
    main()
