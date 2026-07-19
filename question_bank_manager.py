import json
import re
import sys
import uuid
from pathlib import Path
from rebuild_the_indexer import rebuild_bank

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


INDEX_FILE = "index.json"
METADATA_FILE = "metadata.json"
QUESTIONS_FOLDER = "questions"
QUESTION_FILE = "question.md"


def sanitize_folder_part(value: str) -> str:
    value = value.strip()
    value = re.sub(r"[^\w.-]+", "_", value, flags=re.UNICODE)
    value = re.sub(r"_+", "_", value)
    return value.strip("._-")


class QuestionBankManager(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.root_directory: Path = Path(__file__).resolve().parent
        self.index_data: dict = {
            "folders": [],
        }

        self.selected_folder_name: str | None = None
        self.selected_question_id: str | None = None

        self.setWindowTitle("Gerenciador de Banco de Questões")
        self.resize(940, 780)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        folder_layout = QHBoxLayout()

        self.root_label = QLabel("Nenhuma pasta selecionada")
        self.root_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        select_root_button = QPushButton("Selecionar pasta do banco")
        select_root_button.clicked.connect(self.select_root_directory)

        rebuild_button = QPushButton("Reconstruir indexador")
        rebuild_button.clicked.connect(self.rebuild_index)

        folder_layout.addWidget(self.root_label, 1)
        folder_layout.addWidget(select_root_button)
        folder_layout.addWidget(rebuild_button)

        main_layout.addLayout(folder_layout)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.build_create_tab(), "Criar questão")
        self.tabs.addTab(self.build_edit_tab(), "Editar questão")

        main_layout.addWidget(self.tabs)

        self.open_root_directory(self.root_directory)

    @staticmethod
    def create_editable_combo() -> QComboBox:
        combo = QComboBox()
        combo.setEditable(True)
        combo.setInsertPolicy(QComboBox.NoInsert)
        return combo

    def build_create_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        form = QFormLayout()

        self.create_contributor = self.create_editable_combo()
        self.create_discipline = self.create_editable_combo()
        self.create_discipline_code = self.create_editable_combo()
        self.create_professor = self.create_editable_combo()
        self.create_term = self.create_editable_combo()

        self.create_assessment = QSpinBox()
        self.create_assessment.setRange(1, 99)
        self.create_assessment.setValue(1)

        self.create_tag = QLineEdit()
        self.create_tag.setPlaceholderText(
            "Exemplo: rotacao_simples_avl"
        )

        self.create_contents = QTextEdit()
        self.create_contents.setPlaceholderText(
            "Digite um conteúdo por linha"
        )
        self.create_contents.setFixedHeight(110)

        self.create_answer_count = QSpinBox()
        self.create_answer_count.setRange(0, 99)
        self.create_answer_count.setValue(0)

        form.addRow("Colaborador:", self.create_contributor)
        form.addRow("Disciplina:", self.create_discipline)
        form.addRow("Código da disciplina:", self.create_discipline_code)
        form.addRow("Professor:", self.create_professor)
        form.addRow("Período:", self.create_term)
        form.addRow("Avaliação:", self.create_assessment)
        form.addRow("Tag da questão:", self.create_tag)
        form.addRow("Conteúdos:", self.create_contents)
        form.addRow("Quantidade inicial de respostas:", self.create_answer_count)

        layout.addLayout(form)

        self.create_preview = QLabel()
        self.create_preview.setWordWrap(True)
        self.create_preview.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.create_preview.setStyleSheet(
            "padding: 10px; border: 1px solid #888; border-radius: 4px;"
        )

        layout.addWidget(self.create_preview)

        create_button = QPushButton("Criar questão")
        create_button.clicked.connect(self.create_question)

        layout.addWidget(create_button, alignment=Qt.AlignRight)

        self.create_discipline.currentTextChanged.connect(
            self.update_create_preview
        )
        self.create_discipline_code.currentTextChanged.connect(
            self.update_create_preview
        )
        self.create_term.currentTextChanged.connect(
            self.update_create_preview
        )
        self.create_assessment.valueChanged.connect(
            self.update_create_preview
        )
        self.create_tag.textChanged.connect(
            self.update_create_preview
        )

        self.update_create_preview()

        return tab

    def build_edit_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        list_layout = QHBoxLayout()

        self.question_list = QListWidget()
        self.question_list.currentItemChanged.connect(
            self.load_selected_question
        )

        refresh_button = QPushButton("Atualizar lista")
        refresh_button.clicked.connect(self.refresh_question_list)

        list_layout.addWidget(self.question_list, 1)
        list_layout.addWidget(refresh_button, alignment=Qt.AlignTop)

        layout.addLayout(list_layout)

        form = QFormLayout()

        self.edit_id = QLineEdit()
        self.edit_id.setReadOnly(True)

        self.edit_contributor = self.create_editable_combo()
        self.edit_discipline = self.create_editable_combo()
        self.edit_discipline_code = self.create_editable_combo()
        self.edit_professor = self.create_editable_combo()
        self.edit_term = self.create_editable_combo()

        self.edit_assessment = QSpinBox()
        self.edit_assessment.setRange(1, 99)

        self.edit_tag = QLineEdit()

        self.edit_contents = QTextEdit()
        self.edit_contents.setPlaceholderText(
            "Digite um conteúdo por linha"
        )
        self.edit_contents.setFixedHeight(100)

        form.addRow("ID:", self.edit_id)
        form.addRow("Colaborador:", self.edit_contributor)
        form.addRow("Disciplina:", self.edit_discipline)
        form.addRow("Código da disciplina:", self.edit_discipline_code)
        form.addRow("Professor:", self.edit_professor)
        form.addRow("Período:", self.edit_term)
        form.addRow("Avaliação:", self.edit_assessment)
        form.addRow("Tag da questão:", self.edit_tag)
        form.addRow("Conteúdos:", self.edit_contents)

        layout.addLayout(form)

        answers_layout = QHBoxLayout()

        self.answer_list = QListWidget()

        answer_buttons = QVBoxLayout()

        add_answer_button = QPushButton("+ Adicionar resposta")
        add_answer_button.clicked.connect(self.add_answer)

        remove_answer_button = QPushButton("- Remover resposta")
        remove_answer_button.clicked.connect(self.remove_answer)

        answer_buttons.addWidget(add_answer_button)
        answer_buttons.addWidget(remove_answer_button)
        answer_buttons.addStretch()

        answers_layout.addWidget(self.answer_list, 1)
        answers_layout.addLayout(answer_buttons)

        layout.addLayout(answers_layout)

        self.edit_preview = QLabel("Selecione uma questão.")
        self.edit_preview.setWordWrap(True)
        self.edit_preview.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.edit_preview.setStyleSheet(
            "padding: 10px; border: 1px solid #888; border-radius: 4px;"
        )

        layout.addWidget(self.edit_preview)

        save_button = QPushButton("Salvar alterações")
        save_button.clicked.connect(self.save_question_changes)

        layout.addWidget(save_button, alignment=Qt.AlignRight)

        self.edit_discipline.currentTextChanged.connect(
            self.update_edit_preview
        )
        self.edit_discipline_code.currentTextChanged.connect(
            self.update_edit_preview
        )
        self.edit_term.currentTextChanged.connect(
            self.update_edit_preview
        )
        self.edit_assessment.valueChanged.connect(
            self.update_edit_preview
        )
        self.edit_tag.textChanged.connect(
            self.update_edit_preview
        )

        return tab

    def select_root_directory(self) -> None:
        selected = QFileDialog.getExistingDirectory(
            self,
            "Selecionar pasta do banco de questões",
            str(self.root_directory),
        )

        if not selected:
            return

        self.open_root_directory(Path(selected))

    def open_root_directory(self, directory: Path) -> None:
        self.root_directory = directory.resolve()
        self.root_label.setText(str(self.root_directory))
        (self.root_directory / QUESTIONS_FOLDER).mkdir(parents=True, exist_ok=True)

        try:
            self.load_or_create_index()
            self.populate_suggestions()
            self.refresh_question_list()
        except Exception as error:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível abrir o banco de questões.\n\n{error}",
            )

    def rebuild_index(self) -> None:
        try:
            result = rebuild_bank(self.root_directory)
            self.load_or_create_index()
            self.populate_suggestions()
            self.refresh_question_list()
        except Exception as error:
            QMessageBox.critical(
                self,
                "Erro ao reconstruir",
                f"Não foi possível reconstruir o indexador.\n\n{error}",
            )
            return

        renamed_lines = [
            f"- {old_name} -> {new_name}"
            for old_name, new_name in result["renamed"]
        ]
        error_lines = [
            f"- {error}"
            for error in result["errors"]
        ]

        details = [
            f"Questões registradas: {len(result['registered'])}",
            f"Pastas renomeadas: {len(result['renamed'])}",
            f"Pastas ignoradas: {len(result['ignored'])}",
        ]

        if renamed_lines:
            details.extend(["", "Renomeações:", *renamed_lines])

        if error_lines:
            details.extend(["", "Erros encontrados:", *error_lines])

        message = "\n".join(details)

        if result["errors"]:
            QMessageBox.warning(
                self,
                "Indexador reconstruído com avisos",
                message,
            )
        else:
            QMessageBox.information(
                self,
                "Indexador reconstruído",
                message,
            )

    def load_or_create_index(self) -> None:
        if self.root_directory is None:
            return

        index_path = self.root_directory / QUESTIONS_FOLDER / INDEX_FILE

        if not index_path.exists():
            self.index_data = {
                "folders": [],
            }
            self.save_index()
            return

        with index_path.open("r", encoding="utf-8") as file:
            loaded_data = json.load(file)

        if not isinstance(loaded_data, dict):
            raise ValueError("O index.json deve conter um objeto JSON.")

        folders = loaded_data.get("folders", [])

        if not isinstance(folders, list):
            raise ValueError('O campo "folders" deve ser uma lista.')

        self.index_data = {
            "folders": [
                str(folder)
                for folder in folders
                if str(folder).strip()
            ],
        }


    def save_index(self) -> None:
        if self.root_directory is None:
            raise ValueError("Nenhuma pasta do banco foi selecionada.")

        index_path = self.root_directory / QUESTIONS_FOLDER / INDEX_FILE

        with index_path.open("w", encoding="utf-8") as file:
            json.dump(
                self.index_data,
                file,
                ensure_ascii=False,
                indent=4,
            )
            file.write("\n")

    def read_metadata(self, folder_name: str) -> dict:
        if self.root_directory is None:
            raise ValueError("Nenhuma pasta do banco foi selecionada.")

        metadata_path = (
            self.root_directory
            / QUESTIONS_FOLDER
            / folder_name
            / METADATA_FILE
        )

        with metadata_path.open("r", encoding="utf-8") as file:
            metadata = json.load(file)

        if not isinstance(metadata, dict):
            raise ValueError(
                f"O arquivo {metadata_path} não contém um objeto JSON."
            )

        return metadata

    def write_metadata(
        self,
        folder_path: Path,
        metadata: dict,
    ) -> None:
        metadata_path = folder_path / METADATA_FILE

        with metadata_path.open("w", encoding="utf-8") as file:
            json.dump(
                metadata,
                file,
                ensure_ascii=False,
                indent=4,
            )
            file.write("\n")

    def populate_suggestions(self) -> None:
        metadata_list = []

        for folder_name in self.index_data.get("folders", []):
            try:
                metadata_list.append(
                    self.read_metadata(folder_name)
                )
            except Exception:
                continue

        mappings = [
            (
                self.create_contributor,
                self.edit_contributor,
                "contributor",
            ),
            (
                self.create_discipline,
                self.edit_discipline,
                "discipline",
            ),
            (
                self.create_discipline_code,
                self.edit_discipline_code,
                "discipline_code",
            ),
            (
                self.create_professor,
                self.edit_professor,
                "professor",
            ),
            (
                self.create_term,
                self.edit_term,
                "term",
            ),
        ]

        for create_combo, edit_combo, key in mappings:
            values = sorted(
                {
                    str(metadata.get(key, "")).strip()
                    for metadata in metadata_list
                    if str(metadata.get(key, "")).strip()
                },
                key=str.casefold,
            )

            for combo in (create_combo, edit_combo):
                current_text = combo.currentText()

                combo.blockSignals(True)
                combo.clear()
                combo.addItems(values)
                combo.setCurrentText(current_text)
                combo.blockSignals(False)

    def build_folder_name(
        self,
        discipline: str,
        discipline_code: str,
        term: str,
        assessment: int,
        tag: str,
        question_id: str,
    ) -> str:
        return (
            f"{sanitize_folder_part(discipline)}_"
            f"{sanitize_folder_part(discipline_code)}_"
            f"{sanitize_folder_part(term)}_"
            f"A{assessment}_"
            f"{sanitize_folder_part(tag)}_"
            f"ID-{question_id}"
        )

    def update_create_preview(self) -> None:
        folder_name = self.build_folder_name(
            self.create_discipline.currentText(),
            self.create_discipline_code.currentText(),
            self.create_term.currentText(),
            self.create_assessment.value(),
            self.create_tag.text(),
            "xxxx",
        )

        self.create_preview.setText(
            "Prévia do nome da pasta:\n"
            f"{folder_name}"
        )

    def update_edit_preview(self) -> None:
        if not self.edit_id.text():
            self.edit_preview.setText("Selecione uma questão.")
            return

        folder_name = self.build_folder_name(
            self.edit_discipline.currentText(),
            self.edit_discipline_code.currentText(),
            self.edit_term.currentText(),
            self.edit_assessment.value(),
            self.edit_tag.text(),
            self.edit_id.text(),
        )

        self.edit_preview.setText(
            "Ao salvar, a pasta será renomeada automaticamente para:\n"
            f"{folder_name}"
        )

    def generate_short_id(self) -> str:
        existing_ids = set()

        for folder_name in self.index_data.get("folders", []):
            try:
                metadata = self.read_metadata(folder_name)
                existing_ids.add(
                    str(metadata.get("id", "")).lower()
                )
            except Exception:
                continue

        while True:
            short_id = uuid.uuid4().hex[:4]

            if short_id not in existing_ids:
                return short_id

    @staticmethod
    def validate_required(values: dict[str, str]) -> list[str]:
        return [
            label
            for label, value in values.items()
            if not value.strip()
        ]

    def create_question(self) -> None:
        if self.root_directory is None:
            QMessageBox.warning(
                self,
                "Pasta necessária",
                "Selecione primeiro a pasta do banco de questões.",
            )
            return

        required_values = {
            "Colaborador": self.create_contributor.currentText(),
            "Disciplina": self.create_discipline.currentText(),
            "Código da disciplina": (
                self.create_discipline_code.currentText()
            ),
            "Professor": self.create_professor.currentText(),
            "Período": self.create_term.currentText(),
            "Tag": self.create_tag.text(),
        }

        missing_fields = self.validate_required(required_values)

        if missing_fields:
            QMessageBox.warning(
                self,
                "Campos obrigatórios",
                "Preencha os seguintes campos:\n\n"
                + "\n".join(
                    f"- {field}"
                    for field in missing_fields
                ),
            )
            return

        question_id = self.generate_short_id()

        folder_name = self.build_folder_name(
            self.create_discipline.currentText(),
            self.create_discipline_code.currentText(),
            self.create_term.currentText(),
            self.create_assessment.value(),
            self.create_tag.text(),
            question_id,
        )

        (self.root_directory / QUESTIONS_FOLDER).mkdir(parents=True, exist_ok=True)
        folder_path = self.root_directory / QUESTIONS_FOLDER / folder_name

        if folder_path.exists():
            QMessageBox.critical(
                self,
                "Pasta já existente",
                f"A pasta já existe:\n{folder_name}",
            )
            return

        answer_count = self.create_answer_count.value()

        answer_files = [
            f"answer_{number:02d}.md"
            for number in range(1, answer_count + 1)
        ]

        metadata = {
            "id": question_id,
            "contributor": (
                self.create_contributor.currentText().strip()
            ),
            "tag": self.create_tag.text().strip(),
            "discipline": (
                self.create_discipline.currentText().strip()
            ),
            "discipline_code": (
                self.create_discipline_code.currentText().strip()
            ),
            "professor": (
                self.create_professor.currentText().strip()
            ),
            "term": self.create_term.currentText().strip(),
            "assessment": self.create_assessment.value(),
            "contents": [
                line.strip()
                for line in (
                    self.create_contents
                    .toPlainText()
                    .splitlines()
                )
                if line.strip()
            ],
            "files": {
                "question": QUESTION_FILE,
                "answers": answer_files,
            },
        }

        try:
            folder_path.mkdir()
            (folder_path / QUESTION_FILE).touch()

            for answer_file in answer_files:
                (folder_path / answer_file).touch()

            self.write_metadata(folder_path, metadata)

            self.index_data["folders"].append(folder_name)
            self.index_data["folders"].sort(key=str.casefold)

            self.save_index()

        except Exception as error:
            if folder_path.exists():
                for child in folder_path.iterdir():
                    if child.is_file():
                        child.unlink()

                folder_path.rmdir()

            QMessageBox.critical(
                self,
                "Erro ao criar",
                f"Não foi possível criar a questão.\n\n{error}",
            )
            return

        self.populate_suggestions()
        self.refresh_question_list()

        QMessageBox.information(
            self,
            "Questão criada",
            "Questão criada com sucesso.\n\n"
            f"Pasta: {folder_name}",
        )

    def refresh_question_list(self) -> None:
        self.question_list.clear()

        for folder_name in self.index_data.get("folders", []):
            try:
                metadata = self.read_metadata(folder_name)
            except Exception:
                continue

            label = (
                f'{metadata.get("tag", "sem_tag")} | '
                f'{metadata.get("discipline", "")} | '
                f'ID-{metadata.get("id", "")}'
            )

            self.question_list.addItem(label)

            item = self.question_list.item(
                self.question_list.count() - 1
            )

            item.setData(Qt.UserRole, folder_name)

    def load_selected_question(self, current, previous) -> None:
        if current is None:
            return

        folder_name = current.data(Qt.UserRole)

        try:
            metadata = self.read_metadata(folder_name)
        except Exception as error:
            QMessageBox.critical(
                self,
                "Erro ao abrir questão",
                str(error),
            )
            return

        self.selected_folder_name = folder_name
        self.selected_question_id = str(metadata.get("id", ""))

        self.edit_id.setText(self.selected_question_id)
        self.edit_contributor.setCurrentText(
            str(metadata.get("contributor", ""))
        )
        self.edit_discipline.setCurrentText(
            str(metadata.get("discipline", ""))
        )
        self.edit_discipline_code.setCurrentText(
            str(metadata.get("discipline_code", ""))
        )
        self.edit_professor.setCurrentText(
            str(metadata.get("professor", ""))
        )
        self.edit_term.setCurrentText(
            str(metadata.get("term", ""))
        )
        self.edit_assessment.setValue(
            int(metadata.get("assessment", 1))
        )
        self.edit_tag.setText(
            str(metadata.get("tag", ""))
        )
        self.edit_contents.setPlainText(
            "\n".join(metadata.get("contents", []))
        )

        self.answer_list.clear()

        for answer_file in (
            metadata
            .get("files", {})
            .get("answers", [])
        ):
            self.answer_list.addItem(
                Path(answer_file).name
            )

        self.update_edit_preview()

    def add_answer(self) -> None:
        if self.selected_folder_name is None:
            QMessageBox.warning(
                self,
                "Questão necessária",
                "Selecione uma questão primeiro.",
            )
            return

        existing_files = {
            self.answer_list.item(index).text()
            for index in range(self.answer_list.count())
        }

        number = 1

        while f"answer_{number:02d}.md" in existing_files:
            number += 1

        self.answer_list.addItem(
            f"answer_{number:02d}.md"
        )

    def remove_answer(self) -> None:
        selected_item = self.answer_list.currentItem()

        if selected_item is None:
            return

        confirmation = QMessageBox.question(
            self,
            "Remover resposta",
            "O arquivo da resposta será excluído ao salvar. Continuar?",
        )

        if confirmation == QMessageBox.Yes:
            row = self.answer_list.row(selected_item)
            self.answer_list.takeItem(row)

    def save_question_changes(self) -> None:
        if (
            self.root_directory is None
            or self.selected_folder_name is None
            or self.selected_question_id is None
        ):
            QMessageBox.warning(
                self,
                "Questão necessária",
                "Selecione uma questão primeiro.",
            )
            return

        required_values = {
            "Colaborador": self.edit_contributor.currentText(),
            "Disciplina": self.edit_discipline.currentText(),
            "Código da disciplina": (
                self.edit_discipline_code.currentText()
            ),
            "Professor": self.edit_professor.currentText(),
            "Período": self.edit_term.currentText(),
            "Tag": self.edit_tag.text(),
        }

        missing_fields = self.validate_required(required_values)

        if missing_fields:
            QMessageBox.warning(
                self,
                "Campos obrigatórios",
                "Preencha os seguintes campos:\n\n"
                + "\n".join(
                    f"- {field}"
                    for field in missing_fields
                ),
            )
            return

        old_folder_name = self.selected_folder_name
        old_folder_path = self.root_directory / QUESTIONS_FOLDER / old_folder_name

        new_folder_name = self.build_folder_name(
            self.edit_discipline.currentText(),
            self.edit_discipline_code.currentText(),
            self.edit_term.currentText(),
            self.edit_assessment.value(),
            self.edit_tag.text(),
            self.selected_question_id,
        )

        new_folder_path = self.root_directory / QUESTIONS_FOLDER / new_folder_name

        if (
            old_folder_name != new_folder_name
            and new_folder_path.exists()
        ):
            QMessageBox.critical(
                self,
                "Erro ao renomear",
                "Já existe uma pasta com o novo nome:\n"
                f"{new_folder_name}",
            )
            return

        try:
            old_metadata = self.read_metadata(old_folder_name)
        except Exception as error:
            QMessageBox.critical(
                self,
                "Erro ao ler metadados",
                str(error),
            )
            return

        old_answer_files = {
            Path(answer).name
            for answer in (
                old_metadata
                .get("files", {})
                .get("answers", [])
            )
        }

        desired_answer_files = [
            self.answer_list.item(index).text()
            for index in range(self.answer_list.count())
        ]

        desired_answer_set = set(desired_answer_files)

        try:
            if old_folder_name != new_folder_name:
                old_folder_path.rename(new_folder_path)
            else:
                new_folder_path = old_folder_path

            for answer_file in (
                desired_answer_set - old_answer_files
            ):
                (new_folder_path / answer_file).touch()

            for answer_file in (
                old_answer_files - desired_answer_set
            ):
                answer_path = new_folder_path / answer_file

                if answer_path.exists():
                    answer_path.unlink()

            metadata = {
                "id": self.selected_question_id,
                "contributor": (
                    self.edit_contributor.currentText().strip()
                ),
                "tag": self.edit_tag.text().strip(),
                "discipline": (
                    self.edit_discipline.currentText().strip()
                ),
                "discipline_code": (
                    self.edit_discipline_code
                    .currentText()
                    .strip()
                ),
                "professor": (
                    self.edit_professor.currentText().strip()
                ),
                "term": self.edit_term.currentText().strip(),
                "assessment": self.edit_assessment.value(),
                "contents": [
                    line.strip()
                    for line in (
                        self.edit_contents
                        .toPlainText()
                        .splitlines()
                    )
                    if line.strip()
                ],
                "files": {
                    "question": QUESTION_FILE,
                    "answers": desired_answer_files,
                },
            }

            self.write_metadata(new_folder_path, metadata)

            updated_folders = []

            for folder_name in self.index_data["folders"]:
                if folder_name == old_folder_name:
                    updated_folders.append(new_folder_name)
                else:
                    updated_folders.append(folder_name)

            self.index_data["folders"] = sorted(
                set(updated_folders),
                key=str.casefold,
            )

            self.save_index()

            self.selected_folder_name = new_folder_name

        except Exception as error:
            QMessageBox.critical(
                self,
                "Erro ao salvar",
                "Não foi possível salvar as alterações.\n\n"
                f"{error}",
            )
            return

        self.populate_suggestions()
        self.refresh_question_list()

        QMessageBox.information(
            self,
            "Alterações salvas",
            "Os metadados foram atualizados, a pasta foi renomeada "
            "automaticamente e o indexador externo foi sincronizado.",
        )


def main() -> None:
    app = QApplication(sys.argv)

    window = QuestionBankManager()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()