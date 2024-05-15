from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/ristoranti/Copacabana/2019-09-15?order_by=date")
    assert response.status_code == 200
    data = response.json()
    assert data ==  [{'date': '2019-09-15',
      'restaurant': 'Copacabana',
      'hours': 175.0,
      'amount': 2545.34,
      'totbudget': 3996.87,
      'totsells': 1451.53}]
    
def test_2():
    response = client.get("/ristoranti/Copacabana/?date__lte=2019-09-15&order_by=date")
    assert response.status_code == 200
    data = response.json()
    assert data[0] ==  {"index":0,"date":"2016-01-01","restaurant":"Copacabana",
                        "planned_hours":141.0,"actual_hours":176.0,"budget":4025.65,"sells":2801.33,"hours":-35.0,"amount":1224.32}
