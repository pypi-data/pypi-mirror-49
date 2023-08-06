from collections import OrderedDict
import os

import yaml


def _unsafe_include_aware_ordered_load(stream):

    class OrderedLoader(yaml.Loader):

        def __init__(self, stream):
            self._root = os.path.split(stream.name)[0]
            super(OrderedLoader, self).__init__(stream)

        def include(self, node):
            filename = os.path.join(self._root, self.construct_scalar(node))
            with open(filename, 'r') as f:
                return yaml.load(f, OrderedLoader)

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    OrderedLoader.add_constructor('!include', OrderedLoader.include)

    return yaml.load(stream, OrderedLoader)


def _ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            list(data.items()))
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)
