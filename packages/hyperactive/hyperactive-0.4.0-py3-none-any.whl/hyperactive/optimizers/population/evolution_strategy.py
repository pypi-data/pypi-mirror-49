# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import numpy as np
import random

from ...base import BaseOptimizer
from ...base import BasePositioner


class EvolutionStrategyOptimizer(BaseOptimizer):
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
        individuals=10,
        mutation_rate=0.7,
        crossover_rate=0.3,
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

        self.individuals = individuals
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        self.n_mutations = int(round(self.individuals * mutation_rate))
        self.n_crossovers = int(round(self.individuals * crossover_rate))

        self.initializer = self._init_evo

    def _init_individuals(self, _cand_):
        _p_list_ = [Individual() for _ in range(self.individuals)]
        for _p_ in _p_list_:
            _p_.pos_current = _p_.move_random(_cand_)
            _p_.pos_best = _p_.pos_current

        return _p_list_

    def _mutate_individuals(self, _cand_, _p_list_, mutate_idx):
        _p_list_ = np.array(_p_list_)
        for _p_ in _p_list_[mutate_idx]:
            _p_.pos_new = _p_.move_climb(_cand_, _p_.pos_current)

    def _crossover(self, _cand_, _p_list_, cross_idx, replace_idx):
        _p_list_ = np.array(_p_list_)
        for i, _p_ in enumerate(_p_list_[replace_idx]):
            j = i + 1
            if j == len(cross_idx):
                j = 0

            pos_new = self._cross_two_ind(
                [_p_list_[cross_idx][i], _p_list_[cross_idx][j]]
            )

            _p_.pos_new = pos_new

    def _cross_two_ind(self, _p_list_):
        pos_new = []

        for pos1, pos2 in zip(_p_list_[0].pos_current, _p_list_[1].pos_current):
            rand = random.randint(0, 1)
            if rand == 0:
                pos_new.append(pos1)
            else:
                pos_new.append(pos2)

        return np.array(pos_new)

    def _new_generation(self, _cand_, _p_list_):
        idx_sorted_ind = self._rank_individuals(_p_list_)
        mutate_idx, cross_idx, replace_idx = self._select_individuals(idx_sorted_ind)

        self._mutate_individuals(_cand_, _p_list_, mutate_idx)
        self._crossover(_cand_, _p_list_, cross_idx, replace_idx)

    def _eval_individuals(self, _cand_, _p_list_, X, y):
        for _p_ in _p_list_:
            _p_.score_new = _cand_.eval_pos(_p_.pos_new, X, y)

            if _p_.score_new > _cand_.score_best:
                _cand_.score_best = _p_.score_new
                _cand_.pos_best = _p_.pos_new

                _p_.pos_current = _p_.pos_new
                _p_.score_current = _p_.score_new

    def _rank_individuals(self, _p_list_):
        scores_list = []
        for _p_ in _p_list_:
            scores_list.append(_p_.score_current)

        scores_np = np.array(scores_list)
        idx_sorted_ind = list(scores_np.argsort()[::-1])

        return idx_sorted_ind

    def _select_individuals(self, index_best):
        mutate_idx = index_best[: self.n_mutations]
        cross_idx = index_best[: self.n_crossovers]

        n = self.individuals - max(self.n_mutations, self.n_crossovers)
        replace_idx = index_best[-n:]

        return mutate_idx, cross_idx, replace_idx

    def _iterate(self, i, _cand_, _p_list_, X, y):
        self._new_generation(_cand_, _p_list_)
        self._eval_individuals(_cand_, _p_list_, X, y)

        return _cand_

    def _init_evo(self, _cand_, X, y):
        _p_list_ = self._init_individuals(_cand_)

        for _p_ in _p_list_:
            _p_.score_current = _cand_.eval_pos(_p_.pos_current, X, y)
            _p_.score_best = _p_.score_current

        return _p_list_


class Individual(BasePositioner):
    def __init__(self, eps=1):
        super().__init__(eps)
