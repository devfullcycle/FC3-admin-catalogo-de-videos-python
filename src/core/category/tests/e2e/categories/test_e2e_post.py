

import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient
from django.db import connections

@pytest.mark.group('e2e')
@pytest.mark.django_db
class TestCategoriesPostE2E:

    def test_post(self):
        
        client_http = APIClient()
        response: Response = client_http.post('/categories/',data={'name': 'test'})
        # print(response.content)
        # print(response.data)
        assert response.status_code == 201
        # verifico os dados
        # repo.find_by_id()
