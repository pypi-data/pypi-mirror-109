from .core import region_name, session


def get_secret_value(secret_id):
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    return client.get_secret_value(SecretId=secret_id)
