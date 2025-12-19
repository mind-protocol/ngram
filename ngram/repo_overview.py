# DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md
"""
Repository Overview Generator.

Generates a comprehensive map of the repository including:
- File hierarchy tree (respecting .gitignore and .ngramignore)
- Section titles (# and ##) for markdown files
- Function/class definitions for code files
- Dependency map from modules.yaml

Output formats: markdown, yaml, json
"""

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from .doctor_files import (
    load_doctor_config,
    should_ignore_path,
    is_binary_file,
)
from .project_map import analyze_modules, load_modules_yaml
from .context import parse_imports
from .utils import IGNORED_EXTENSIONS

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class FileInfo:
    """Information about a single file."""
    path: str
    type: str  # 'file' or 'dir'
    language: str = ""
    chars: int = 0  # characters in this file (for files)
    total_chars: int = 0  # total chars including all children (for dirs)
    docs_ref: str = ""  # DOCS: reference path (code → docs link)
    code_refs: List[str] = field(default_factory=list)  # Code file references (docs → code link)
    doc_refs: List[str] = field(default_factory=list)  # Doc file references (docs → docs link)
    imports: List[str] = field(default_factory=list)  # import/dependency paths
    sections: List[str] = field(default_factory=list)  # # and ## headers for md
    functions: List[str] = field(default_factory=list)  # function/class names
    children: List["FileInfo"] = field(default_factory=list)


@dataclass
class DependencyInfo:
    """Module dependency information."""
    name: str
    code_pattern: str
    docs_path: str
    depends_on: List[str]
    lines: int
    files: int


@dataclass
class RepoOverview:
    """Complete repository overview."""
    project_name: str
    generated_at: str
    file_tree: FileInfo
    dependencies: List[DependencyInfo]
    stats: Dict[str, Any]


def get_language(file_path: Path) -> str:
    """Determine language from file extension."""
    ext_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'tsx',
        '.jsx': 'jsx',
        '.go': 'go',
        '.rs': 'rust',
        '.java': 'java',
        '.rb': 'ruby',
        '.php': 'php',
        '.c': 'c',
        '.cpp': 'cpp',
        '.h': 'c-header',
        '.md': 'markdown',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.json': 'json',
        '.toml': 'toml',
        '.sh': 'shell',
        '.bash': 'shell',
        '.css': 'css',
        '.scss': 'scss',
        '.html': 'html',
    }
    return ext_map.get(file_path.suffix.lower(), '')


def extract_docs_ref(file_path: Path) -> str:
    """Extract DOCS: reference from file header (bidirectional link).

    Looks for patterns like:
    - Python: # DOCS: docs/path/to/PATTERNS_*.md
    - JS/TS: // DOCS: docs/path/to/PATTERNS_*.md
    - C-style: /* DOCS: docs/path/to/PATTERNS_*.md */
    - In docstrings: DOCS: docs/path/to/PATTERNS_*.md
    """
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return ""

    # Only search in first 2000 chars (file header)
    header = content[:2000]

    # Pattern to match DOCS: references in various comment styles
    patterns = [
        r'#\s*DOCS:\s*([^\n]+)',      # Python style
        r'//\s*DOCS:\s*([^\n]+)',     # JS/C++ style
        r'/\*\s*DOCS:\s*([^\n*]+)',   # C-style block comment
        r'^\s*DOCS:\s*([^\n]+)',      # In docstrings (no comment marker)
    ]

    for pattern in patterns:
        match = re.search(pattern, header, re.MULTILINE)
        if match:
            return match.group(1).strip()

    return ""


