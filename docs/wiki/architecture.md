# Arquitetura do Projeto IBGE-GeoData

## Organização da Estrutura de Diretórios

### 📁 Estrutura Geral

```
ibge-geodata/
├── geodata/                    # Código-fonte principal
│   ├── __init__.py
│   ├── core/                   # Camada central — Lógica principal
│   │   ├── __init__.py
│   │   ├── base.py             # Classe principal GeoDataBase (orquestração)
│   │   ├── enums.py            # Enumerações consolidadas
│   │   ├── client.py           # Cliente HTTP com lógica de cache
│   │   ├── models.py           # Definições de tipos e TypedDicts
│   │   └── locator.py          # Localizador geográfico (ponto-em-polígono)
│   ├── storage/                # Camada de armazenamento
│   │   ├── __init__.py
│   │   └── cache.py            # Gerenciamento de cache (SQLite)
│   └── utils/                  # Utilidades
│       ├── __init__.py
│       ├── geocoords.py        # Classe GeoCoords para coordenadas
│       ├── constants.py        # Constantes globais (URLs, TTL)
│       └── exceptions.py       # Exceções customizadas
├── tests/                      # Suíte de testes
│   ├── conftest.py             # Configuração e fixtures compartilhadas
│   ├── unit/                   # Testes unitários (sem dependências externas)
│   │   ├── __init__.py
│   │   └── test_cache.py       # Testes de cache
│   ├── integration/            # Testes de integração (com API real)
│   │   ├── __init__.py
│   │   └── test_geodata.py     # Testes com API IBGE
│   └── fixtures/               # Dados e mocks reutilizáveis
│       └── __init__.py
├── docs/                       # Documentação
│   ├── wiki/                   # Guias de usuário
│   └── assets/                 # Recursos (logos, ícones)
├── pyproject.toml              # Configuração Poetry
├── mkdocs.yml                  # Configuração MkDocs
├── README.md                   # Documentação principal
└── .gitignore
```

## Detalhes de Cada Camada

### 🎯 `geodata/core/` — Camada Central

Responsável pela lógica principal do negócio geográfico.

#### **base.py** — `GeoDataBase`

- Classe principal para interação com dados geográficos
- **Responsabilidades**: Orquestração, interfaces públicas
- **Delega para**:
  - `HTTPClient` para operações HTTP e cache
  - `CacheManager` para caminhos e gerenciamento de cache
  - `metadata` e `polygons` como propriedades públicas

#### **enums.py** — Enumerações

Fonte de verdade para todos os tipos enumerados do pacote:

- `SpatialLevel`: Níveis espaciais (`COUNTRY`, `REGION`, `STATE`, `MUNICIPALITY`, etc.)
- `Metadata`: Categorias de metadados correspondentes
- `GeoLevel`: Combina `SpatialLevel` e `Metadata`
- `Quality`: Qualidade dos dados (`LOW`, `MEDIUM`, `HIGH`)

#### **client.py** — `HTTPClient`

- Encapsula toda a lógica HTTP e de cache
- **Métodos**:
  - `fetch_polygons()`: Busca dados espaciais com cache SQLite (TTL de 86400 s)
  - `fetch_metadata()`: Busca metadados da API IBGE
- **Dependências**: `hishel`, `httpx`, `geopandas`

#### **models.py** — Tipos de Dados

- `TypedDict` para respostas da API
- Facilita type-checking com Pylance / MyPy
- Documenta as estruturas de dados das APIs IBGE

#### **locator.py** — `GeoLocator`

- Localização ponto-em-polígono em múltiplos níveis administrativos IBGE
- Locator com cache reutilizável

### 💾 `geodata/storage/` — Camada de Armazenamento

#### **cache.py** — `CacheManager`

