from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_basic_division():
    r = client.post("/calculator", params={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculator", params={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculator", params={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_error():
    r = client.post("/calculator", params={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""
    
def test_calculator_history():
    r = client.delete("/history")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True

    expressions = ["10 + 5", "20 - 4", "3 * 7"]
    for expr in expressions:
        r = client.post("/calculator", params={"expr": expr})
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] is True

    r = client.get("/history")
    assert r.status_code == 200
    history = r.json()
    assert len(history) == len(expressions)
    for i, record in enumerate(history):
        assert record["expr"] == expressions[i]
        assert record["ok"] is True