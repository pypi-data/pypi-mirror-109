import requests
import requests.structures
import os
import yaml
from m2r import convert
from .response import AbstractResponse


class ClientInitError(ImportError):
    pass


class Client:
    default_host = ''

    def __init__(self, host=None, api_key=None, session=None):
        if host is None:
            host = self.default_host
        if session is None:
            session = requests.session()

        self._url = host.rstrip('/') + '/{endpoint}'
        self._session = session
        self._headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': host,
        }

    def status(self):
        return self.get('status')

    def get(self, endpoint, params=None):
        """
        :return: :class:`Response <apisports.response.AbstractResponse>` object
        :rtype: apisports.response.AbstractResponse
        """

        return AbstractResponse.create(
            self,
            self._session.get(
                self._url.format(endpoint=endpoint),
                params=params,
                headers=self._headers
            )
        )


class ClientMeta:
    @classmethod
    def get(cls, kind, version=None):
        if version is None:
            version = '1'
        filename = os.path.join(os.path.dirname(__file__),
                                'data', f'{kind}-v{version}.yaml')
        try:
            with open(filename, encoding='UTF-8') as stream:
                config = yaml.safe_load(stream)

            return {
                "default_host": config['servers'][0]['url'],
                **{
                    p['get']['operationId'][4:].replace('-', '_'): cls._get_method(
                        class_name=kind,
                        name=p['get']['operationId'][4:].replace('-', '_'),
                        description=p['get']['description'],
                        endpoint=k.lstrip('/'),
                        params=[param for param in p['get']['parameters'] if param['in'] == 'query'],
                    ) for k, p in config['paths'].items()
                }
            }
        except (KeyError, OSError, yaml.YAMLError) as exc:
            raise ClientInitError(f"Could not load API config for {kind} from {filename}") from exc

    @staticmethod
    def _get_method(class_name, name, description, endpoint, params):
        def _(self, **kwargs):
            return self.get(endpoint, kwargs)

        _.__name__ = name
        _.__module__ = f'apisports.{class_name}'

        _.__doc__ = convert(description) + '\n\n'

        for p in params:
            _.__doc__ += ":param {name}: {description}{pattern}\n".format(**{
                "description": '',
                "pattern": (' (' + p['schema']['pattern'] + ')' if 'pattern' in p['schema'] else ''),
                **p
            })
            if 'type' in p['schema']:
                _.__doc__ += ":type {name}: {type}\n".format(
                    name=p['name'],
                    type=p['schema']['type'],
                )

        _.__doc__ += '\n:return: :class:`Response <apisports._client.Response>` object'
        _.__doc__ += '\n:rtype: apisports.response.AbstractResponse'
        return _
