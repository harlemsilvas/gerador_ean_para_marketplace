# Gerador e Validador de Códigos EAN-13

Este projeto gera e valida códigos EAN-13, com persistência em JSON e validação opcional via API pública.

## Configuração

As variáveis de ambiente devem ser definidas em um arquivo `.env` na raiz do projeto. Um exemplo está disponível em `.env.local`.

### Variáveis configuráveis

- `WQUANT`: Quantidade de códigos a serem gerados em lote (padrão: 20)
- `PREFIXO_EMPRESA`: Prefixo da empresa (3 ou 4 dígitos, ex: 1933 ou 123)
- `ARQUIVO_JSON`: Caminho do arquivo JSON para persistência dos códigos (ex: ean_validos.json)
- `CAMINHO_SAIDA_TXT`: Caminho do arquivo de saída da lista simples (ex: ean_lista.txt)

> **Atenção:** O campo `PREFIXO_EMPRESA` identifica a empresa ou pode ser usado para controle interno. O padrão EAN-13 utiliza prefixos para identificar o país e a empresa. Ajuste conforme sua necessidade e controle.

### Exemplo de `.env`

```env
WQUANT=20                  # Quantidade de códigos a serem gerados em lote
PREFIXO_EMPRESA=1933       # Prefixo da empresa (3 ou 4 dígitos)
ARQUIVO_JSON=ean_validos.json # Caminho do arquivo JSON para persistência
CAMINHO_SAIDA_TXT=ean_lista.txt # Caminho do arquivo de saída da lista simples
```

### Exemplo de `.env.local`

```env
WQUANT=__QUANTIDADE__        # Quantidade de códigos a serem gerados em lote (ex: 20)
PREFIXO_EMPRESA=__EMPRESA__  # Prefixo da empresa (3 ou 4 dígitos, ex: 1933 ou 123)
ARQUIVO_JSON=__CAMINHO_JSON__ # Caminho do arquivo JSON para salvar os códigos (ex: ean_validos.json)
CAMINHO_SAIDA_TXT=__CAMINHO_TXT__ # Caminho do arquivo de saída da lista simples (ex: ean_lista.txt)
```

## Uso

1. Configure o arquivo `.env` com seus parâmetros.
2. Execute o script de ambiente para instalar dependências e preparar o ambiente virtual:
   - No Windows: `setup_env.bat`
   - No Linux/Mac: `bash setup_env.sh`
3. Execute o script principal para gerar e validar códigos:
   - `python ean-valido.py`
4. Os códigos gerados serão salvos no arquivo JSON e a lista simples no arquivo TXT configurado.

## Sobre o limite de 99999 códigos

O sistema permite gerar até 99.999 códigos por prefixo. Caso precise gerar mais, basta alterar o valor de `PREFIXO_EMPRESA` para outro identificador (pode ser reduzido para 3 dígitos, ex: 123), permitindo continuar a geração sem perder o padrão EAN-13.

## Observações

- O prefixo da empresa é parte fundamental do código EAN-13 e pode ser ajustado para fins de controle.
- O projeto salva todos os códigos gerados e permite exportação para arquivo texto.
- Para uso em produção, consulte as normas oficiais do GS1 para emissão de prefixos válidos.

---

**Mantenha seu arquivo `.env` fora do controle de versão (adicione ao `.gitignore`).**

---

## Iniciando o repositório

1. Inicialize o repositório Git:
   ```sh
   git init
   git add .
   git commit -m "Projeto EAN-13: estrutura inicial"
   ```
2. Crie um repositório no GitHub e siga as instruções para adicionar o remoto e fazer o push inicial.
