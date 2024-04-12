import random

import pytest
from httpx import AsyncClient

from .test_data import registration_data
from .utils import get_code_capsys
from repositories.sql_db.models.user import User


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
    resend_activation_url = '/users/resend_activation'
    reset_password = '/users/reset_password'
    reset_password_request = '/users/reset_password_request'

    async def test_activation(self, client: AsyncClient, capsys: pytest.CaptureFixture) -> None:
        data = {
            "email": 'activ@gmail.com',
            'password': 'password123PASS@',
            're_password': 'password123PASS@',
        }
        await client.post(self.sign_up_url, json=data)
        act_data = {
            'email': data['email'],
            'code': get_code_capsys(capsys)
        }
        response = await client.post(self.activation_url, json=act_data)
        assert response.status_code == 200

    async def test_activation_resend_fake_mail(
        self,
        client: AsyncClient,
    ) -> None:
        data = {
            'email': 'fakemail@gmail.com',
        }
        response = await client.post(self.resend_activation_url, json=data)
        assert response.status_code == 404, ('Failed resend activation fake mail')

    async def test_activation_resend(
        self,
        client: AsyncClient,
        capsys: pytest.CaptureFixture,
        inactive_user: User,
    ) -> None:
        inactive_email = inactive_user.email
        data = {
            'email': inactive_email
        }
        response = await client.post(self.resend_activation_url, json=data)
        assert response.status_code == 200, ('Failed resend activation')
        response_fake_code = await client.post(
            self.activation_url,
            json={'email': inactive_email, 'code': str(random.randint(0, 9999999))}
        )
        assert response_fake_code.status_code == 400, ('Fake code activation request')
        data = {
            'email': inactive_email,
            'code': get_code_capsys(capsys)
        }
        activ_response = await client.post(
            self.activation_url,
            json=data
        )
        assert activ_response.status_code == 200, ('Failed activation with code')
        re_activ_response = await client.post(
            self.activation_url,
            json=data
        )
        assert re_activ_response.status_code == 400, ('Activation after success')

    async def test_reset_password(
        self,
        client: AsyncClient,
        active_user: User,
        capsys: pytest.CaptureFixture,
    ) -> None:
        response = await client.post(
            self.reset_password_request,
            json={'email': active_user.email}
        )
        assert response.status_code == 200, ('Failed reset password request')
        new_password = 'password123PASS@'
        data = {
            'email': active_user.email,
            'password': new_password,
            're_password': new_password,
            'code': get_code_capsys(capsys)
        }
        response = await client.post(
            self.reset_password,
            json=data
        )
        assert response.status_code == 200, ('Failed reset password')
