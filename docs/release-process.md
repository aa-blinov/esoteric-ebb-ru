# Release process / Процесс релиза

## English

The repository uses semantic versions. The localization archive contains the
twelve CSV files under `Russian/`; release builds do not contain the pipeline,
game assets or local work files.

### Choose a version

- **Patch** (`1.0.1`): proofreading, terminology, layout and documentation
  fixes that do not add a new language or change the package format.
- **Minor** (`1.1.0`): a substantial new content pass or a notable addition
  that remains compatible with the existing installation.
- **Major** (`2.0.0`): a change that breaks the package layout or installation
  instructions.

### Publish

1. Merge the reviewed pull request to `main` after `Check and test` and
   `House style` pass.
2. Move the release entries from `Unreleased` to a dated version section in
   `CHANGELOG.md`; write matching Russian notes in `docs/releases/vX.Y.Z.md`.
3. Update the archive links in both READMEs for the new version.
4. Push an annotated tag named `vX.Y.Z` at the release commit. The release
   workflow runs tests, packages the twelve CSV files, and publishes the
   matching release notes and ZIP archive.
5. Verify that the workflow succeeded and that the release has the expected
   archive before announcing it.

Do not reuse a published tag. If a release build fails, fix the cause in a new
commit and use a new version; do not move the tag.

## Русский

В проекте используется семантическая версия. В архив попадают двенадцать CSV
из папки `Russian/`; пайплайн, игровые ресурсы и локальные рабочие файлы в него
не входят.

### Как выбрать версию

- **Patch** (`1.0.1`): вычитка, термины, вёрстка и документация без смены
  формата пакета и появления нового языка.
- **Minor** (`1.1.0`): большой новый этап перевода или заметное совместимое
  улучшение.
- **Major** (`2.0.0`): несовместимое изменение структуры архива или установки.

### Как выпустить

1. Влей проверенный pull request в `main` после успешных `Check and test` и
   `House style`.
2. Перенеси готовые записи из `Unreleased` в датированный раздел
   `CHANGELOG.md` и создай русские заметки `docs/releases/vX.Y.Z.md`.
3. Обнови ссылки на архив в обоих README.
4. Отправь аннотированный тег `vX.Y.Z` на коммит релиза. Workflow проверит
   тесты, соберёт архив из двенадцати CSV и опубликует заметки и ZIP.
5. Убедись, что workflow завершился успешно и в релизе лежит нужный архив,
   прежде чем объявлять о выпуске.

Не используй опубликованный тег повторно. Если сборка релиза сломалась,
исправь причину новым коммитом и выпусти новую версию; не передвигай тег.
