from __future__ import annotations

import re
from pathlib import Path


def leading_spaces(s: str) -> int:
    return len(s) - len(s.lstrip(" "))


def slugify(title: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", title.strip())
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "Tool"


def extract_block(lines: list[str], start_idx: int) -> tuple[list[str], int, int]:
    """Return (body_lines, base_indent, end_idx_exclusive)."""
    start_line = lines[start_idx]
    base_indent = leading_spaces(start_line)
    body: list[str] = []
    i = start_idx + 1
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == "":
            body.append("\n")
            i += 1
            continue
        if leading_spaces(ln) <= base_indent:
            break
        body.append(ln)
        i += 1
    return body, base_indent, i


def dedent(body: list[str], n: int) -> str:
    out: list[str] = []
    for ln in body:
        if ln.strip() == "":
            out.append("\n")
        else:
            out.append(ln[n:] if ln.startswith(" " * n) else ln.lstrip(" "))
    return "".join(out)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    app = repo_root / "app.py"
    pages = repo_root / "pages"
    pages.mkdir(exist_ok=True)

    text = app.read_text(encoding="utf-8")
    lines = text.splitlines(True)

    # Remove existing generated pages (keep __init__.py, if any).
    for p in pages.glob("*.py"):
        if p.name.startswith("__"):
            continue
        p.unlink()

    # Only scan inside main() for tool UI blocks.
    main_start = None
    for i, ln in enumerate(lines):
        if ln.startswith("def main():"):
            main_start = i
            break
    if main_start is None:
        raise SystemExit("Could not find def main():")

    # Determine end of main by next top-level def or EOF.
    main_end = len(lines)
    for i in range(main_start + 1, len(lines)):
        if lines[i].startswith("def ") and not lines[i].startswith("def main"):
            main_end = i
            break

    expander_re = re.compile(r"^\s*with\s+st\.expander\(\"([^\"]+)\"")
    container_re = re.compile(r"^\s*with\s+st\.container\(border=True\):\s*$")
    subheader_re = re.compile(r"^\s*st\.subheader\(\"([^\"]+)\"\)")

    blocks: list[tuple[str, str]] = []  # (title, body_code)

    idx = main_start
    while idx < main_end:
        ln = lines[idx]

        m = expander_re.match(ln)
        if m:
            title = m.group(1)
            body, base_indent, end = extract_block(lines, idx)
            body_code = dedent(body, base_indent + 4)
            blocks.append((title, body_code))
            idx = end
            continue

        if container_re.match(ln):
            body, base_indent, end = extract_block(lines, idx)
            title = None
            for b in body:
                sm = subheader_re.match(b)
                if sm:
                    title = sm.group(1)
                    break
            if title:
                body_code = dedent(body, base_indent + 4)
                blocks.append((title, body_code))
            idx = end
            continue

        idx += 1

    # De-duplicate by title (keep first occurrence).
    seen: set[str] = set()
    unique_blocks: list[tuple[str, str]] = []
    for title, code in blocks:
        if title in seen:
            continue
        if title == "Optional dependencies status":
            continue
        seen.add(title)
        unique_blocks.append((title, code))

    for i, (title, code) in enumerate(unique_blocks, start=1):
        fname = f"{i:02d}_{slugify(title)}.py"
        page = pages / fname
        content = (
            "import sys\n"
            "from pathlib import Path\n\n"
            "ROOT = Path(__file__).resolve().parents[1]\n"
            "root_str = str(ROOT)\n"
            "if sys.path[:1] != [root_str]:\n"
            "    if root_str in sys.path:\n"
            "        sys.path.remove(root_str)\n"
            "    sys.path.insert(0, root_str)\n\n"
            "import streamlit as st\n"
            "import importlib\n"
            "import importlib.util\n\n"
            "def _load_local_app():\n"
            "    app_path = (ROOT / 'app.py').resolve()\n"
            "    spec = importlib.util.spec_from_file_location('app', app_path)\n"
            "    if spec is None or spec.loader is None:\n"
            "        raise ImportError(f'Cannot load app.py from {app_path}')\n"
            "    module = importlib.util.module_from_spec(spec)\n"
            "    sys.modules['app'] = module\n"
            "    spec.loader.exec_module(module)\n"
            "    return module\n\n"
            "try:\n"
            "    import app as _app\n"
            "    _app_file = getattr(_app, '__file__', '')\n"
            "    if not _app_file or Path(_app_file).resolve() != (ROOT / 'app.py').resolve():\n"
            "        _app = _load_local_app()\n"
            "except Exception:\n"
            "    _app = _load_local_app()\n\n"
            "for _name in dir(_app):\n"
            "    if not _name.startswith('__'):\n"
            "        globals()[_name] = getattr(_app, _name)\n\n"
            "APP_TITLE = getattr(_app, 'APP_TITLE', 'PDF & Image Tools')\n"
            f"st.set_page_config(page_title=f\"{{APP_TITLE}} - {title}\", layout=\"wide\")\n"
            "if st.button(\"← Home\"):\n"
            "    st.switch_page(\"app.py\")\n\n"
            f"st.title(\"{title}\")\n\n"
            "deps = get_dependency_status()\n\n"
            + code
        )
        page.write_text(content, encoding="utf-8")

    print(f"Generated {len(unique_blocks)} tool pages in: {pages}")


if __name__ == "__main__":
    main()
