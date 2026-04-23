wquant = 20 # define a quantidade de códigos a serem gerados no lote
import json
import os
from datetime import datetime
from typing import Optional, List, Dict
import requests
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Variáveis configuráveis
wquant = int(os.getenv('WQUANT', 20))
prefixo_empresa_env = os.getenv('PREFIXO_EMPRESA', '1933')
arquivo_json_env = os.getenv('ARQUIVO_JSON', 'ean_validos.json')

class GeradorEAN13:
    """
    Gerenciador completo de geração e validação de códigos EAN-13
    com persistência em JSON e validação via API opcional.
    """
    
    def __init__(self, arquivo_json: str = None, prefixo_empresa: str = None):
        self.arquivo_json = arquivo_json if arquivo_json is not None else arquivo_json_env
        self.prefixo_brasil = "789"
        # Aceita prefixo_empresa com 3 ou 4 dígitos
        self.prefixo_empresa = prefixo_empresa if prefixo_empresa is not None else prefixo_empresa_env
        if not (self.prefixo_empresa.isdigit() and 3 <= len(self.prefixo_empresa) <= 4):
            raise ValueError("O PREFIXO_EMPRESA deve ter 3 ou 4 dígitos numéricos.")
        self.prefixo_fixo = self.prefixo_brasil + self.prefixo_empresa  # 6 ou 7 dígitos
        self.codigos_gerados: List[Dict] = []
        self.contador_atual: int = 0
        self._carregar_dados()
    
    def _carregar_dados(self):
        """Carrega dados existentes do arquivo JSON"""
        if os.path.exists(self.arquivo_json):
            try:
                with open(self.arquivo_json, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.codigos_gerados = dados.get('codigos', [])
                    self.contador_atual = dados.get('contador', 0)
                print(f"📂 Dados carregados: {len(self.codigos_gerados)} códigos existentes")
            except Exception as e:
                print(f"⚠️ Erro ao carregar JSON: {e}")
                self.codigos_gerados = []
                self.contador_atual = 0
        else:
            print("📝 Novo arquivo JSON será criado")
    
    def _salvar_dados(self):
        """Salva os dados no arquivo JSON"""
        dados = {
            'contador': self.contador_atual,
            'total_gerados': len(self.codigos_gerados),
            'ultima_atualizacao': datetime.now().isoformat(),
            'prefixo': f"{self.prefixo_brasil}{self.prefixo_empresa}",
            'codigos': self.codigos_gerados
        }
        
        with open(self.arquivo_json, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def calcular_digito_verificador(codigo_12: str) -> str:
        """Calcula o dígito verificador EAN-13"""
        if len(codigo_12) != 12 or not codigo_12.isdigit():
            raise ValueError("Código deve ter 12 dígitos numéricos")
        
        soma = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(codigo_12))
        return str((10 - (soma % 10)) % 10)
    
    @staticmethod
    def validar_ean_local(ean13: str) -> bool:
        """Valida EAN-13 localmente usando o algoritmo oficial"""
        if len(ean13) != 13 or not ean13.isdigit():
            return False
        
        codigo_12 = ean13[:12]
        digito_informado = ean13[12]
        digito_calculado = GeradorEAN13.calcular_digito_verificador(codigo_12)
        
        return digito_informado == digito_calculado
    
    @staticmethod
    def validar_ean_api(ean13: str, timeout: int = 20) -> Dict: 
        """
        Valida EAN-13 usando APIs públicas gratuitas.
        Retorna dicionário com status e informações.
        """
        apis = [
            {
                'nome': 'BarcodeAPI.io',
                'url': f'https://api.barcodeapi.io/api/validate/{ean13}',
                'metodo': 'GET'
            },
            {
                'nome': 'UPC Database',
                'url': f'https://upcdatabase.com/api/validate/{ean13}',
                'metodo': 'GET'
            },
            {
                'nome': 'EAN-Search.org',
                'url': f'https://api.ean-search.org/api/v1/validate/{ean13}',
                'metodo': 'GET'
            }
        ]
        
        resultado = {
            'ean': ean13,
            'valido_local': GeradorEAN13.validar_ean_local(ean13),
            'valido_api': False,
            'api_usada': None,
            'detalhes': None,
            'erro': None
        }
        
        for api in apis:
            try:
                response = requests.get(api['url'], timeout=timeout)
                if response.status_code == 200:
                    dados = response.json()
                    resultado['valido_api'] = True
                    resultado['api_usada'] = api['nome']
                    resultado['detalhes'] = dados
                    break
            except requests.exceptions.RequestException as e:
                continue
            except json.JSONDecodeError:
                continue
        
        return resultado
    
    def _gerar_sequencia_inicial(self) -> int:
        """Gera sequência inicial baseada na hora atual (5 dígitos)"""
        agora = datetime.now()
        # Formato: HHMMS onde S = segundo // 6 (0-9)
        sequencia = f"{agora.hour:02d}{agora.minute:02d}{agora.second // 6}"
        return int(sequencia)
    
    def gerar_codigo(self, validar_api: bool = False) -> Dict:
        """
        Gera um novo código EAN-13 incremental.
        
        Args:
            validar_api: Se True, valida através de API pública
            
        Returns:
            Dicionário com informações do código gerado
        """
        # Incrementa contador
        self.contador_atual += 1
        
        # Usa hora como base na primeira geração, depois incrementa
        if self.contador_atual == 1 and len(self.codigos_gerados) == 0:
            base = self._gerar_sequencia_inicial()
        else:
            # Pega o último código e incrementa
            if self.codigos_gerados:
                ultimo_codigo = self.codigos_gerados[-1]['codigo']
                base = int(ultimo_codigo[7:12]) + 1
            else:
                base = self._gerar_sequencia_inicial()
        
        # Garante que a sequência tenha 5 dígitos (00000-99999)
        if base > 99999:
            print("⚠️ Limite de 99999 códigos atingido para este prefixo_empresa! Altere o PREFIXO_EMPRESA no .env para continuar gerando.")
            raise ValueError("Limite de 99999 códigos atingido para este prefixo_empresa! Altere o PREFIXO_EMPRESA no .env para continuar gerando.")

        sequencia = f"{base:05d}"
        codigo_12 = self.prefixo_fixo + sequencia
        digito_verificador = self.calcular_digito_verificador(codigo_12)
        ean13 = codigo_12 + digito_verificador
        
        # Validação local
        valido_local = self.validar_ean_local(ean13)
        
        # Validação API (opcional)
        validacao_api = None
        if validar_api:
            validacao_api = self.validar_ean_api(ean13)
        
        # Cria registro
        registro = {
            'codigo': ean13,
            'sequencia': sequencia,
            'digito_verificador': digito_verificador,
            'data_geracao': datetime.now().isoformat(),
            'contador': self.contador_atual,
            'valido_local': valido_local,
            'valido_api': validacao_api['valido_api'] if validacao_api else None,
            'api_validacao': validacao_api['api_usada'] if validacao_api else None
        }
        
        # Adiciona à lista e salva
        self.codigos_gerados.append(registro)
        self._salvar_dados()
        
        return registro
    
    def gerar_lote(self, quantidade: int, validar_api: bool = False, 
                   intervalo: float = 0.0) -> List[Dict]:
        """
        Gera múltiplos códigos em lote.
        
        Args:
            quantidade: Número de códigos a gerar
            validar_api: Se True, valida cada código via API
            intervalo: Delay entre gerações (segundos)
            
        Returns:
            Lista de códigos gerados
        """
        import time
        
        codigos = []
        print(f"🚀 Gerando {quantidade} códigos EAN-13...")
        
        for i in range(quantidade):
            try:
                codigo = self.gerar_codigo(validar_api=validar_api)
                codigos.append(codigo)
                print(f"  ✓ [{i+1}/{quantidade}] {codigo['codigo']}")
                
                if intervalo > 0:
                    time.sleep(intervalo)
                    
            except Exception as e:
                print(f"  ✗ Erro na geração {i+1}: {e}")
                break
        
        print(f"\n✅ {len(codigos)} códigos gerados com sucesso!")
        return codigos
    
    def validar_codigo_existente(self, ean13: str) -> Dict:
        """Valida um código EAN-13 existente"""
        return {
            'codigo': ean13,
            'valido_formato': len(ean13) == 13 and ean13.isdigit(),
            'valido_algoritmo': self.validar_ean_local(ean13),
            'prefixo_brasil': ean13[:3] == '789' if len(ean13) >= 3 else False,
            'prefixo_empresa': ean13[3:7] == self.prefixo_empresa if len(ean13) >= 7 else False,
            'detalhes_api': self.validar_ean_api(ean13)
        }
    
    def get_estatisticas(self) -> Dict:
        """Retorna estatísticas dos códigos gerados"""
        return {
            'total_gerados': len(self.codigos_gerados),
            'contador_atual': self.contador_atual,
            'arquivo': self.arquivo_json,
            'prefixo': f"{self.prefixo_brasil}{self.prefixo_empresa}",
            'ultima_geracao': self.codigos_gerados[-1]['data_geracao'] if self.codigos_gerados else None,
            'todos_validos_local': all(c['valido_local'] for c in self.codigos_gerados)
        }
    
    def exportar_lista_simples(self, arquivo_saida: str = "ean_lista.txt"):
        """Exporta apenas a lista de códigos em arquivo texto"""
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            for codigo in self.codigos_gerados:
                f.write(f"{codigo['codigo']}\n")
        print(f"📄 Lista exportada para {arquivo_saida}")


# ==========================================
# EXEMPLO DE USO
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("🏷️  SISTEMA DE GERAÇÃO EAN-13 - PADRÃO BRASIL")
    print("=" * 60)

    # Inicializa o gerador com variáveis do .env
    gerador = GeradorEAN13(arquivo_json=arquivo_json_env, prefixo_empresa=prefixo_empresa_env)

    # 1. Gerar um único código
    print("\n1️⃣  Gerando 1 código EAN-13:")
    codigo = gerador.gerar_codigo(validar_api=False)
    print(f"   Código: {codigo['codigo']}")
    print(f"   Válido (local): {codigo['valido_local']}")

    # 2. Gerar lote de códigos conforme wquant
    print(f"\n2️⃣  Gerando lote de {wquant} códigos:")
    lote = gerador.gerar_lote(quantidade=wquant, validar_api=False, intervalo=0.5)

    # 3. Validar um código específico via API
    print("\n3️⃣  Validando código via API pública:")
    if lote:
        codigo_teste = lote[0]['codigo']
        validacao = gerador.validar_ean_api(codigo_teste)
        print(f"   Código: {validacao['ean']}")
        print(f"   Válido (local): {validacao['valido_local']}")
        print(f"   Válido (API): {validacao['valido_api']}")
        print(f"   API usada: {validacao['api_usada'] or 'Nenhuma'}")

    # 4. Exibir estatísticas
    print("\n4️⃣  Estatísticas:")
    stats = gerador.get_estatisticas()
    for chave, valor in stats.items():
        print(f"   {chave}: {valor}")

    # 5. Exportar lista simples
    print("\n5️⃣  Exportando lista para arquivo texto:")
    gerador.exportar_lista_simples("ean_lista.txt")

    print("\n" + "=" * 60)
    print(f"✅ Processo concluído! Verifique o arquivo {arquivo_json_env}")
    print("=" * 60)