def extract_markdown_sections(file_path: Path) -> List[str]:
    """Extract # and ## section titles from markdown file."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return []

    sections = []
    for line in content.split('\n'):
        # Match # and ## headers (not ### or deeper)
        match = re.match(r'^(#{1,2})\s+(.+)$', line.strip())
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            prefix = '#' * level
            sections.append(f"{prefix} {title}")

    return sections


def extract_markdown_code_refs(file_path: Path) -> List[str]:
    """Extract code file references from markdown files (docs → code direction)."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return []

    refs = set()

    # Pattern 1: Backtick code references like `ngram/cli.py` or `cli.py`
    backtick_refs = re.findall(r'`((?:src/)?[a-zA-Z_][\w/]*\.(?:py|js|ts|tsx|jsx|go|rs|java))`', content)
    refs.update(backtick_refs)

    # Pattern 2: Markdown links to code files [text](path/to/file.py)
    link_refs = re.findall(r'\]\(([^)]*\.(?:py|js|ts|tsx|jsx|go|rs|java))\)', content)
    refs.update(link_refs)

    # Pattern 3: Explicit CODE: or IMPL: markers
    code_markers = re.findall(r'(?:CODE|IMPL):\s*`?([^\s`\n]+\.(?:py|js|ts|tsx|jsx|go|rs|java))`?', content)
    refs.update(code_markers)

    # Pattern 4: Table cells with src/ paths like | `ngram/cli.py` | or | ngram/cli.py |
    table_refs = re.findall(r'\|\s*`?(src/[a-zA-Z_][\w/]*\.(?:py|js|ts|tsx|jsx|go|rs|java))`?\s*\|', content)
    refs.update(table_refs)

    # Clean up paths (remove ../ prefixes, normalize)
    cleaned = []
    for ref in refs:
        # Remove leading ../ or ./
        ref = re.sub(r'^(?:\.\./)+', '', ref)
        ref = re.sub(r'^\./', '', ref)
        if ref:
            cleaned.append(ref)

    return sorted(set(cleaned))


def extract_markdown_doc_refs(file_path: Path) -> List[str]:
    """Extract doc file references from markdown files (docs → docs cross-links).

    Only includes cross-folder references - skips same-folder siblings (chain links).
    """
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return []

    refs = set()

    # Pattern 1: Markdown links to other docs [text](path/to/DOC.md) - only with path
    link_refs = re.findall(r'\]\(([^)]+/[^)]*\.md)\)', content)
    refs.update(link_refs)

    # Pattern 2: Backtick doc references with paths like `docs/cli/SYNC.md`
    backtick_refs = re.findall(r'`([a-z][a-z0-9_/]*[A-Z][A-Z_]*[^`]*\.md)`', content)
    refs.update(backtick_refs)

    # Clean up paths (remove ../ prefixes, normalize)
    cleaned = []
    for ref in refs:
        # Remove leading ../ or ./
        ref = re.sub(r'^(?:\.\./)+', '', ref)
        ref = re.sub(r'^\./', '', ref)
        # Skip self-references, anchors, and same-folder refs (no / means same folder)
        if ref and not ref.startswith('#') and '/' in ref and ref != file_path.name:
            cleaned.append(ref)

    return sorted(set(cleaned))


