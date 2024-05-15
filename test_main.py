from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/ristoranti/Copacabana/2019-09-15?order_by=date")
    assert response.status_code == 200
    assert response.json() == [{'date': '2019-09-15',
  'restaurant': 'Copacabana',
  'hours': 175.0,
  'amount': 2545.34,
  'totbudget': 3996.87,
  'totsells': 1451.53}]