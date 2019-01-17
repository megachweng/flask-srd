import collections
import logging
from dns import rdatatype
from dns.resolver import Resolver
from dns.resolver import NoNameservers, NoAnswer

LOGGER = logging.getLogger(__name__)

SRV = collections.namedtuple(
    'SRV', ['host', 'port', 'priority', 'weight', 'hostname'])


class ConsulResolver:
    def __init__(self, nameservers: list = None, port: int = 8600):
        self.resolver = Resolver()
        self.resolver.nameservers = nameservers
        self.resolver.port = port

    def query(self, service_name: str, tag: str = None, domain: str = 'service.consul'):
        label = [q for q in [tag, service_name, domain] if q]
        try:
            answer = self.resolver.query('.'.join(label), 'SRV')
            return self._build_result_set(answer)
        except (NoNameservers, NoAnswer) as e:
            LOGGER.error(f'DNS Query Failed :{e.msg}')

    @staticmethod
    def _build_result_set(answer):
        """Return a list of SRV instances for a DNS answer.
        :rtype: list of SRV
        """

        def _build_resource_to_address_map(answer):
            mapping = collections.defaultdict(list)
            for resource in answer.response.additional:
                target = resource.name.to_text()
                mapping[target].extend(record.address for record in resource.items if record.rdtype == rdatatype.A)
            return mapping

        resource_map = _build_resource_to_address_map(answer)
        result_set = []
        for resource in answer:
            target = resource.target.to_text()
            if target in resource_map:
                result_set.extend(
                    SRV(address, resource.port, resource.priority, resource.weight,
                        target.strip('.')) for address in resource_map[target])
            else:
                result_set.append(
                    SRV(target.rstrip('.'), resource.port, resource.priority,
                        resource.weight, target.strip('.')))
        return result_set


if __name__ == '__main__':
    r = ConsulResolver(nameservers=['10.1.1.7'])
    print(r.query(tag='python', service_name='a', domain='service.consul'))