def extract_code_definitions(file_path: Path) -> List[str]:
    """Extract function and class definitions from code files."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return []

    definitions = []
    suffix = file_path.suffix.lower()

    if suffix == '.py':
        # Python: def, class, async def
        pattern = re.compile(r'^(?:async\s+)?(?:def|class)\s+(\w+)')
        for line in content.split('\n'):
            line = line.strip()
            match = pattern.match(line)
            if match:
                name = match.group(1)
                if line.startswith('class'):
                    definitions.append(f"class {name}")
                elif 'async def' in line:
                    definitions.append(f"async def {name}()")
                else:
                    definitions.append(f"def {name}()")

    elif suffix in ['.js', '.ts', '.jsx', '.tsx']:
        # JavaScript/TypeScript
        patterns = [
            (re.compile(r'^(?:export\s+)?(?:async\s+)?function\s+(\w+)'), 'function'),
            (re.compile(r'^(?:export\s+)?class\s+(\w+)'), 'class'),
            (re.compile(r'^(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\('), 'const'),
            (re.compile(r'^(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?function'), 'const'),
        ]
        for line in content.split('\n'):
            line = line.strip()
            for pattern, kind in patterns:
                match = pattern.match(line)
                if match:
                    name = match.group(1)
                    if kind == 'class':
                        definitions.append(f"class {name}")
                    else:
                        definitions.append(f"{name}()")
                    break

    elif suffix == '.go':
        # Go: func, type
        func_pattern = re.compile(r'^func\s+(?:\([^)]+\)\s+)?(\w+)')
        type_pattern = re.compile(r'^type\s+(\w+)\s+(?:struct|interface)')
        for line in content.split('\n'):
            line = line.strip()
            match = func_pattern.match(line)
            if match:
                definitions.append(f"func {match.group(1)}()")
                continue
            match = type_pattern.match(line)
            if match:
                definitions.append(f"type {match.group(1)}")

    elif suffix == '.rs':
        # Rust: fn, struct, impl, enum
        patterns = [
            (re.compile(r'^(?:pub\s+)?(?:async\s+)?fn\s+(\w+)'), 'fn'),
            (re.compile(r'^(?:pub\s+)?struct\s+(\w+)'), 'struct'),
            (re.compile(r'^(?:pub\s+)?enum\s+(\w+)'), 'enum'),
            (re.compile(r'^impl(?:<[^>]+>)?\s+(\w+)'), 'impl'),
        ]
        for line in content.split('\n'):
            line = line.strip()
            for pattern, kind in patterns:
                match = pattern.match(line)
                if match:
                    name = match.group(1)
                    if kind == 'fn':
                        definitions.append(f"fn {name}()")
                    else:
                        definitions.append(f"{kind} {name}")
                    break

    elif suffix in ['.java', '.kt']:
        # Java/Kotlin: class, interface, method
        class_pattern = re.compile(r'^(?:public\s+)?(?:abstract\s+)?(?:class|interface)\s+(\w+)')
        method_pattern = re.compile(r'^(?:public|private|protected)?\s*(?:static\s+)?(?:\w+\s+)+(\w+)\s*\(')
        for line in content.split('\n'):
            line = line.strip()
            match = class_pattern.match(line)
            if match:
                definitions.append(f"class {match.group(1)}")
                continue
            match = method_pattern.match(line)
            if match and match.group(1) not in ['if', 'for', 'while', 'switch']:
                definitions.append(f"{match.group(1)}()")

    return definitions


def count_chars(file_path: Path) -> int:
    """Count characters in a file."""
    try:
        return file_path.stat().st_size
    except Exception:
        return 0


# Python stdlib modules (partial list of common ones)
_STDLIB_MODULES = {
    'abc', 'asyncio', 'argparse', 'ast', 'base64', 'bisect', 'builtins',
    'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs',
    'codeop', 'collections', 'colorsys', 'compileall', 'concurrent',
    'configparser', 'contextlib', 'contextvars', 'copy', 'copyreg', 'cProfile',
    'crypt', 'csv', 'ctypes', 'curses', 'dataclasses', 'datetime', 'dbm',
    'decimal', 'difflib', 'dis', 'distutils', 'doctest', 'email', 'encodings',
    'enum', 'errno', 'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch',
    'fractions', 'ftplib', 'functools', 'gc', 'getopt', 'getpass', 'gettext',
    'glob', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http',
    'imaplib', 'imghdr', 'imp', 'importlib', 'inspect', 'io', 'ipaddress',
    'itertools', 'json', 'keyword', 'lib2to3', 'linecache', 'locale', 'logging',
    'lzma', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap',
    'modulefinder', 'multiprocessing', 'netrc', 'nis', 'nntplib', 'numbers',
    'operator', 'optparse', 'os', 'ossaudiodev', 'pathlib', 'pdb', 'pickle',
    'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib', 'poplib',
    'posix', 'posixpath', 'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile',
    'pyclbr', 'pydoc', 'queue', 'quopri', 'random', 're', 'readline', 'reprlib',
    'resource', 'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors',
    'shelve', 'shlex', 'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr',
    'socket', 'socketserver', 'spwd', 'sqlite3', 'ssl', 'stat', 'statistics',
    'string', 'stringprep', 'struct', 'subprocess', 'sunau', 'symtable', 'sys',
    'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile',
    'termios', 'test', 'textwrap', 'threading', 'time', 'timeit', 'tkinter',
    'token', 'tokenize', 'trace', 'traceback', 'tracemalloc', 'tty', 'turtle',
    'turtledemo', 'types', 'typing', 'unicodedata', 'unittest', 'urllib', 'uu',
    'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'winreg',
    'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile',
    'zipimport', 'zlib', '_thread',
}

# Node.js built-ins and common npm packages to exclude
_NODE_MODULES = {
    # Node.js built-ins
    'assert', 'buffer', 'child_process', 'cluster', 'console', 'constants',
    'crypto', 'dgram', 'dns', 'domain', 'events', 'fs', 'http', 'https',
    'module', 'net', 'os', 'path', 'perf_hooks', 'process', 'punycode',
    'querystring', 'readline', 'repl', 'stream', 'string_decoder', 'timers',
    'tls', 'tty', 'url', 'util', 'v8', 'vm', 'worker_threads', 'zlib',
    # Next.js / React
    'next', 'react', 'react-dom', 'next/router', 'next/link', 'next/image',
    'next/head', 'next/script', 'next/navigation', 'next/headers',
    '@next/font', '@next/mdx',
    # Common npm packages
    'axios', 'lodash', 'moment', 'dayjs', 'date-fns', 'uuid', 'nanoid',
    'express', 'fastify', 'koa', 'hapi',
    'prisma', '@prisma/client', 'mongoose', 'sequelize', 'typeorm', 'knex',
    'zod', 'yup', 'joi', 'ajv',
    'tailwindcss', 'styled-components', '@emotion/react', '@emotion/styled',
    'clsx', 'classnames', 'class-variance-authority',
    'zustand', 'jotai', 'recoil', 'redux', '@reduxjs/toolkit', 'mobx',
    'swr', '@tanstack/react-query', 'react-query',
    'framer-motion', 'react-spring', '@react-spring/web',
    '@radix-ui', '@headlessui/react', '@chakra-ui/react', '@mui/material',
    'lucide-react', 'react-icons', '@heroicons/react',
    'typescript', 'tslib', '@types',
    'eslint', 'prettier', 'jest', 'vitest', '@testing-library',
    'webpack', 'vite', 'esbuild', 'rollup', 'parcel', 'turbopack',
}


def _filter_local_imports(imports: List[str], target_dir: Path) -> List[str]:
    """Filter imports to only keep local/custom ones (not stdlib or third-party)."""
    result = []
    # Get project package name from src/ or project root
    src_dir = target_dir / "src"
    project_packages = set()
    if src_dir.exists():
        for item in src_dir.iterdir():
            if item.is_dir() and not item.name.startswith('_'):
                project_packages.add(item.name)

    for imp in imports:
        # Get root module name (first part before /)
        root = imp.split('/')[0]

        # Skip Python stdlib
        if root in _STDLIB_MODULES:
            continue

        # Skip Node.js/npm packages (check both root and full path for scoped packages)
        if root in _NODE_MODULES or imp in _NODE_MODULES:
            continue
        # Skip @scoped packages
        if root.startswith('@'):
            continue

        # Include if it matches project package or starts with . (relative)
        if root in project_packages or imp.startswith('.'):
            result.append(imp)

    return result


def build_file_tree(
    target_dir: Path,
    config,
    current_path: Optional[Path] = None,
    depth: int = 0,
    max_depth: int = 10
) -> Optional[FileInfo]:
    """Build file tree recursively."""
    if current_path is None:
        current_path = target_dir

    if depth > max_depth:
        return None

    # Skip ignored paths
    if should_ignore_path(current_path, config.ignore, target_dir):
        return None

    # Get relative path
    try:
        rel_path = str(current_path.relative_to(target_dir))
    except ValueError:
        rel_path = str(current_path)

    if rel_path == '.':
        rel_path = current_path.name

    if current_path.is_file():
        # Skip binary and ignored extensions
        if current_path.suffix.lower() in IGNORED_EXTENSIONS:
            return None
        if is_binary_file(current_path):
            return None

        language = get_language(current_path)
        chars = count_chars(current_path)

        # Extract docs_ref and imports for code files
        docs_ref = ""
        imports = []
        sections = []
        functions = []

        code_refs = []
        doc_refs = []
        if language == 'markdown':
            sections = extract_markdown_sections(current_path)
            code_refs = extract_markdown_code_refs(current_path)
            doc_refs = extract_markdown_doc_refs(current_path)
        elif language in ['python', 'javascript', 'typescript', 'tsx', 'jsx', 'go', 'rust', 'java']:
            functions = extract_code_definitions(current_path)
            docs_ref = extract_docs_ref(current_path)
            raw_imports = parse_imports(current_path)
            # Filter to only local imports (not stdlib/third-party)
            imports = _filter_local_imports(raw_imports, target_dir)

        return FileInfo(
            path=rel_path,
            type='file',
            language=language,
            chars=chars,
            docs_ref=docs_ref,
            code_refs=code_refs,
            doc_refs=doc_refs,
            imports=imports,
            sections=sections,
            functions=functions,
        )

    elif current_path.is_dir():
        # Skip hidden directories and common non-code directories
        if current_path.name.startswith('.') and current_path != target_dir:
            return None

        skip_dirs = {'__pycache__', 'node_modules', '.venv', 'venv', 'dist', 'build', '.git'}
        if current_path.name in skip_dirs:
            return None

        children = []
        for child in sorted(current_path.iterdir()):
            child_info = build_file_tree(target_dir, config, child, depth + 1, max_depth)
            if child_info:
                children.append(child_info)

        # Don't include empty directories
        if not children and current_path != target_dir:
            return None

        # Calculate total chars for directory (sum of all children)
        total_chars = 0
        for child in children:
            if child.type == 'file':
                total_chars += child.chars
            else:
                total_chars += child.total_chars

        return FileInfo(
            path=rel_path,
            type='dir',
            total_chars=total_chars,
            children=children,
        )

    return None


def get_dependency_info(target_dir: Path) -> List[DependencyInfo]:
    """Get dependency information from modules.yaml."""
    modules = analyze_modules(target_dir)

    deps = []
    for m in modules:
        deps.append(DependencyInfo(
            name=m.name,
            code_pattern=m.code_pattern,
            docs_path=m.docs_path,
            depends_on=m.depends_on,
            lines=m.total_lines,
            files=len(m.code_files),
        ))

    return deps


def count_tree_stats(tree: FileInfo) -> Dict[str, Any]:
    """Count statistics from file tree."""
    stats = {
        'total_files': 0,
        'total_dirs': 0,
        'total_chars': 0,
        'doc_files': 0,
        'code_files': 0,
        'link_count': 0,
        'by_language': {},
    }

    def traverse(node: FileInfo):
        if node.type == 'file':
            stats['total_files'] += 1
            stats['total_chars'] += node.chars
            if node.language:
                stats['by_language'][node.language] = stats['by_language'].get(node.language, 0) + 1
                if node.language == 'markdown':
                    stats['doc_files'] += 1
                else:
                    stats['code_files'] += 1
                    # Count files with DOCS: references
                    if node.docs_ref:
                        stats['link_count'] += 1
        elif node.type == 'dir':
            stats['total_dirs'] += 1
            for child in node.children:
                traverse(child)

    traverse(tree)

    # Calculate average links per code file
    if stats['code_files'] > 0:
        stats['avg_links_per_file'] = round(stats['link_count'] / stats['code_files'], 2)
    else:
        stats['avg_links_per_file'] = 0

    return stats


def count_docs_structure(target_dir: Path) -> Dict[str, int]:
    """Count areas and modules from docs/ folder structure.

    Areas = direct subfolders of docs/ (excluding concepts, map files)
    Modules = subfolders within areas
    """
    docs_dir = target_dir / "docs"
    if not docs_dir.exists():
        return {'areas': 0, 'modules': 0}

    areas = 0
    modules = 0

    for item in docs_dir.iterdir():
        if not item.is_dir():
            continue
        if item.name in ('concepts', '__pycache__'):
            continue

        # This is an area
        areas += 1

        # Count modules (subfolders within area)
        for subitem in item.iterdir():
            if subitem.is_dir() and not subitem.name.startswith('.'):
                modules += 1

    return {'areas': areas, 'modules': modules}


def generate_repo_overview(target_dir: Path) -> RepoOverview:
    """Generate complete repository overview."""
    from datetime import datetime

    config = load_doctor_config(target_dir)

    # Build file tree
    file_tree = build_file_tree(target_dir, config)
    if not file_tree:
        file_tree = FileInfo(path=target_dir.name, type='dir')

    # Get dependencies
    dependencies = get_dependency_info(target_dir)

    # Calculate stats
    stats = count_tree_stats(file_tree)

    # Count areas and modules from docs/ structure
    docs_stats = count_docs_structure(target_dir)
    stats['areas'] = docs_stats['areas']
    stats['modules'] = docs_stats['modules']

    return RepoOverview(
        project_name=target_dir.name,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        file_tree=file_tree,
        dependencies=dependencies,
        stats=stats,
    )


def file_info_to_dict(info: FileInfo) -> Dict[str, Any]:
    """Convert FileInfo to dict, handling nested structures."""
    result = {
        'path': info.path,
        'type': info.type,
    }
    if info.language:
        result['language'] = info.language
    if info.chars:
        result['chars'] = info.chars
    if info.total_chars:
        result['total_chars'] = info.total_chars
    if info.docs_ref:
        result['docs_ref'] = info.docs_ref
    if info.code_refs:
        result['code_refs'] = info.code_refs
    if info.doc_refs:
        result['doc_refs'] = info.doc_refs
    if info.imports:
        result['imports'] = info.imports
    if info.sections:
        result['sections'] = info.sections
    if info.functions:
        result['functions'] = info.functions
    if info.children:
        result['children'] = [file_info_to_dict(c) for c in info.children]
    return result


def overview_to_dict(overview: RepoOverview) -> Dict[str, Any]:
    """Convert RepoOverview to dict."""
    return {
        'project_name': overview.project_name,
        'generated_at': overview.generated_at,
        'stats': overview.stats,
        'dependencies': [asdict(d) for d in overview.dependencies],
        'file_tree': file_info_to_dict(overview.file_tree),
    }


def _format_size(chars: int) -> str:
    """Format character count with K/M suffix."""
    if chars >= 1_000_000:
        return f"{chars / 1_000_000:.1f}M"
    elif chars >= 1_000:
        return f"{chars / 1_000:.1f}K"
    else:
        return str(chars)


def format_markdown(overview: RepoOverview) -> str:
    """Format overview as markdown."""
    lines = []
    lines.append(f"# Repository Map: {overview.project_name}")
    lines.append("")
    lines.append(f"*Generated: {overview.generated_at}*")
    lines.append("")

    # Stats
    lines.append("## Statistics")
    lines.append("")
    lines.append(f"- **Files:** {overview.stats['total_files']}")
    lines.append(f"- **Directories:** {overview.stats['total_dirs']}")
    lines.append(f"- **Total Size:** {_format_size(overview.stats['total_chars'])}")
    lines.append(f"- **Doc Files:** {overview.stats.get('doc_files', 0)}")
    lines.append(f"- **Code Files:** {overview.stats.get('code_files', 0)}")
    lines.append(f"- **Areas:** {overview.stats.get('areas', 0)} (docs/ subfolders)")
    lines.append(f"- **Modules:** {overview.stats.get('modules', 0)} (subfolders in areas)")
    lines.append(f"- **DOCS Links:** {overview.stats.get('link_count', 0)} ({overview.stats.get('avg_links_per_file', 0)} avg per code file)")
    lines.append("")

    if overview.stats.get('by_language'):
        lines.append("### By Language")
        lines.append("")
        for lang, count in sorted(overview.stats['by_language'].items(), key=lambda x: -x[1]):
            lines.append(f"- {lang}: {count}")
        lines.append("")

    # Dependencies
    if overview.dependencies:
        lines.append("## Module Dependencies")
        lines.append("")
        lines.append("```mermaid")
        lines.append("graph TD")
        for dep in overview.dependencies:
            node_id = dep.name.replace('-', '_').replace('.', '_')
            lines.append(f"    {node_id}[{dep.name}]")
            for d in dep.depends_on:
                dep_id = d.replace('-', '_').replace('.', '_')
                lines.append(f"    {node_id} --> {dep_id}")
        lines.append("```")
        lines.append("")

        lines.append("### Module Details")
        lines.append("")
        lines.append("| Module | Code | Docs | Lines | Files | Dependencies |")
        lines.append("|--------|------|------|-------|-------|--------------|")
        for dep in overview.dependencies:
            deps_str = ', '.join(dep.depends_on) if dep.depends_on else '-'
            lines.append(f"| {dep.name} | `{dep.code_pattern}` | `{dep.docs_path}` | {dep.lines} | {dep.files} | {deps_str} |")
        lines.append("")

    # File tree
    lines.append("## File Tree")
    lines.append("")
    lines.append("```")

    def render_tree(node: FileInfo, prefix: str = "", is_last: bool = True):
        connector = "└── " if is_last else "├── "
        # Only show the basename, not full path
        name = Path(node.path).name
        if node.type == 'dir':
            # Show directory with total chars
            dir_info = f"{name}/"
            if node.total_chars:
                dir_info += f" ({_format_size(node.total_chars)})"
            lines.append(f"{prefix}{connector}{dir_info}")
            new_prefix = prefix + ("    " if is_last else "│   ")
            for i, child in enumerate(node.children):
                render_tree(child, new_prefix, i == len(node.children) - 1)
        else:
            info = name
            if node.chars:
                info += f" ({_format_size(node.chars)})"
            if node.docs_ref:
                info += " →"  # Arrow indicates has docs link
            lines.append(f"{prefix}{connector}{info}")

    # Start with root's children (not root itself)
    for i, child in enumerate(overview.file_tree.children):
        render_tree(child, "", i == len(overview.file_tree.children) - 1)

    lines.append("```")
    lines.append("")

    # File details with sections/functions
    lines.append("## File Details")
    lines.append("")

    def render_details(node: FileInfo, path_parts: List[str] = None):
        if path_parts is None:
            path_parts = []

        name = Path(node.path).name
        current_parts = path_parts + [name]

        if node.type == 'file':
            if node.sections or node.functions or node.docs_ref or node.code_refs or node.doc_refs or node.imports:
                full_path = "/".join(current_parts)
                lines.append(f"### `{full_path}`")
                lines.append("")
                if node.docs_ref:
                    lines.append(f"**Docs:** `{node.docs_ref}`")
                    lines.append("")
                if node.code_refs:
                    lines.append("**Code refs:**")
                    for ref in node.code_refs:
                        lines.append(f"- `{ref}`")
                    lines.append("")
                if node.doc_refs:
                    lines.append("**Doc refs:**")
                    for ref in node.doc_refs:
                        lines.append(f"- `{ref}`")
                    lines.append("")
                if node.imports:
                    lines.append("**Imports:**")
                    for imp in node.imports:
                        lines.append(f"- `{imp}`")
                    lines.append("")
                if node.sections:
                    lines.append("**Sections:**")
                    for s in node.sections:
                        lines.append(f"- {s}")
                    lines.append("")
                if node.functions:
                    lines.append("**Definitions:**")
                    for f in node.functions:
                        lines.append(f"- `{f}`")
                    lines.append("")
        elif node.type == 'dir':
            for child in node.children:
                render_details(child, current_parts)

    for child in overview.file_tree.children:
        render_details(child, [])

    return "\n".join(lines)


def format_yaml(overview: RepoOverview) -> str:
    """Format overview as YAML."""
    if not HAS_YAML:
        return "# YAML not available - install pyyaml"
    return yaml.dump(overview_to_dict(overview), default_flow_style=False, sort_keys=False)


def format_json(overview: RepoOverview) -> str:
    """Format overview as JSON."""
    return json.dumps(overview_to_dict(overview), indent=2)


def generate_and_save(target_dir: Path, output_format: str = "md") -> Path:
    """Generate overview and save to docs/map.{format}."""
    overview = generate_repo_overview(target_dir)

    # Ensure docs directory exists
    docs_dir = target_dir / "docs"
    docs_dir.mkdir(exist_ok=True)

    # Generate output
    if output_format == "yaml":
        content = format_yaml(overview)
        output_path = docs_dir / "map.yaml"
    elif output_format == "json":
        content = format_json(overview)
        output_path = docs_dir / "map.json"
    else:  # default to markdown
        content = format_markdown(overview)
        output_path = docs_dir / "map.md"

    output_path.write_text(content)
    return output_path


if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    fmt = sys.argv[2] if len(sys.argv) > 2 else "md"
    output = generate_and_save(target, fmt)
    print(f"Generated: {output}")
