from pathlib import Path
import subprocess
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "_data" / "cv.yml"
BUILD_DIR = ROOT / "_build"
PDF_DIR = ROOT / "assets"
PDF_FILE = PDF_DIR / "cv.pdf"


def plain_text(value):
    """Προστασία ειδικών χαρακτήρων στη μορφή Markdown."""
    text = " ".join(str(value).split())
    for character in "\\`*_{}[]<>#!|":
        text = text.replace(character, "\\" + character)
    return text


def main():
    data = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError("Το cv.yml πρέπει να περιέχει πεδία βιογραφικού.")

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        "# " + plain_text(data["name"]),
        "",
        plain_text(data["headline"]),
        "",
    ]

    sections = [
        ("education", "Σπουδές"),
        ("experience", "Εργασιακή εμπειρία"),
        ("interests", "Ενδιαφέροντα"),
    ]

    for key, title in sections:
        items = data.get(key, [])
        if not isinstance(items, list):
            raise ValueError(f"Το πεδίο {key} πρέπει να είναι λίστα.")

        lines.extend(["## " + title, ""])
        for item in items:
            lines.append("- " + plain_text(item))
        lines.append("")

    markdown_file = BUILD_DIR / "cv.md"
    markdown_file.write_text("\n".join(lines), encoding="utf-8")

    subprocess.run(
        [
            "pandoc",
            str(markdown_file),
            "--from=markdown",
            "--standalone",
            "--pdf-engine=xelatex",
            "-V", "mainfont=DejaVu Sans",
            "-V", "papersize=a4",
            "-V", "geometry:margin=20mm",
            "-V", "fontsize=11pt",
            "-V", "pagestyle=empty",
            "--output", str(PDF_FILE),
        ],
        check=True,
    )

    print(f"Πηγή δεδομένων: {DATA_FILE}")
    print(f"Δημιουργήθηκε PDF: {PDF_FILE}")


if __name__ == "__main__":
    main()
