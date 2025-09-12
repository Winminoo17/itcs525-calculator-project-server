from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_basic_division():
    r = client.post("/calculator", json={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculator", json={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculator", json={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_error():
    r = client.post("/calculator", json={"expr": "2**(3"})
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
        r = client.post("/calculator", json={"expr": expr})
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

def test_history_response_model():
    """Test that history returns proper CalculatorLog structure."""
    # Clear and add one calculation
    client.delete("/history")
    client.post("/calculator", json={"expr": "5 + 5"})
    
    r = client.get("/history")
    assert r.status_code == 200
    history = r.json()
    assert len(history) == 1
    
    log_entry = history[0]
    # Check all required fields exist
    required_fields = ["timestamp", "expr", "result", "ok", "error"]
    for field in required_fields:
        assert field in log_entry
    
    # Verify data types and values
    assert isinstance(log_entry["timestamp"], str)  # Should be ISO format string
    assert log_entry["expr"] == "5 + 5"
    assert log_entry["result"] == 10.0
    assert log_entry["ok"] is True
    assert log_entry["error"] == ""

def test_expression_model_validation():
    """Test that Expression model validates input properly."""
    # Valid expression
    r = client.post("/calculator", json={"expr": "1 + 1"})
    assert r.status_code == 200
    
    # Missing expr field should return 422 (validation error)
    r = client.post("/calculator", json={})
    assert r.status_code == 422
