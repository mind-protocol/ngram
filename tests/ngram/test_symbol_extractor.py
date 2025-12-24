"""
Tests for Symbol Extraction

Tests the symbol extraction functionality:
- Python AST parsing
- Symbol node creation
- Link creation (contains, calls, imports)
- Test inference
- Docs linking

DOCS: docs/cli/symbols/PATTERNS_Symbol_Extraction.md
"""

import pytest
import tempfile
import os
from pathlib import Path

from ngram.symbol_extractor import (
    PythonExtractor,
    TestInferrer,
    DocsLinker,
    SymbolExtractor,
    ExtractedSymbol,
    ExtractedLink,
    slugify,
    calculate_complexity,
    get_docstring_first_line,
    get_signature,
)


# =============================================================================
# UTILITY FUNCTION TESTS
# =============================================================================

class TestSlugify:
    """Test the slugify utility function."""

    def test_basic_path(self):
        assert slugify("engine/physics/tick.py") == "engine-physics-tick-py"

    def test_underscores(self):
        assert slugify("my_module.py") == "my-module-py"

    def test_special_chars(self):
        assert slugify("file@name!.py") == "filename-py"

    def test_multiple_hyphens(self):
        assert slugify("a--b---c") == "a-b-c"

    def test_leading_trailing(self):
        assert slugify("/path/to/file/") == "path-to-file"


class TestComplexity:
    """Test cyclomatic complexity calculation."""

    def test_simple_function(self):
        import ast
        code = """
def simple():
    return 1
"""
        tree = ast.parse(code)
        func = tree.body[0]
        assert calculate_complexity(func) == 1

    def test_if_statement(self):
        import ast
        code = """
def with_if(x):
    if x:
        return 1
    return 0
"""
        tree = ast.parse(code)
        func = tree.body[0]
        assert calculate_complexity(func) == 2

    def test_multiple_branches(self):
        import ast
        code = """
def branches(x, y):
    if x:
        return 1
    elif y:
        return 2
    for i in range(10):
        pass
    return 0
"""
        tree = ast.parse(code)
        func = tree.body[0]
        assert calculate_complexity(func) == 4  # 1 + if + elif + for


class TestDocstring:
    """Test docstring extraction."""

    def test_first_line(self):
        docstring = """This is the first line.

        More details here.
        """
        assert get_docstring_first_line(docstring) == "This is the first line."

    def test_empty(self):
        assert get_docstring_first_line("") == ""
        assert get_docstring_first_line(None) == ""


# =============================================================================
# PYTHON EXTRACTOR TESTS
# =============================================================================

