#!/usr/bin/env python3

import functools
import pandas as pd
import numpy as np
import multiprocessing as mp
from MultiProcessDivision.divide import divide


class RelationAnimals():
    def __init__(self) -> None:
        pass

    def availableAnimals(self, relationAnimals:np.ndarray, relationColumns:np.ndarray) -> np.ndarray:
        splitted = [x.to_numpy() for x in divide(pd.Series(data=relationColumns), axis=0, series=True)]
        r = []
        to_execute = functools.partial(self.checkIfRelationExists, relationAnimals)
        with mp.Pool(processes=mp.cpu_count()) as pool:
            _r = [x for x in pool.map(to_execute,splitted)]
            _r = [_item for _sublist in _r for _item in _sublist]
            r.append(_r)
        return np.unique(r)

    def checkIfRelationExists(self, relationAnimals:np.ndarray, columnAnimals:np.ndarray) -> list:
        r = columnAnimals.tolist()
        for animal in columnAnimals:
            if animal not in relationAnimals:
                r.append(animal)
        return r