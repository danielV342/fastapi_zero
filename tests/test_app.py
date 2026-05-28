from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client):

    response = client.get('/')

    assert response.json() == {'message': 'Ola mundo!'}
    assert response.status_code == HTTPStatus.OK


def teste_create_user(client):

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'alice',
    }


def test_read_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )
    print(response.json())
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):

    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_read_user_not_found(client):
    response = client.get(
        '/users/999',
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado.'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário deletado.'}

    # def test_update_user_not_found(client, token):
    #     response = client.put(
    #         '/users/99999',
    #         headers={'Authorization': f'Bearer {token}'},
    #         json={
    #             'username': 'bob',
    #             'email': 'bob@example.com',
    #             'password': 'secret',
    #         },
    #     )

    # assert response.status_code == HTTPStatus.NOT_FOUND


# def test_update_integrity_error(client, user, token):
#     client.post(
#         '/users/',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'username': 'fausto',
#             'email': 'fausto@example.com',
#             'password': 'secret',
#         },
#     )

#     response = client.put(
#         f'/users/{user.id}',
#         json={
#             'username': 'fausto',
#             'email': 'bob@example.com',
#             'password': 'mynewpassword',
#         },
#     )

#     assert response.status_code == HTTPStatus.CONFLICT
#     assert response.json() == {'detail': 'Este usuário ou e-mail já existe.'}


# def test_create_user_integrity_error(client, user, token):

#     response = client.post(
#         '/users/',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'username': 'teste',
#             'email': 'outro@teste.com',
#             'password': 'testtest',
#         },
#     )

#     assert response.status_code == HTTPStatus.CONFLICT
#     assert response.json() == {'detail': 'Usuário já existe.'}


def test_create_email_integrity_error(client, user, token):

    response = client.post(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'outro',
            'email': 'teste@teste.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'E-mail já existe.'}


def test_delete_user_not_found(client, user, token):
    response = client.delete(
        '/users/9999',
        headers={'Authorization': f'Bearer {token}'},
        )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado.'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
