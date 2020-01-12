# -*- coding: utf-8 -*-

from ..settings.settings import NUMBER_OF_SPIDERS
from .all_pipelines import ALL_PIPELINES

class TransformData(object):
    def process_item(self, item, spider):
        for counter in range(1, NUMBER_OF_SPIDERS + 1):
            if type(spider).__name__ == f'Spider{counter}':
                ALL_PIPELINES[f'spider{counter}'](item)
        return item
