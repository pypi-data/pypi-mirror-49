import json
import logging
import uuid
from functools import partial
from typing import List

import boto3
import requests

from bubuku.config import Config, KafkaProperties
from bubuku.id_generator import BrokerIdGenerator
from bubuku.zookeeper import BukuExhibitor, AddressListProvider
from bubuku.zookeeper.exhibitor import ExhibitorAddressProvider

_LOG = logging.getLogger('bubuku.amazon')


class EnvProvider(object):
    def get_id(self) -> str:
        raise NotImplementedError('Not implemented')

    def get_address_provider(self):
        raise NotImplementedError('Not implemented')

    def create_broker_id_manager(self, zk: BukuExhibitor, kafka_props: KafkaProperties):
        raise NotImplementedError('Not implemented')

    def get_rack(self):
        raise NotImplementedError('Not implemented')

    @staticmethod
    def create_env_provider(config: Config):
        if config.mode == 'amazon':
            return AmazonEnvProvider(config)
        elif config.mode == 'local':
            return LocalEnvProvider()
        else:
            raise NotImplementedError('Configuration mode "{}" is not supported'.format(config.mode))


class AmazonEnvProvider(EnvProvider):
    def __init__(self, config: Config):
        self.aws_addr = '169.254.169.254'
        self.config = config
        self.ip_address = None
        self._document = None

    def _get_document(self) -> dict:
        if not self._document:
            self._document = requests.get(
                'http://{}/latest/dynamic/instance-identity/document'.format(self.aws_addr),
                timeout=5).json()
            _LOG.info("Amazon specific information loaded from AWS: {}".format(json.dumps(self._document, indent=2)))
        return self._document

    def get_id(self) -> str:
        if not self.ip_address:
            self.ip_address = self._get_document()['privateIp']
        return self.ip_address

    def get_rack(self):
        return self._get_document()['availabilityZone']

    def _load_instance_ips(self, lb_name: str):
        region = self._get_document()['region']

        private_ips = []

        elb = boto3.client('elb', region_name=region)
        ec2 = boto3.client('ec2', region_name=region)

        response = elb.describe_instance_health(LoadBalancerName=lb_name)

        for instance in response['InstanceStates']:
            if instance['State'] == 'InService':
                private_ips.append(ec2.describe_instances(
                    InstanceIds=[instance['InstanceId']])['Reservations'][0]['Instances'][0]['PrivateIpAddress'])

        _LOG.info("Ip addresses for {} are: {}".format(lb_name, private_ips))
        return private_ips

    def get_address_provider(self):
        if self.config.zk_static_ips:
            return StaticAddressesProvider(self.config.zk_static_ips)
        else:
            return ExhibitorAddressProvider(partial(self._load_instance_ips, self.config.zk_stack_name))

    def create_broker_id_manager(self, zk: BukuExhibitor, kafka_props: KafkaProperties):
        return BrokerIdGenerator(zk, kafka_props)


class _LocalAddressProvider(AddressListProvider):
    def get_latest_address(self) -> (List[str], int):
        return ('zookeeper',), 2181


class StaticAddressesProvider(AddressListProvider):
    def __init__(self, addr: str):
        ips, port = addr.split(':')
        self.ips = ips.split(',')
        self.port = int(port)

    def get_latest_address(self) -> (List[str], int):
        return self.ips, self.port


class LocalEnvProvider(EnvProvider):
    unique_id = str(uuid.uuid4())

    def get_id(self) -> str:
        return self.unique_id

    def get_address_provider(self):
        return _LocalAddressProvider()

    def get_rack(self):
        return None

    def create_broker_id_manager(self, zk: BukuExhibitor, kafka_props: KafkaProperties):
        return BrokerIdGenerator(zk, kafka_props)
