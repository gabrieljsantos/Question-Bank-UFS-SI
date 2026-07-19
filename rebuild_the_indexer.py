import json
import re
import sys
from pathlib import Path


INDEX_FILE = "index.json"
METADATA_FILE = "metadata.json"
QUESTIONS_FOLDER = "questions"


def sanitize_folder_part(value: str) -> str:
    value = value.strip()
    value = re.sub(r"[^\w.-]+", "_", value, flags=re.UNICODE)
    value = re.sub(r"_+", "_", value)
    return value.strip("._-")


def build_folder_name(metadata: dict) -> str:
    required = [
        "id",
        "tag",
        "discipline",
        "discipline_code",
        "term",
        "assessment",
    ]

    missing = [
        key
        for key in required
        if str(metadata.get(key, "")).strip() == ""
    ]

    if missing:
        raise ValueError(
            "Metadados incompletos: " + ", ".join(missing)
        )

    try:
        assessment = int(metadata["assessment"])
    except (TypeError, ValueError) as error:
        raise ValueError(
            'O campo "assessment" deve ser um número inteiro.'
        ) from error

    return (
        f"{sanitize_folder_part(str(metadata['discipline']))}_"
        f"{sanitize_folder_part(str(metadata['discipline_code']))}_"
        f"{sanitize_folder_part(str(metadata['term']))}_"
        f"A{assessment}_"
        f"{sanitize_folder_part(str(metadata['tag']))}_"
        f"ID-{sanitize_folder_part(str(metadata['id']))}"
    )


def rebuild_bank(base_directory: Path | str | None = None) -> dict:
    if base_directory is None:
        base_directory = Path(__file__).resolve().parent
    else:
        base_directory = Path(base_directory).expanduser().resolve()

    if not base_directory.is_dir():
        raise NotADirectoryError(
            f"A pasta base não existe: {base_directory}"
        )

    questions_root = base_directory / QUESTIONS_FOLDER
    questions_root.mkdir(parents=True, exist_ok=True)

    index_path = questions_root / INDEX_FILE

    registered_folders: list[str] = []
    renamed: list[tuple[str, str]] = []
    ignored: list[str] = []
    errors: list[str] = []

    candidate_folders = sorted(
        [
            path
            for path in questions_root.iterdir()
            if path.is_dir()
        ],
        key=lambda path: path.name.casefold(),
    )

    for folder_path in candidate_folders:
        metadata_path = folder_path / METADATA_FILE

        if not metadata_path.is_file():
            ignored.append(folder_path.name)
            continue

        try:
            with metadata_path.open("r", encoding="utf-8") as file:
                metadata = json.load(file)

            if not isinstance(metadata, dict):
                raise ValueError(
                    "metadata.json não contém um objeto JSON"
                )

            expected_name = build_folder_name(metadata)
            expected_path = questions_root / expected_name

            if folder_path.name != expected_name:
                if expected_path.exists():
                    raise FileExistsError(
                        f"já existe uma pasta chamada {expected_name}"
                    )

                old_name = folder_path.name
                folder_path.rename(expected_path)
                folder_path = expected_path
                renamed.append((old_name, expected_name))

            registered_folders.append(folder_path.name)

        except Exception as error:
            errors.append(f"{folder_path.name}: {error}")

    registered_folders.sort(key=str.casefold)

    index_data = {
        "folders": registered_folders,
    }

    with index_path.open("w", encoding="utf-8") as file:
        json.dump(
            index_data,
            file,
            ensure_ascii=False,
            indent=4,
        )
        file.write("\n")

    return {
        "registered": registered_folders,
        "renamed": renamed,
        "ignored": ignored,
        "errors": errors,
        "index_path": str(index_path),
    }


def main() -> int:
    base_directory = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path(__file__).resolve().parent
    )

    try:
        result = rebuild_bank(base_directory)
    except Exception as error:
        print(f"Erro ao reconstruir banco: {error}")
        return 1

    print(f"Index atualizado: {result['index_path']}")
    print(f"Questões registradas: {len(result['registered'])}")
    print(f"Pastas renomeadas: {len(result['renamed'])}")
    print(f"Pastas ignoradas: {len(result['ignored'])}")

    for old_name, new_name in result["renamed"]:
        print(f"  {old_name} -> {new_name}")

    if result["errors"]:
        print("Erros encontrados:")

        for error in result["errors"]:
            print(f"  - {error}")

        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
