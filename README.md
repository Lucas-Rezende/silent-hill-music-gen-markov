# silent-hill-music-gen-markov
Experimental Markov Chain music generator pipeline based on the Silent Hill soundtrack.

## Como recriar o corpus
O corpus foi construído utilizando arquivos do jogo e MIDIs feitos por fãs, disponibilizados na internet. Para replicar a parte do corpus correspondente às músicas presentes na ISO do jogo é necessário uma cópia do jogo.

Nesse sentido, possuindo alguma das ISOs aceitas (ver README do sh2ex), utilize o repositório Nisto/sh2ex e Nisto/kdt-tool. Clone ambos dentro da pasta `tools`:

```bash
mkdir -p tools
cd tools

git clone https://github.com/Nisto/sh2ex.git
git clone https://github.com/Nisto/kdt-tool.git
```

Em seguida, Execute sh2ex passando o caminho da ISO:
```bash
cd sh2ex
python3 sh2ex.py "/path/to/SilentHill2.iso"
```

Os experimentos deste projeto foram realizados utilizando SLES-51156 - Director's Cut (v1.02).

Após executar o sh2ex.py na ISO do jogo, serão criadas duas pastas. Usaremos exclusivamente a pasta de nome '[Your ISO name] - sound'. Encontre esta pasta para garantir que o processo deu certo. Nesta pasta estão as músicas sequenciadas do jogo, armazenadas em grupos de arquivos `.TD`, `.HD` e `.BD` (.TD: contém dados de sequência e eventos, .HD: contém metadados dos bancos de sons, .BD: contém os samples utilizados pelos bancos de sons).

Para o treinamento, usaremos apenas os do bloco KDT1, presentes nos arquivos .TD, pois podem ser convertidos para MIDI.

Assim, use o script `extract_convert_all_bgm.py`, que automatiza o processo de converter os arquivos `.TD` em MIDI. Use:

```bash
python3 scripts/extract_convert_all_bgm.py \
    "/path/to/[Your ISO name] - sound"
```

Após isso, os MIDIs baseados nos arquivos do jogo estarão em `corpus/game`. Em seguida, adicione seus próprios MIDIs ou outros encontrados na internet de músicas do jogo para encorporar o corpus. Para os experimentos deste trabalho, as músicas útilizadas estão disponíveis em `corpus/metadata/other_songs.csv`.
Os MIDIs externos estão organizados em `corpus/others`. Cada som está na pasta de seu respectivo jogo.

```bash
corpus/others/
├── SH1/
├── SH2/
├── SH3/
└── SH4/
```

## Créditos e ferramentas utilizadas

A reconstrução do corpus do jogo utiliza as ferramentas [Nisto/sh2ex](https://github.com/Nisto/sh2ex) e [Nisto/kdt-tool](https://github.com/Nisto/kdt-tool), responsáveis por extrair os arquivos da ISO de Silent Hill 2 e pela conversão das sequências KDT1 para MIDI.

Parte do corpus complementar foi construída a partir de transcrições MIDI feitas por fãs encontradas em acervos como MIDIFind, HomeTown e VGMusic.