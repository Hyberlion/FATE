#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#


import typing

from fate_arch.abc import CTableABC
from fate_arch.common import log
from fate_arch.common.profile import log_elapsed

LOGGER = log.getLogger()


class Table(CTableABC):

    def __init__(self, rp):
        self._rp = rp

    @property
    def partitions(self):
        return self._rp.get_partitions()

    @log_elapsed
    def save(self, address, partitions, schema: dict, **kwargs):
        options = kwargs.get("options", {})
        from fate_arch.common.address import EggRollAddress
        if isinstance(address, EggRollAddress):
            options["store_type"] = address.storage_type
            self._rp.save_as(name=address.name, namespace=address.namespace, partition=partitions, options=options)
            schema.update(self.schema)
            return
        raise NotImplementedError(f"address type {type(address)} not supported with eggroll backend")

    @log_elapsed
    def collect(self, **kwargs) -> list:
        return self._rp.get_all()

    @log_elapsed
    def count(self, **kwargs) -> int:
        return self._rp.count()

    def take(self, n=1, **kwargs):
        options = dict(keys_only=False)
        return self._rp.take(n=n, options=options)

    def first(self):
        options = dict(keys_only=False)
        return self._rp.first(options=options)

    @log_elapsed
    def map(self, func, **kwargs):
        return Table(self._rp.map(func))

    @log_elapsed
    def mapValues(self, func: typing.Callable[[typing.Any], typing.Any], **kwargs):
        return Table(self._rp.map_values(func))

    def applyPartitions(self, func):
        return Table(self._rp.collapse_partitions(func))

    def mapPartitions(self, func, use_previous_behavior=True, **kwargs):
        if use_previous_behavior is True:
            LOGGER.warning(f"please use `applyPartitions` instead of `mapPartitions` "
                           f"if the previous behavior was expected. "
                           f"The previous behavior will not work in future")
            return self.applyPartitions(func)

        return Table(self._rp.map_partitions(func))

    def mapReducePartitions(self, mapper, reducer, **kwargs):
        return Table(self._rp.map_partitions(func=mapper, reduce_op=reducer))

    @log_elapsed
    def reduce(self, func, **kwargs):
        return self._rp.reduce(func)

    @log_elapsed
    def join(self, other: 'Table', func, **kwargs):
        return Table(self._rp.join(other._rp, func=func))

    @log_elapsed
    def glom(self, **kwargs):
        return Table(self._rp.glom())

    @log_elapsed
    def sample(self, fraction, seed=None, **kwargs):
        return Table(self._rp.sample(fraction=fraction, seed=seed))

    @log_elapsed
    def subtractByKey(self, other: 'Table', **kwargs):
        return Table(self._rp.subtract_by_key(other._rp))

    @log_elapsed
    def filter(self, func, **kwargs):
        return Table(self._rp.filter(func))

    @log_elapsed
    def union(self, other: 'Table', func=lambda v1, v2: v1, **kwargs):
        return Table(self._rp.union(other._rp, func=func))

    @log_elapsed
    def flatMap(self, func, **kwargs):
        flat_map = self._rp.flat_map(func)
        shuffled = flat_map.map(lambda k, v: (k, v))  # trigger shuffle
        return Table(shuffled)
