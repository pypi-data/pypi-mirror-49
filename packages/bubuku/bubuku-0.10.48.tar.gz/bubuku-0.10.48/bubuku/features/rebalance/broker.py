from typing import Tuple, List, Iterator, Dict, Optional


class _TopicPartitions(object):
    __slots__ = (
        '_items',
        '_expectation',
        '_has_free_slots',
        '_topic_partitions'
    )

    def __init__(self):
        self._items = set()
        self._expectation = 0
        self._has_free_slots = None
        self._topic_partitions = {}

    def __str__(self):
        return 'TP, expectation: {}, items: {}'.format(self._expectation, self._items)

    def get_item_count(self) -> int:
        return len(self._items)

    def contains(self, item) -> bool:
        return item in self._items

    def add(self, item: Tuple[str, int]):
        self._items.add(item)
        topic, partition = item
        if topic not in self._topic_partitions:
            self._topic_partitions[topic] = []
        self._topic_partitions[topic].append(partition)
        self._has_free_slots = None

    def remove(self, item: Tuple[str, int]):
        self._items.remove(item)
        topic, partition = item
        self._topic_partitions[topic].remove(partition)
        self._has_free_slots = None

    def iterate_items(self) -> Iterator[Tuple[str, int]]:
        return self._items.__iter__()

    def get_topic_partitions(self, topic: str) -> List[int]:
        return self._topic_partitions.get(topic, [])

    def get_expectation(self) -> int:
        return self._expectation

    def set_expectation(self, expectation: int):
        self._has_free_slots = None
        self._expectation = expectation

    def calculate_cardinality(self) -> Dict[str, int]:
        return {k: len(v) for k, v in self._topic_partitions.items()}

    def has_free_slots(self) -> bool:
        if self._has_free_slots is None:
            self._has_free_slots = self.get_item_count() < self.get_expectation()
        return self._has_free_slots


class BrokerDescription(object):
    __slots__ = (
        '_broker_id',
        '_rack_id',
        '_leaders',
        '_replicas',
    )

    def __init__(self, broker_id: int, rack_id: str = None):
        self._broker_id = broker_id
        self._rack_id = rack_id
        self._leaders = _TopicPartitions()
        self._replicas = _TopicPartitions()

    @property
    def broker_id(self) -> int:
        return self._broker_id

    @property
    def rack_id(self) -> str:
        return self._rack_id

    def __str__(self) -> str:
        return 'BrokerDescription(id={}, rack={}, leaders={}, replicas={})'.format(
            self._broker_id, self._rack_id, self._leaders, self._replicas)

    def set_leader_expectation(self, leader_count: int):
        self._leaders.set_expectation(leader_count)

    def set_replica_expectation(self, replica_count: int):
        self._replicas.set_expectation(replica_count)

    def add_leader(self, topic_partition: Tuple[str, int]):
        self._leaders.add(topic_partition)

    def add_replica(self, topic_partition: Tuple[str, int]):
        self._replicas.add(topic_partition)

    def get_leader_count(self) -> int:
        return self._leaders.get_item_count()

    def get_replica_count(self) -> int:
        return self._replicas.get_item_count()

    def get_replica_overload(self) -> int:
        return self._replicas.get_item_count() - self._replicas.get_expectation()

    def has_free_replica_slots(self) -> int:
        return self._replicas.has_free_slots()

    def have_extra_leaders(self) -> bool:
        return self._leaders.get_expectation() < self._leaders.get_item_count()

    def have_less_leaders(self) -> bool:
        return self._leaders.get_expectation() > self._leaders.get_item_count()

    def get_expected_leaders(self) -> int:
        return self._leaders.get_expectation()

    def accept_leader(self, source_broker: 'BrokerDescription', topic_partition: Tuple[str, int]):
        """
        Moves topic_partition from source_broker to self broker.
        :param source_broker: Broker to take topic_partition from.
        :param topic_partition: topic and partition tuple to take.
        """
        self._leaders.add(topic_partition)
        source_broker._leaders.remove(topic_partition)

    def _accept_replica(self, source_broker: 'BrokerDescription', topic_partition: Tuple[str, int]) -> bool:
        # Already a leader for this partition
        if self._leaders.contains(topic_partition):
            return False
        # Already a replica for this partition
        if self._replicas.contains(topic_partition):
            return False
        if self._rack_id != source_broker._rack_id:
            return False
        self._replicas.add(topic_partition)
        source_broker._replicas.remove(topic_partition)
        return True

    def move_replica(self, topic_partition: Tuple[str, int], broker_list: List['BrokerDescription']) \
            -> Optional['BrokerDescription']:
        """
        Moves replica topic_partition to some broker from broker_list.
        :param topic_partition: Topic and partition to move
        :param broker_list: List of brokers (BrokerDescription) to move to
        :return: Broker, to which partition was moved
        """
        for target in broker_list:
            if target._accept_replica(self, topic_partition):
                return target
        return None

    def list_replica_copies(self) -> List[Tuple[str, int]]:
        return list([tp for tp in self._replicas.iterate_items() if self._leaders.contains(tp)])

    def list_partitions(self, topic: str, replica: bool) -> List[int]:
        return (self._replicas if replica else self._leaders).get_topic_partitions(topic)

    def list_replicas(self) -> Iterator[Tuple[str, int]]:
        return self._replicas.iterate_items()

    def calculate_topic_cardinality(self) -> Dict[str, int]:
        """
        Calculates 'topic to leader count' dictionary on this broker.
        For example, topic t0 have partitions 0, 1, 2, 3. If leaders for partitions 0, 3 are located on this broker
         than return value will contain mapping t0->2 (there are 2 leaders for topic t0 on this broker)
        :return: Dictionary with leaders count per topic for this broker.
        """
        return self._leaders.calculate_cardinality()
