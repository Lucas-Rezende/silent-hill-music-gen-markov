# silent-hill-music-gen-markov
Pipeline para geração de música simbólica (MIDI) com Cadeias de Markov, utilizando como corpus músicas da trilha sonora de *Silent Hill 1–4*.

## Como utilizar o projeto
Primeiramente, instale as dependências (para facilitar, use ambiente):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Em seguida, basta rodar:
```bash
PYTHONWARNINGS="ignore:Unable to import Axes3D" python3 main.py output/<specific_corpus_path> <output_path> --order <N> --resolution <R> --seed <seed> --numsongs <n>
```
Hiperparâmetros disponíveis:
- `--order`: ordem `N` da Cadeia de Markov, i.e., quantidade de estados anteriores utilizados como contexto.
- `--resolution`: quantidade de passos temporais por semínima.
- `--seed`: semente aleatória para reprodutibilidade.
- `--numsongs`: quantidade de músicas geradas.

Os hiperparâmetros avaliados no trabalho são `order` e `resolution`.

## Como replicar os experimentos
```bash
mkdir -p outputs

for resolution in 1 2 4 8; do
    for order in 1 2 3 4 5 10 15 50 100; do
        echo "corpus=all | N=$order | resolution=$resolution"

        PYTHONWARNINGS="ignore:Unable to import Axes3D" \
        python3 main.py corpus/all outputs \
            --order "$order" \
            --resolution "$resolution" \
            --seed 42 \
            --numsongs 5
    done
done
```

## Como recriar o corpus
Consulte `_metadata/CORPUS.md`

## Créditos e ferramentas utilizadas
Parte do corpus complementar foi obtida a partir de transcrições MIDI feitas por fãs disponíveis em acervos como MIDIFind, HomeTown e VGMusic.

## Uso de IA
Foi utilizado o GPT-5.6 Sol para:
1. Criação do script `scripts/extract_convert_all_bgm.py`, para ajudar na geração do corpus.
2. Auxiliar no resumo e organização do README.
3. Auxiliar na revisão gramatical e teórica do resumo do trabalho.