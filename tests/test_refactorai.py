import pytest
from refactorai import (
    upload_codebase,
    train_model,
    generate_recommendations,
    Codebase,
    Analysis,
    FunctionInfo,
)


def test_upload_codebase_happy_path():
    files = {"a.py": "def foo():\n    pass"}
    cb = upload_codebase(files)
    assert isinstance(cb, Codebase)
    assert cb.files == files


def test_upload_codebase_invalid_type():
    with pytest.raises(TypeError):
        upload_codebase(["not", "a", "dict"])


def test_upload_codebase_invalid_content():
    with pytest.raises(ValueError):
        upload_codebase({1: "def foo():\n    pass"})


def test_train_model_extracts_functions():
    source = """
def short():
    return 1

def long():
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12
    m = 13
    n = 14
    o = 15
    p = 16
    q = 17
    r = 18
    s = 19
    t = 20
    u = 21
"""
    cb = upload_codebase({"mod.py": source})
    analysis = train_model(cb)

    assert isinstance(analysis, Analysis)
    assert "mod.py" in analysis.functions
    funcs = analysis.functions["mod.py"]
    names = {f.name for f in funcs}
    assert names == {"short", "long"}

    # Verify line counts (short should be 2 lines, long > 20)
    short_info = next(f for f in funcs if f.name == "short")
    long_info = next(f for f in funcs if f.name == "long")
    assert short_info.line_count == 2
    assert long_info.line_count > 20


def test_generate_recommendations_happy_path():
    # Build an analysis with one long function
    funcs = [FunctionInfo(name="big_one", line_count=30)]
    analysis = Analysis(functions={"file.py": funcs})

    recs = generate_recommendations(analysis, max_func_len=20)
    assert len(recs) == 1
    assert "big_one" in recs[0]
    assert "30 lines" in recs[0] or "30 lines long" in recs[0]  # wording check


def test_generate_recommendations_no_long_functions():
    funcs = [FunctionInfo(name="tiny", line_count=5)]
    analysis = Analysis(functions={"file.py": funcs})

    recs = generate_recommendations(analysis, max_func_len=20)
    assert recs == []


def test_end_to_end_empty_codebase():
    cb = upload_codebase({})
    analysis = train_model(cb)
    assert analysis.functions == {}
    recs = generate_recommendations(analysis)
    assert recs == []
