"""Главный модуль программы."""

import argparse
import sys
import parser

def parse_args():
    """Разбирает аргументы командной строки."""
    desc = "Визуализатор графа зависимостей (Вариант 8)"
    p = argparse.ArgumentParser(description=desc)
    
    p.add_argument("--package", required=True, help="Имя пакета")
    p.add_argument("--repo", required=True, help="Путь к VFS или URL")
    p.add_argument("--test-mode", action="store_true", help="Тест")
    p.add_argument("--version", default="latest", help="Версия")
    p.add_argument("--output", default="graph.png", help="Файл")
    p.add_argument("--ascii", action="store_true", help="ASCII вывод")
    p.add_argument("--depth", type=int, default=3, help="Глубина")
    p.add_argument("--filter", default="", help="Фильтр")

    args = p.parse_args()
    
    if args.depth < 1:
        print("Ошибка: Глубина > 0.")
        sys.exit(1)
        
    if args.test_mode and args.repo.startswith("http"):
        print("Ошибка: В тесте нужен файл, а не URL.")
        sys.exit(1)
        
    if not args.test_mode and not args.repo.startswith("http"):
        print("Ошибка: Нужен URL.")
        sys.exit(1)
    return args

def print_config(args):
    """Печатает параметры."""
    print("\nПараметры:")
    print(f"package: {args.package}")
    print(f"repo:    {args.repo}")
    print(f"test:    {args.test_mode}")
    print(f"version: {args.version}")
    print(f"output:  {args.output}")
    print(f"ascii:   {args.ascii}")
    print(f"depth:   {args.depth}")
    f_val = args.filter if args.filter else "(пусто)"
    print(f"filter:  {f_val}")

def run_stage_2(args):
    """Выполняет Этап 2."""
    print("\nЭТАП 2: Сбор данных")
    deps = parser.get_dependencies(
        args.package, args.version, args.test_mode, args.repo
    )
    if deps:
        print(f"Зависимости ({len(deps)} шт.):")
        for d in deps:
            print(f" - {d}")
    else:
        print("Нет зависимостей.")

def run_stages_3_4(args):
    """Выполняет Этапы 3 и 4."""
    print("\nЭТАП 3: Граф")
    graph = parser.build_graph(
        args.package, args.depth, args.test_mode, args.repo, args.filter
    )
    print(f"Узлов: {len(graph)}")
    
    print("\nЭТАП 4: Порядок")
    order = parser.get_install_order(graph)
    for i, pkg in enumerate(order, 1):
        print(f" {i}. {pkg}")
    return graph

def run_stage_5(args, graph):
    """Выполняет Этап 5."""
    print("\nЭТАП 5: Визуализация")
    code = parser.generate_mermaid(graph)
    print("Mermaid код:")
    print(code)
    parser.save_png_from_mermaid(code, args.output)
    if args.ascii:
        parser.print_ascii_tree(graph, args.package)

def main():
    """Точка входа."""
    print("ЭТАП 1: Конфигурация")
    args = parse_args()
    print_config(args)
    
    run_stage_2(args)
    graph = run_stages_3_4(args)
    run_stage_5(args, graph)

if __name__ == "__main__":
    main()