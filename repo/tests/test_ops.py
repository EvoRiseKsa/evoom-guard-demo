from tempconv.ops import c_to_f, f_to_c

# Cross-account negative control: touching the judge-owned test must be rejected.

def test_c_to_f():
    assert c_to_f(100) == 212

def test_f_to_c():
    assert f_to_c(212) == 100
