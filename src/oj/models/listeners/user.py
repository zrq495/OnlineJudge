
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .. import SolutionModel
from ..hook import entity, CommonEntityHook


@entity(SolutionModel)
class SolutionHook(CommonEntityHook):

    flush_interest = ['new', 'deleted']

    def on_flush(self, new_solutions, deleted_solutions):
        solutions = new_solutions | deleted_solutions
        self.update_children_count(
            solutions, 'user', 'solutions', 'solutions_count')