class TestPythonExtractor:
    """Test Python AST extraction."""

    @pytest.fixture
    def temp_project(self):
        """Create a temporary project with Python files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)

            # Create source file
            src = base / "engine" / "module.py"
            src.parent.mkdir(parents=True)
            src.write_text('''"""Module docstring."""

CONSTANT_VALUE = 42

def public_function(x: int, y: str = "default") -> bool:
    """Public function docstring."""
    return True

def _private_function():
    pass

class MyClass:
    """Class docstring."""

    def __init__(self):
        pass

    def method(self, arg):
        """Method docstring."""
        return arg

    def _private_method(self):
        pass
''')

            yield base

    def test_extracts_file(self, temp_project):
        extractor = PythonExtractor(temp_project)
        symbols, links = extractor.extract_file(temp_project / "engine" / "module.py")

        file_symbols = [s for s in symbols if s.type == "file"]
        assert len(file_symbols) == 1
        assert file_symbols[0].name == "module.py"
        assert file_symbols[0].description == "Module docstring."

    def test_extracts_functions(self, temp_project):
        extractor = PythonExtractor(temp_project)
        symbols, links = extractor.extract_file(temp_project / "engine" / "module.py")

        funcs = [s for s in symbols if s.type == "func"]
        assert len(funcs) == 2

        public = next(f for f in funcs if f.name == "public_function")
        assert public.is_public is True
        assert "x: int" in public.signature
        assert "-> bool" in public.signature

        private = next(f for f in funcs if f.name == "_private_function")
        assert private.is_public is False

    def test_extracts_class(self, temp_project):
        extractor = PythonExtractor(temp_project)
        symbols, links = extractor.extract_file(temp_project / "engine" / "module.py")

        classes = [s for s in symbols if s.type == "class"]
        assert len(classes) == 1
        assert classes[0].name == "MyClass"
        assert classes[0].method_count == 3

    def test_extracts_methods(self, temp_project):
        extractor = PythonExtractor(temp_project)
        symbols, links = extractor.extract_file(temp_project / "engine" / "module.py")

        methods = [s for s in symbols if s.type == "method"]
        assert len(methods) == 3  # __init__, method, _private_method

        public_method = next(m for m in methods if m.name == "method")
        assert public_method.is_public is True

    def test_extracts_constants(self, temp_project):
        extractor = PythonExtractor(temp_project)
        symbols, links = extractor.extract_file(temp_project / "engine" / "module.py")

        consts = [s for s in symbols if s.type == "const"]
        assert len(consts) == 1
        assert consts[0].name == "CONSTANT_VALUE"
        assert consts[0].value == "42"

    def test_creates_contains_links(self, temp_project):
        extractor = PythonExtractor(temp_project)
        symbols, links = extractor.extract_file(temp_project / "engine" / "module.py")

        contains_links = [l for l in links if l.type == "contains"]
        # file -> 2 funcs, file -> 1 class, file -> 1 const, class -> 3 methods
        assert len(contains_links) == 7


class TestPythonExtractorCalls:
    """Test call relationship extraction."""

    @pytest.fixture
    def call_project(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            src = base / "module.py"
            src.write_text('''
def helper():
    return 1

def main():
    helper()
    helper()
    return 0
''')
            yield base

    def test_extracts_calls(self, call_project):
        extractor = PythonExtractor(call_project)
        symbols, links = extractor.extract_file(call_project / "module.py")

        calls = [l for l in links if l.direction == "calls"]
        assert len(calls) == 1
        assert calls[0].call_count == 2


# =============================================================================
# TEST INFERENCE TESTS
# =============================================================================

class TestTestInferrer:
    """Test the test-to-source inference logic."""

    @pytest.fixture
    def symbols_for_inference(self):
        """Create symbols for inference testing."""
        return [
            ExtractedSymbol(
                id="thing_FUNC_engine-module-py_calculate",
                node_type="thing",
                type="func",
                name="calculate",
                description="",
                uri="engine/module.py::calculate",
                line_start=10, line_end=15, lines=6,
            ),
            ExtractedSymbol(
                id="thing_FUNC_tests-test-module-py_test-calculate",
                node_type="thing",
                type="func",
                name="test_calculate",
                description="",
                uri="tests/test_module.py::test_calculate",
                line_start=5, line_end=10, lines=6,
            ),
            ExtractedSymbol(
                id="thing_FILE_engine-module-py",
                node_type="thing",
                type="file",
                name="module.py",
                description="",
                uri="engine/module.py",
                line_start=1, line_end=100, lines=100,
            ),
        ]

    def test_naming_convention(self, symbols_for_inference, tmp_path):
        inferrer = TestInferrer(tmp_path)
        links = inferrer.infer_test_links(symbols_for_inference, [])

        naming_links = [l for l in links if l.inference == "naming"]
        assert len(naming_links) == 1
        assert "test-calculate" in naming_links[0].node_a
        assert "calculate" in naming_links[0].node_b


# =============================================================================
# DOCS LINKER TESTS
# =============================================================================

class TestDocsLinker:
    """Test documentation linking."""

    @pytest.fixture
    def docs_project(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)

            # Create docs
            docs = base / "docs" / "engine"
            docs.mkdir(parents=True)
            (docs / "IMPLEMENTATION_Engine.md").write_text('''
# Implementation

The `run_tick` function handles the main loop.

See engine/physics.py for details.
''')

            yield base

    def test_finds_narrative_docs(self, docs_project):
        linker = DocsLinker(docs_project)
        narratives = linker._find_narrative_docs(docs_project / "docs")
        assert len(narratives) == 1
        assert "IMPLEMENTATION_Engine.md" in list(narratives.keys())[0]

    def test_links_code_references(self, docs_project):
        linker = DocsLinker(docs_project)

        symbols = [
            ExtractedSymbol(
                id="thing_FUNC_engine-physics-py_run-tick",
                node_type="thing",
                type="func",
                name="run_tick",
                description="",
                uri="engine/physics.py::run_tick",
                line_start=1, line_end=10, lines=10,
            ),
        ]

        links = linker.link_docs(symbols)
        doc_links = [l for l in links if l.direction == "documented_by"]
        assert len(doc_links) >= 1


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestSymbolExtractor:
    """Integration tests for the full extraction pipeline."""

    def test_dry_run_extraction(self):
        """Test extraction without database."""
        from ngram.symbol_extractor import extract_symbols_command

        # Run dry-run on actual codebase
        result = extract_symbols_command(
            directory="ngram",
            graph_name=None,
            dry_run=True
        )

        assert result.files > 0
        assert result.symbols > 0
        assert result.links > 0

    def test_extraction_result_fields(self):
        """Test that extraction returns all expected fields."""
        from ngram.symbol_extractor import extract_symbols_command

        result = extract_symbols_command(
            directory="ngram",
            dry_run=True
        )

        assert hasattr(result, 'files')
        assert hasattr(result, 'symbols')
        assert hasattr(result, 'links')
        assert hasattr(result, 'errors')
        assert hasattr(result, 'extracted_files')