- Gerenciamento centralizado de cache SQLite
- **Métodos**:
  - `get_cache_dir()`: Retorna o diretório plataforma-específico
    - Windows: `AppData\Local\geodata_cache\`
    - Linux/macOS: `~/.cache/geodata_cache/`
  - `get_cache_path(geolevel_value, quality_value)`: Gera o path do arquivo SQLite
  - `clear_cache(geolevel_value?, quality_value?)`: Limpa cache total ou parcial

### 🔧 `geodata/utils/` — Utilidades

#### **constants.py** — Constantes Globais

```python
URL_SPATIAL      = "https://servicodados.ibge.gov.br/api/v4/malhas"
URL_METADATA     = "https://servicodados.ibge.gov.br/api/v1/localidades"
DEFAULT_CACHE_TTL = 86400          # 1 dia em segundos
CACHE_DIR_NAME   = "geodata_cache"
CACHE_DB_SUFFIX  = ".sqlite"
```

#### **exceptions.py** — Exceções Customizadas

| Exceção           | Descrição                        |
| ----------------- | -------------------------------- |
| `GeoDataError`    | Base exception do pacote         |
| `CacheError`      | Problemas com operações de cache |
| `FetchError`      | Falhas ao buscar dados           |
| `ValidationError` | Dados inválidos                  |
| `APIError`        | Erros retornados pela API IBGE   |

#### **geocoords.py** — `GeoCoords`

- Classe para coordenadas WGS-84 validadas
- Conversões (UTM, shapely `Point`), distância geodésica e bearing

### ✅ `tests/` — Organização de Testes

#### **unit/** — Testes Unitários

- Testes isolados, sem dependências externas nem rede
- `test_cache.py`: Validação de paths, diretórios e nomes de arquivo
- Rápidos, confiáveis, executam offline

#### **integration/** — Testes de Integração

- Testes que realizam chamadas reais à API IBGE
- `test_geodata.py`: Inicialização e fetch de metadados
- Requerem conexão com a internet

#### **conftest.py** — Configuração Compartilhada

- Fixtures `sample_geolevel`, `sample_quality`, `sample_geodata`
- Configuração global do pytest

## Fluxo de Dados

```
┌─────────────────────────────────────────┐
│  Usuário / API Externa                  │
└──────────────┬──────────────────────────┘
               │
               ▼
       ┌───────────────────┐
       │   GeoDataBase     │  ← Orquestração
       │   (base.py)       │
       └─────────┬─────────┘
                 │
         ┌───────┴───────┐
         ▼               ▼
   ┌──────────────┐  ┌──────────────┐
   │  HTTPClient  │  │ CacheManager │
   │ (client.py)  │  │ (storage/)   │
   └──────┬───────┘  └──────┬───────┘
          │                  │
   ┌──────▼──────────┐       │
   │   IBGE APIs     │       │
   │ (constants.py)  │       │
   └─────────────────┘       │
                      ┌──────▼──────────┐
                      │  SQLite Cache   │
                      │ (~/.cache/...)  │
                      └─────────────────┘
```

## Importações

Todos os pontos de importação abaixo são suportados:

```python
# Topo-level (recomendado para uso geral)
from geodata import GeoData, GeoLevel, Quality, GeoLocator

# Core — enums
from geodata.core.enums import GeoLevel, Quality, SpatialLevel, Metadata

# Core — classes
from geodata.core.client import HTTPClient
from geodata.core.locator import GeoLocator

# Armazenamento
from geodata.storage import CacheManager

# Utilidades
from geodata.utils.geocoords import GeoCoords
from geodata.utils.exceptions import GeoDataError, CacheError, APIError
from geodata.utils.constants import URL_SPATIAL, DEFAULT_CACHE_TTL
```

## Configuração do Cache

**Localização**: Plataforma-específica

| Plataforma | Caminho                         |
| ---------- | ------------------------------- |
| 🐧 Linux   | `~/.cache/geodata_cache/`       |
| 🍎 macOS   | `~/.cache/geodata_cache/`       |
| 🪟 Windows | `%LOCALAPPDATA%\geodata_cache\` |

**Padrão de nomenclatura**: `{spatial}_{quality}.sqlite`

Exemplo: `regiao_maxima.sqlite`

**TTL padrão**: 86400 segundos (1 dia)

**Limpeza Manual**:

```python
from geodata.storage import CacheManager

# Limpar cache específico
CacheManager.clear_cache("regiao", "maxima")

# Limpar todos os caches de um nível
CacheManager.clear_cache("regiao")

# Limpar tudo
CacheManager.clear_cache()
```

## Princípios de Design

1. **Separação de Responsabilidades** — Cache em `storage/`, HTTP em `client.py`, enums em `enums.py`
2. **Type Safety** — TypedDicts em `models.py`, enums em `enums.py`, compatível com Pylance/MyPy
3. **Testes Organizados** — Unit tests rápidos e offline; integration tests com APIs reais separados
4. **Extensibilidade** — Camada `storage/` preparada para padrão Repository; `utils/` extensível

## Futuras Melhorias

- `storage/repository.py` — Padrão Repository para troca entre backends (SQLite, PostgreSQL, etc.)
- `utils/validators.py` — Validações de entrada centralizadas e reutilizáveis
- `utils/formatters.py` — Conversão entre formatos (GeoJSON, WKT, etc.)
- `cli/` — Interface de linha de comando para gerenciamento de cache e downloads offline

## Executando Testes

```bash
# Testes unitários (rápidos, offline)
poetry run pytest tests/unit/ -v

# Testes de integração (requer conexão com a API IBGE)
poetry run pytest tests/integration/ -v

# Todos os testes
poetry run pytest tests/ -v

# Com coverage
poetry run pytest tests/ --cov=geodata --cov-report=html
```
