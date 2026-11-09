"""Модуль сбора данных и построения графа зависимостей."""

import json
import urllib.request
import urllib.error
import urllib.parse
import base64

HTTP_NOT_FOUND = 404

def get_dependencies(pkg, ver="latest", test=False, repo=""):
    """Возвращает список прямых зависимостей пакета."""
    if test:
        return get_deps_from_file(pkg, repo)
    return get_deps_from_web(pkg, ver)

def _clean_dep_name(raw_dep):
    """Очищает имя зависимости от версий."""
    clean = raw_dep.split(' ')[0].split('>')[0]
    clean = clean.split('<')[0].split('=')[0].strip()
    return clean

def get_deps_from_file(pkg, filepath):
    """Читает зависимости из JSON-файла."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if pkg not in data:
            print(f"Ошибка: Пакет '{pkg}' не найден.")
            return []
            
        deps = data[pkg].get("requires_dist", [])
        return [_clean_dep_name(d) for d in deps if _clean_dep_name(d)]
        
    except FileNotFoundError:
        print(f"Ошибка: Файл {filepath} не найден.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: Неверный JSON в {filepath}.")
        return []

def get_deps_from_web(pkg, ver="latest"):
    """Запрашивает зависимости у PyPI."""
    if ver == "latest":
        url = f"https://pypi.org/pypi/{pkg}/json"
    else:
        url = f"https://pypi.org/pypi/{pkg}/{ver}/json"
        
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        reqs = data.get("info", {}).get("requires_dist", [])
        if not reqs:
            return []
            
        clean_deps = []
        for dep in reqs:
            if ";" in dep:
                continue
            name = _clean_dep_name(dep)
            if name:
                clean_deps.append(name)
        return clean_deps
        
    except urllib.error.HTTPError as e:
        if e.code == HTTP_NOT_FOUND:
            print(f"Ошибка: Пакет '{pkg}' не найден.")
        else:
            print(f"Ошибка сети: {e.code}")
        return []
    except urllib.error.URLError:
        print("Ошибка: Нет интернета.")
        return []

def build_graph(start_pkg, max_depth, test=False, repo="", flt=""):
    """Строит граф зависимостей (DFS без рекурсии)."""
    stack = [(start_pkg, 0)]
    graph = {}
    visited = set()
    
    while stack:
        curr, depth = stack.pop()
        
        if curr in visited or depth >= max_depth:
            continue
        if flt and flt in curr:
            continue
            
        visited.add(curr)
        deps = get_dependencies(curr, "latest", test, repo)
        graph[curr] = deps
        
        for d in deps:
            if d not in visited:
                stack.append((d, depth + 1))
    return graph

def get_install_order(graph):
    """Выполняет топологическую сортировку."""
    visited = set()
    order = []
    
    for start in graph:
        if start in visited:
            continue
        stack = [(start, False)]
        
        while stack:
            node, processed = stack.pop()
            
            if processed:
                if node not in order:
                    order.append(node)
                continue
            if node in visited:
                continue
                
            visited.add(node)
            stack.append((node, True))
            
            for dep in reversed(graph.get(node, [])):
                if dep in graph and dep not in visited:
                    stack.append((dep, False))
    return order

def generate_mermaid(graph):
    """Генерирует код Mermaid для графа."""
    lines = ["graph TD"]
    for pkg, deps in graph.items():
        if not deps:
            lines.append(f"    {pkg}")
        for dep in deps:
            lines.append(f"    {pkg} --> {dep}")
    return "\n".join(lines)

def save_png_from_mermaid(text, path):
    """Сохраняет PNG из mermaid.ink."""
    encoded = base64.urlsafe_b64encode(text.encode('utf-8'))
    encoded_str = encoded.decode('ascii')
    url = f"https://mermaid.ink/img/{encoded_str}?type=png"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(path, 'wb') as f:
                f.write(response.read())
        print(f"Сохранено: {path}")
    except Exception as e:
        print(f"Ошибка картинки: {e}")

def print_ascii_tree(graph, start):
    """Выводит ASCII-дерево."""
    print(f"\nДерево для '{start}':")
    
    def _print_node(node, prefix="", is_last=True):
        conn = "└── " if is_last else "├── "
        print(f"{prefix}{conn}{node}")
        
        deps = graph.get(node, [])
        new_pref = prefix + ("    " if is_last else "│   ")
        
        for i, dep in enumerate(deps):
            _print_node(dep, new_pref, i == len(deps) - 1)
    _print_node(start)