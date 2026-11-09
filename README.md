# dependency-graph
# Визуализатор графа зависимостей пакетов Python

Учебный проект по предмету «Конфигурационное управление».
Инструмент для анализа и визуализации зависимостей пакетов Python (PyPI).

**Вариант №8**

## Описание
Программа позволяет построить граф зависимостей для заданного пакета, обойти его алгоритмом DFS (без рекурсии), вывести правильный порядок установки (топологическая сортировка), а также сгенерировать визуализацию в формате Mermaid и PNG.

## Настройки и параметры командной строки
Программа поддерживает следующие аргументы:
- `--package` (обязательный) — имя анализируемого пакета.
- `--repo` (обязательный) — URL репозитория (например, `https://pypi.org`) или путь к локальному JSON-файлу.
- `--test-mode` — включает режим тестирования (чтение графа из локального файла).
- `--version` — версия пакета (по умолчанию `latest`).
- `--output` — имя файла для сохранения картинки (по умолчанию `graph.png`).
- `--ascii` — флаг для вывода дерева зависимостей в консоль.
- `--depth` — максимальная глубина анализа (по умолчанию `3`).
- `--filter` — подстрока для исключения пакетов из анализа.

## Команды для запуска

Для запуска используйте скрипт `run.sh` или Python напрямую:

```bash
# Запуск в тестовом режиме (из файла)
./run.sh --package A --repo test_data.json --test-mode --depth 2 --ascii

# Запуск в реальном режиме (из PyPI)
./run.sh --package requests --repo https://pypi.org --depth 2

**Общий запуск (демонстрация всех этапов сразу):**
```bash
python src/main.py --package A --repo test_data.json --test-mode --depth 3 --ascii --output result.png

**Этап 1. Проверка конфигурации и обработки ошибок: **
```bash
python src/main.py --package requests --repo https://pypi.org

*Этап 2. Сбор данных (из файла):**
```bash
python src/main.py --package A --repo test_data.json --test-mode

**Этап 3. Построение графа (DFS с глубиной и фильтром):**
```bash
python src/main.py --package A --repo test_data.json --test-mode --depth 2 --filter C

**Этап 4. Порядок загрузки (Топологическая сортировка):**
```bash
python src/main.py --package A --repo test_data.json --test-mode

**Этап 5. Визуализация (Mermaid + PNG + ASCII):
```bash
python src/main.py --package A --repo test_data.json --test-mode --ascii --output my_graph.png
