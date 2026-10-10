# silent-hill-music-gen-markov
Pipeline para geração de música simbólica (MIDI) com Cadeias de Markov, utilizando como base músicas da OST de *Silent Hill 1–4*.

## Como utilizar
Clone o repositório e instale as dependências em um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

O desenvolvimento foi realizado com `Python 3.10.12`.
Os arquivos MIDI do corpus não são distribuídos no repositório. A estrutura de diretórios está disponível em `corpus/`, e as instruções para reconstrução estão em:

```text
/_metadata/CORPUS.md
```

Após reconstruir o corpus, execute:

```bash
PYTHONWARNINGS="ignore:Unable to import Axes3D" python3 main.py \
    corpus/<specific_corpus> <output_path> \
    --order <N> \
    --resolution <R> \
    --seed <seed> \
    --numsongs <n>
```

Parâmetros:
- `--order`: ordem `N` da Cadeia de Markov;
- `--resolution`: passos temporais por semínima;
- `--seed`: semente aleatória para reprodutibilidade;
- `--numsongs`: quantidade de músicas geradas.

Os hiperparâmetros avaliados no trabalho são `order` e `resolution`.

## Replicação dos experimentos
```bash
mkdir -p outputs

for resolution in 1 2 4 8; do
    for order in 1 2 3 4 5 10 15 50 100; do
        PYTHONWARNINGS="ignore:Unable to import Axes3D" \
        python3 main.py corpus/all outputs \
            --order "$order" \
            --resolution "$resolution" \
            --seed 42 \
            --numsongs 5
    done
done
```

## Créditos
A reconstrução dos arquivos de *Silent Hill 2* utiliza [Nisto/sh2ex](https://github.com/Nisto/sh2ex) e [Nisto/kdt-tool](https://github.com/Nisto/kdt-tool).
Parte do corpus foi obtida a partir MIDI disponíveis em acervos como MIDIFind, HomeTown e VGMusic.

## Uso de IA
Foi utilizado o GPT-5.6 Sol para:
1. auxiliar na criação do script `scripts/extract_convert_all_bgm.py`,
2. auxiliar na síntese e organização do README,
3. auxiliar na revisão gramatical e teórica do resumo do trabalho.