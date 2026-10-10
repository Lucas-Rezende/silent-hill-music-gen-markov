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
```

Os experimentos deste projeto utilizaram a versão `SLES-51156 - Director's Cut (v1.02)`.
Após a extração, utilize o script abaixo para extrair as sequências KDT1 dos arquivos `.TD` e convertê-las para MIDI:

```bash
python3 scripts/extract_convert_all_bgm.py \
    "/path/to/[Your ISO name] - sound"
```

Os MIDIs resultantes são armazenados em:

```text
corpus/game/
```