# coding: utf-8

import requests
from flask_srd.consul_dns import ConsulResolver
import random
from flask import current_app as app
from urllib.parse import urljoin
from flask_srd.decorators import with_retry_connections


class ConsulService(object):
    def __init__(self, service_name, tag=None, nameservers=None, port=None, domain='service.consul'):
        """
        :param service_name: str
        :param nameservers: consul dns server list
        :param port: dns port
        :param domain: str
        """
        if not isinstance(nameservers, list):
            raise ValueError('NameServer must be a list')

        self.service_name = service_name
        self.tag = tag
        self.domain = domain
        self.resolver = ConsulResolver(nameservers=nameservers, port=port)
        self.session = requests.Session()

    def _resolve(self):
        """
        Query the consul DNS server for the service IP and port
        """
        services = self.resolver.query(service_name=self.service_name, tag=self.tag, domain=self.domain)
        app.logger.info(f'Available Services {self.service_name}: {services}')
        choose_service = random.choice(services)
        app.logger.info(f'Choose Server: {choose_service.host}:{choose_service.port}')
        return f'http://{choose_service.host}:{choose_service.port}'

    @property
    def base_url(self):
        """
        get the next endpoint from self.endpoints
        """
        return self._resolve()

    @with_retry_connections()
    def request(self, method, endpoint, **kwargs):
        """
        Proxy to requests.request
        :param method: str formatted http method
        :param endpoint: service endpoint
        :param kwargs: kwargs passed directly to requests.request
        :return:
        """
        kwargs.setdefault('timeout', (1, 30))
        return self.session.request(
            method,
            urljoin(self.base_url, endpoint),
            **kwargs
        )

    def get(self, endpoint, **kwargs):
        return self.request('GET', endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request('POST', endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request('DELETE', endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request('PUT', endpoint, **kwargs)

    def options(self, endpoint, **kwargs):
        return self.request('OPTIONS', endpoint, **kwargs)

    def head(self, endpoint, **kwargs):
        return self.request('HEAD', endpoint, **kwargs)
