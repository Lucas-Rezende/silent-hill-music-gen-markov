## Recriando o corpus

Os arquivos MIDI utilizados nos experimentos não são distribuídos neste repositório.

Crie a estrutura utilizada pelo projeto:

```bash
mkdir -p corpus/all \
         corpus/all-separated-by-game \
         corpus/all-without-repetition \
         corpus/game-only \
         corpus/not-official-only
```

A organização utilizada nos experimentos é:

```text
corpus/game-only/                 MIDIs extraídos diretamente do jogo
corpus/not-official-only/         MIDIs obtidos nos acervos indicados nos metadados
corpus/all/                       união dos dois conjuntos
corpus/all-separated-by-game/     corpus separado por Silent Hill 1–4
corpus/all-without-repetition/    corpus com transcrições alternativas removidas
```

Os arquivos utilizados e suas fontes são documentados nos CSVs presentes em `_metadata/`.

### Extração dos arquivos de Silent Hill 2

Para reconstruir essa parte do corpus, é necessária uma cópia compatível do jogo. Consulte o README do [Nisto/sh2ex](https://github.com/Nisto/sh2ex) para verificar as versões suportadas.

Clone as ferramentas em `tools/`:

```bash
mkdir -p tools
cd tools

git clone https://github.com/Nisto/sh2ex.git
git clone https://github.com/Nisto/kdt-tool.git
```

Execute o `sh2ex` passando o caminho da ISO:

```bash
cd sh2ex
python3 sh2ex.py "/path/to/SilentHill2.iso"
cd ../..
```

Os experimentos deste projeto utilizaram a versão `SLES-51156 - Director's Cut (v1.02)`.

Após a extração, utilize o script abaixo para extrair as sequências KDT1 dos arquivos `.TD` e convertê-las para MIDI:

```bash
python3 scripts/extract_convert_all_bgm.py \
    "/path/to/[Your ISO name] - sound"
```

Os MIDIs resultantes são armazenados em:

```text
corpus/game-only/
```
