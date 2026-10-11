#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

import mido

ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "outputs" / "favorites" / "MIDI"
FAVORITES_DIR = ROOT / "outputs" / "favorites"
SOUNDFONT_ROOT = ROOT / "Silent Guy Vol. 2 PS2"

SOUNDFONTS = {
    "instruments": {
        "filename": "Silent Guy Vol. 2 Instruments PS2.sf2",
        "output_folder": "sintetizados_instruments_ps2",
    },
    "pads": {
        "filename": "Silent Guy Vol. 2 Pads PS2.sf2",
        "output_folder": "sintetizados_pads_ps2",
    },
}


def find_soundfont(filename: str) -> Path:
    matches = sorted(
        SOUNDFONT_ROOT.rglob(filename),
        key=lambda path: (len(path.parts), str(path)),
    )

    if not matches:
        raise FileNotFoundError(
            f"SoundFont não encontrada: {filename}\n"
            f"Procurei dentro de: {SOUNDFONT_ROOT}"
        )

    return matches[0]


def set_program(input_path: Path, output_path: Path, program: int) -> None:
    midi = mido.MidiFile(input_path)
    found_program_change = False

    for track in midi.tracks:
        for message in track:
            if message.type == "program_change":
                message.program = program
                found_program_change = True

    if not found_program_change and midi.tracks:
        midi.tracks[0].insert(
            0,
            mido.Message("program_change", program=program, time=0),
        )

    midi.save(output_path)


def render_wav(
    midi_path: Path,
    wav_path: Path,
    soundfont: Path,
    sample_rate: int,
) -> None:
    subprocess.run(
        [
            "fluidsynth",
            "-ni",
            str(soundfont),
            str(midi_path),
            "-F",
            str(wav_path),
            "-r",
            str(sample_rate),
        ],
        check=True,
    )


def convert_to_mp3(
    wav_path: Path,
    mp3_path: Path,
    bitrate: str,
) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(wav_path),
            "-codec:a",
            "libmp3lame",
            "-b:a",
            bitrate,
            str(mp3_path),
        ],
        check=True,
    )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Sintetiza os MIDIs de outputs/favorites/MIDI em MP3 usando "
            "as SoundFonts Instruments PS2 e Pads PS2 do Silent Guy Vol. 2."
        )
    )

    parser.add_argument(
        "--only",
        choices=list(SOUNDFONTS),
        help=(
            "Gera apenas uma versão. "
            "Opções: instruments, pads. "
            "Se omitido, gera as duas."
        ),
    )

    parser.add_argument(
        "--program",
        type=int,
        help=(
            "Preset MIDI de 0 a 127. "
            "Se omitido, mantém o program original do MIDI."
        ),
    )

    parser.add_argument(
        "--sample-rate",
        type=int,
        default=44100,
        help="Sample rate usado na renderização intermediária. Padrão: 44100.",
    )

    parser.add_argument(
        "--bitrate",
        default="192k",
        help="Bitrate dos MP3s. Padrão: 192k.",
    )

    args = parser.parse_args()

    if args.program is not None and not 0 <= args.program <= 127:
        parser.error("--program deve estar entre 0 e 127.")

    if args.sample_rate <= 0:
        parser.error("--sample-rate deve ser maior que 0.")

    return args


def get_midi_files() -> list[Path]:
    return sorted(
        path
        for path in INPUT_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in {".mid", ".midi"}
    )


def render_collection(
    name: str,
    output_folder: str,
    soundfont: Path,
    midi_files: list[Path],
    program: int | None,
    sample_rate: int,
    bitrate: str,
) -> None:
    output_dir = FAVORITES_DIR / output_folder
    output_dir.mkdir(parents=True, exist_ok=True)

    print()
    print("=" * 72)
    print(f"Versão: {name}")
    print(f"SoundFont: {soundfont}")
    print(f"Saída: {output_dir}")
    print(f"Formato: MP3 ({bitrate})")
    print("=" * 72)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)

        for midi_path in midi_files:
            source_midi = midi_path

            if program is not None:
                source_midi = temp_dir / f"program_{midi_path.name}"
                set_program(midi_path, source_midi, program)

            wav_path = temp_dir / f"{midi_path.stem}.wav"
            mp3_path = output_dir / f"{midi_path.stem}.mp3"

            print(f"Sintetizando: {midi_path.name}")

            render_wav(
                source_midi,
                wav_path,
                soundfont,
                sample_rate,
            )

            convert_to_mp3(
                wav_path,
                mp3_path,
                bitrate,
            )

            print(f"Gerado: {mp3_path.relative_to(ROOT)}")


def main():
    args = parse_arguments()

    if shutil.which("fluidsynth") is None:
        raise SystemExit(
            "FluidSynth não foi encontrado no PATH.\n"
            "Confirme com: fluidsynth --version"
        )

    if shutil.which("ffmpeg") is None:
        raise SystemExit(
            "FFmpeg não foi encontrado no PATH.\n"
            "Confirme com: ffmpeg -version"
        )

    if not INPUT_DIR.exists():
        raise SystemExit(f"Pasta não encontrada: {INPUT_DIR}")

    midi_files = get_midi_files()

    if not midi_files:
        raise SystemExit(f"Nenhum MIDI encontrado em: {INPUT_DIR}")

    selected = (
        {args.only: SOUNDFONTS[args.only]}
        if args.only
        else SOUNDFONTS
    )

    print(f"MIDIs encontrados: {len(midi_files)}")
    if args.program is None:
        print("Preset: mantendo o program original dos MIDIs")
    else:
        print(f"Preset: program {args.program}")

    for name, config in selected.items():
        soundfont = find_soundfont(config["filename"])
        render_collection(
            name=name,
            output_folder=config["output_folder"],
            soundfont=soundfont,
            midi_files=midi_files,
            program=args.program,
            sample_rate=args.sample_rate,
            bitrate=args.bitrate,
        )


if __name__ == "__main__":
    main()
