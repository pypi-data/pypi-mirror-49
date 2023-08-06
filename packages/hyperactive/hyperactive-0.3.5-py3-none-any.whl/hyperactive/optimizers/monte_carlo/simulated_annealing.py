# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import random

import numpy as np
import tqdm

from ...base import BaseOptimizer
from ..local.hill_climbing_optimizer import HillClimber


class SimulatedAnnealingOptimizer(BaseOptimizer):
    def __init__(
        self,
        search_config,
        n_iter,
        metric="accuracy",
        n_jobs=1,
        cv=5,
        verbosity=1,
        random_state=None,
        warm_start=False,
        memory=True,
        scatter_init=False,
        eps=1,
        t_rate=0.98,
        n_neighbours=1,
    ):
        super().__init__(
            search_config,
            n_iter,
            metric,
            n_jobs,
            cv,
            verbosity,
            random_state,
            warm_start,
            memory,
            scatter_init,
        )

        self.eps = eps
        self.t_rate = t_rate
        self.temp = 0.1

    def _annealing(self, _cand_):
        self.temp = self.temp * self.t_rate
        rand = random.uniform(0, 1)

        # Normalized score difference to have a factor for later use with temperature and random
        score_diff_norm = (self.score_curr - _cand_.score) / (
            self.score_curr + _cand_.score
        )
        p_accept = np.exp(-(score_diff_norm / self.temp))

        if _cand_.score > self.score_curr:
            self.score_curr = _cand_.score
            self.pos_curr = _cand_.pos

            if _cand_.score > _cand_.score_best:
                _cand_.score_best = _cand_.score
                self.pos_curr = _cand_.pos

        elif p_accept > rand:
            self.score_curr = _cand_.score
            self.pos_curr = _cand_.pos

        return self.pos_curr

    def search(self, nth_process, X, y):
        _cand_ = self._init_search(nth_process, X, y)
        _annealer_ = Annealer()

        _cand_.eval(X, y)

        _cand_.pos_best = _cand_.pos
        _cand_.score_best = _cand_.score

        self.pos_curr = _cand_.pos
        self.score_curr = _cand_.score

        for i in tqdm.tqdm(**self._tqdm_dict(_cand_)):

            _annealer_.find_neighbour(_cand_)
            _cand_.eval(X, y)

            self._annealing(_cand_)

        return _cand_


class Annealer(HillClimber):
    def __init__(self, eps=1):
        super().__init__(eps)

    def find_neighbour(self, _cand_):
        super().climb(_cand_)
