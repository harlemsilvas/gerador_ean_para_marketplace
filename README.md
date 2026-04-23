# Gerador e Validador de Códigos EAN-13

Este projeto gera e valida códigos EAN-13, com persistência em JSON e validação opcional via API pública.

## Configuração

As variáveis de ambiente devem ser definidas em um arquivo `.env` na raiz do projeto. Um exemplo está disponível em `.env.local`.

### Variáveis configuráveis

- `WQUANT`: Quantidade de códigos a serem gerados em lote (padrão: 5)
- `PREFIXO_EMPRESA`: Prefixo da empresa (3 ou 4 dígitos, ex: 1933 ou 123)
- `ARQUIVO_JSON`: Caminho do arquivo JSON para persistência dos códigos (ex: ean_validos.json)
- `CAMINHO_SAIDA_TXT`: Caminho do arquivo de saída da lista simples (ex: ean_lista.txt)

> **Atenção:** O campo `PREFIXO_EMPRESA` identifica a empresa ou pode ser usado para controle interno. O padrão EAN-13 utiliza prefixos para identificar o país e a empresa. Ajuste conforme sua necessidade e controle.

### Exemplo de `.env`

```env
QUANTIDADE_A_GERAR=10                       # Quantidade de códigos a serem gerados em lote
PREFIXO_EMPRESA=9999            # Prefixo da empresa (3 ou 4 dígitos)
ARQUIVO_JSON=ean_validos.json   # Caminho do arquivo JSON para persistência
CAMINHO_SAIDA_TXT=ean_lista.txt # Caminho do arquivo de saída da lista simples
```

### Exemplo de `.env.local`

```env
QUANTIDADE_A_GERAR=__QUANTIDADE__             # Quantidade de códigos a serem gerados em lote (ex: 20)
PREFIXO_EMPRESA=__EMPRESA__       # Prefixo da empresa (3 ou 4 dígitos, ex: 1933 ou 123)
ARQUIVO_JSON=__CAMINHO_JSON__     # Caminho do arquivo JSON para salvar os códigos (ex: ean_validos.json)
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

## Autor

**HDevSoluções**  
Transformando ideias em soluções digitais  
Desenvolvedor especializado em criar experiências digitais incríveis e funcionais

- **Contato:** contato@hdevsolucoes.tech / hdevsolucoes@gmail.com
- **WhatsApp:** (11) 96774-5351
- **Localização:** São Paulo - SP
- **Site:** https://hdevsolucoes.tech/

---

## Como contribuir ou utilizar

Você pode utilizar este projeto de duas formas:

- **Fork:**
  1.  Clique em "Fork" no topo da página do repositório no GitHub.
  2.  Faça suas alterações e envie Pull Requests para contribuir.

- **Clone:**
  1.  Clone o repositório para sua máquina:
      ```sh
      git clone https://github.com/hdevsolucoes/ean-validos.git
      ```
  2.  Siga as instruções de configuração e uso acima.

## Licença e direitos

Este projeto é distribuído sob a licença MIT. Você pode usar, modificar e distribuir livremente, desde que mantenha os créditos ao autor.

© 2026 HDevSoluções. Todos os direitos reservados.

Para mais detalhes, consulte o arquivo LICENSE.

<div align="center">
   <a href="https://hdevsolucoes.tech/" title="Site"><img src="https://img.shields.io/badge/Site-hdevsolucoes.tech-blue?style=flat&logo=google-chrome"/></a>
   <a href="https://github.com/hdevsolucoes" title="GitHub"><img src="https://img.shields.io/badge/GitHub-hdevsolucoes-black?style=flat&logo=github"/></a>
   <a href="https://www.instagram.com/hdevsolucoes/" title="Instagram"><img src="https://img.shields.io/badge/Instagram-hdevsolucoes-E4405F?style=flat&logo=instagram&logoColor=white"/></a>
   <a href="https://x.com/hdevsolucoes" title="X"><img src="https://img.shields.io/badge/X-hdevsolucoes-000000?style=flat&logo=x"/></a>
   <a href="https://www.linkedin.com/in/harlem-afonso-claumann-silva-bb5160356/" title="LinkedIn"><img src="https://img.shields.io/badge/LinkedIn-hdevsolucoes-0A66C2?style=flat&logo=linkedin&logoColor=white"/></a>
 </div>

<div align="center" style="margin-top: 2em;">
   <sub>© 2026 HDevSoluções. Todos os direitos reservados.</sub>
</div>
