# AI Dev Harness

AI Dev Harness (`aih`) é um projeto pessoal e educacional para construir, em pequenos marcos, um harness para agentes de IA voltados ao desenvolvimento de software. A prioridade é entender cada camada antes de automatizar a próxima.

## Estado atual

O primeiro marco implementa apenas `aih status`: identifica a raiz do repositório Git que contém o diretório atual e mostra o nome do repositório, a branch e contagens de arquivos modificados, novos e staged. O programa somente lê o estado do Git. Ainda não há modelo de IA, agente, ferramentas de escrita ou sandbox.

## Requisitos e instalação local

- Python 3.11 ou mais recente
- Git disponível no `PATH`

Na raiz do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

O modo `-e` instala o pacote de forma editável: alterações em `src/aih` passam a ser usadas pelo comando instalado sem reinstalar. A aplicação e os testes usam apenas a biblioteca padrão do Python; o Git é um requisito externo.

## Uso

Entre em qualquer repositório Git local, inclusive em uma subpasta, e execute:

```bash
aih status
```

Para observar as chamadas internas ao Git:

```bash
aih --verbose status
```

`aih` sem subcomando mostra a ajuda. Fora de um repositório, `aih status` informa o problema em `stderr` e retorna código 1.

## Testes

```bash
python -m unittest discover -s tests -v
```

Os testes criam repositórios em diretórios temporários usando `tempfile.TemporaryDirectory`. Eles não alteram nem dependem do repositório onde o projeto está sendo desenvolvido.

## Arquitetura atual

```text
src/aih/cli.py       entrada da CLI e apresentação do resultado
src/aih/workspace.py  descoberta da raiz Git a partir do diretório atual
src/aih/git.py        execução de comandos Git e leitura de branch/status
tests/               verificações em repositórios temporários
```

O fluxo de `aih status` é: CLI → descoberta do workspace → consulta ao Git → formatação da saída. Usamos `argparse`, `subprocess`, `pathlib` e `logging` da biblioteca padrão. O Git é chamado como lista de argumentos, sem shell. A saída `--porcelain=v1 -z` do status tem formato estável e separa os caminhos com NUL, o que evita confusão com espaços ou quebras de linha em nomes de arquivos.

## Próximos marcos possíveis

Após revisar e compreender esta fundação, um próximo marco pequeno pode adicionar ferramentas **somente de leitura** do workspace. Integração com modelos, loops de agente, permissões, sandbox e outras camadas ficam para etapas posteriores.

Princípios: entender antes de automatizar; marcos pequenos; código explícito; segurança antes de autonomia; observabilidade desde o começo; um agente antes de múltiplos; ferramentas antes de orquestração; contexto importa tanto quanto o modelo; Git como rede de segurança.
