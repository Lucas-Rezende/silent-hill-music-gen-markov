# silent-hill-music-gen-markov
Pipeline para geração de música simbólica (MIDI) com Cadeias de Markov, utilizando como base músicas da OST de *Silent Hill 1–4*.

## Como utilizar
Clone o repositório, instale uma versão atual de Python (preferencialmente `Python 3.10.12`, a mesma versão utilizada no desenvolvimento do projeto) e instale as dependências em um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r _requirements.txt
```

Os arquivos MIDI do corpus não são distribuídos no repositório. As instruções para reconstrução e organização do corpus estão em `_metadata/CORPUS.md`, caso queira utilizar as mesmas músicas. Caso queira usar seus próprios arquivos MIDI, basta criar uma pasta (<output_path>) e adicionar os arquivos MIDI dentro dela.

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
- `--order`: ordem `N` da Cadeia de Markov.
- `--resolution`: passos temporais por semínima.
- `--seed`: random seed.
- `--numsongs`: quantidade de músicas geradas.

Os hiperparâmetros avaliados no trabalho são `order` e `resolution`.

## Replicação dos experimentos
Para gerar os mesmos MIDI utilizados na experimentação e discussão dos resultados, basta rodar:
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

## Exemplos gerados
Exemplos de músicas geradas em MIDI e suas respectivas versões sintetizadas em áudio (.wav) estão disponíveis em `outputs/favorites/`.

## Créditos
A reconstrução dos arquivos de *Silent Hill 2* utiliza [Nisto/sh2ex](https://github.com/Nisto/sh2ex) e [Nisto/kdt-tool](https://github.com/Nisto/kdt-tool).
Parte do corpus foi obtida a partir de arquivos MIDI disponíveis em acervos como MIDIFind, HomeTown e VGMusic.
A soundfont utilizada para renderizar os áudios sintetizados foi [Silent Guy Vol. 2 PS2](https://ko-fi.com/s/e87f78ff2c), feita por SoundFontGuy.

## Uso de IA
Foi utilizado o GPT-5.6 Sol para:
1. auxiliar na criação dos scripts (utilizados para construir o corpus e renderizar as músicas):
   1.  `scripts/extract_convert_all_bgm.py`
   2.  `synthesize_favorites_vol2`
2. auxiliar na síntese e organização do README,
3. auxiliar na revisão gramatical e teórica do resumo do trabalho.