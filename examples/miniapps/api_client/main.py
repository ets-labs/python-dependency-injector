"""Main module."""

from dependency_injector import providers

import api
import models


# Creating ApiClient and User providers:
api_client = providers.Singleton(api.ApiClient,
                                 host='production.com',
                                 api_key='PROD_API_KEY')
user_factory = providers.Factory(models.User,
                                 api_client=api_client)


if __name__ == '__main__':
    # Creating several users and register them:
    user1 = user_factory(1)
    user1.register()
    # API call [production.com:PROD_API_KEY], method - register, data -
    # {'id': 1}

    user2 = user_factory(2)
    user2.register()
    # API call [production.com:PROD_API_KEY], method - register, data -
    # {'id': 2}

    # Overriding of ApiClient on dev environment:
    api_client.override(providers.Singleton(api.ApiClient,
                                            host='localhost',
                                            api_key='DEV_API_KEY'))

    user3 = user_factory(3)
    user3.register()
    # API call [localhost:DEV_API_KEY], method - register, data - {'id': 3}
