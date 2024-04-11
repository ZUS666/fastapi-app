import json
import re

import pytest
from httpx import AsyncClient

from .confest import *
from .test_data import registration_data


@pytest.mark.asyncio
class TestUserRegistraion:
    url = '/users/signup'

    @pytest.mark.parametrize(
        'email,password,re_password,firstname,lastname,status',
        registration_data)
    async def test_registration_all_fields(
        self,
        client: AsyncClient,
        email,
        password,
        re_password,
        firstname,
        lastname,
        status
    ) -> None:
        response = await client.post(
            self.url,
            json={
                "email": email,
                "password": password,
                "re_password": re_password,
                "profile": {
                    "first_name": firstname,
                    "last_name": lastname
                }
            }
        )
        assert response.status_code == status
        if response.status_code == 201:
            result = response.json()
            assert result['user_id'] is not None
            assert result['email'] == email
            assert result['profile']['first_name'] == firstname
            assert result['profile']['last_name'] == lastname

    async def test_skip_first_name(self, client: AsyncClient) -> None:
        data = {
            "email": 'skipfn@gmail.com',
            "password": 'password123PASS@',
            "re_password": 'password123PASS@',
            "profile": {
                "last_name": 'lastname'
            }
        }
        response = await client.post(
            self.url,
            json=data
        )
        assert response.status_code == 201
        result = response.json()
        assert result['user_id'] is not None
        assert result['email'] == data['email']
        assert result['profile']['first_name'] is None
        assert result['profile']['last_name'] == data['profile']['last_name']

    async def test_skip_last_name(self, client: AsyncClient) -> None:
        data = {
            "email": 'skipln@gmail.com',
            "password": 'password123PASS@',
            "re_password": 'password123PASS@',
            "profile": {
                "first_name": 'lastname'
            }
        }
        response = await client.post(
            self.url,
            json=data
        )
        assert response.status_code == 201
        result = response.json()
        assert result['user_id'] is not None
        assert result['email'] == data['email']
        assert result['profile']['last_name'] is None
        assert result['profile']['first_name'] == data['profile']['first_name']

    async def test_skip_profile(self, client: AsyncClient) -> None:
        data = {
            "email": 'skipprofile@gmail.com',
            "password": 'password123PASS@',
            "re_password": 'password123PASS@',
        }
        response = await client.post(
            self.url,
            json=data
        )
        assert response.status_code == 201
        result = response.json()
        assert result['user_id'] is not None
        assert result['email'] == data['email']
        assert result['profile']['last_name'] is None
        assert result['profile']['first_name'] is None


@pytest.mark.asyncio
class TestUserConfirmation:
    sign_up_url = '/users/signup'
    activation_url = '/users/activation'

    async def test_activation(self, client: AsyncClient, capsys: pytest.CaptureFixture) -> None:
        data = {
            "email": 'activ@gmail.com',
            'password': 'password123PASS@',
            're_password': 'password123PASS@',
        }
        await client.post(self.sign_up_url, json=data)
        captured = capsys.readouterr().out
        pattern = r"'code': '([^']+)'"
        code = re.search(pattern, captured).group(1)
        act_data = {
            'email': data['email'],
            'code': code
        }
        response = await client.post(self.activation_url, json=act_data)
        assert response.status_code == 200
