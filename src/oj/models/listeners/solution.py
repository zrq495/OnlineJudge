
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
        self.update_children_count(
            solutions, 'user', 'accepts', 'accepts_count')
        self.update_children_count(
            solutions, 'problem', 'solutions', 'solutions_count')
        self.update_children_count(
            solutions, 'problem', 'accepts', 'accepts_count')
        self.update_children_count(
            solutions, 'problem', 'solution_users',
            'solution_users_count', True)
        self.update_children_count(
            solutions, 'problem', 'accept_users', 'accept_users_count', True)
