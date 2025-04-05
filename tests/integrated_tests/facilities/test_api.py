from src.schemas.facilities import FacilityAdd


async def test_api_add_facility(ac):
    response = await ac.post(
        "/facilities",
        json={
            "title":"Массажка"
        }
        )
    
    assert response.status_code == 200


async def test_api_get_facility(ac):
    response = await ac.get(
        "facilities"
        )
    
    assert response.json()
    assert response.status_code == 200