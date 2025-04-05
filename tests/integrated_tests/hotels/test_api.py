

async def test_hotels_get(ac):
    response = await ac.get(
        "/hotels",
        params= {
            "date_from": "2024-10-10",
            "date_to": "2024-10-18"
        }    
        )
    

    assert response.status_code == 200