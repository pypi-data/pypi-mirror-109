#!/usr/bin/env python3

import pandas as pd
import numpy as np
from MultiProcessDivision.divide import divide
import multiprocessing as mp
import functools
import gc


class MissingYOB():
    def __init__(self):
        pass

    def missingYOB(self, animals:pd.DataFrame, data:pd.DataFrame) -> pd.DataFrame:
        splitted = divide(animals, axis=0)
        to_execute = functools.partial(self.mapYOB, data)
        with mp.Pool(processes=mp.cpu_count()) as pool:
            _res = pd.concat(
                [
                    x for x in pool.map(to_execute, splitted) if x is not None
                ], axis=0
            )
            data = pd.concat([data, _res], axis=0)
            del _res
            gc.collect()
        data = data[~data.index.duplicated(keep="last")]
        return data

    def mapYOB(self, animals:pd.DataFrame, data:pd.DataFrame) -> pd.DataFrame:
        _data = animals.groupby(animals.index).apply(
            lambda x: self.__assignYOB(animal=x, data=data)
        )
        return _data

    def __assignYOB(self, animal:pd.DataFrame, data:pd.DataFrame) -> pd.DataFrame:
        if animal.loc[:,"Sex"].to_numpy()[0] == 1 and animal.loc[:,"Year of Birth"].to_numpy()[0] == 0:
            sired_offspring_yob = data.loc[
                (data["Ear tag sire"] == np.unique(animal.index)[0]) &
                (data["Year of Birth"] != 0), "Year of Birth"
            ]
            if sired_offspring_yob.size > 0:
                data.loc[np.unique(animal.index)[0], "Year of Birth"] = np.min(sired_offspring_yob.to_numpy())[0] - 3
                data.loc[
                    (data["Year of Birth sire"] == 0) & 
                    (data["Ear tag sire"] == np.unique(animal.index)[0]),
                    "Year of Birth sire"] = np.min(sired_offspring_yob.to_numpy())[0] - 3
                r = pd.DataFrame()
                r = pd.concat([r, data.loc[np.unique(animal.index)[0],:]], axis=0)
                r = pd.concat(
                    [
                        r, 
                        data.loc[data["Ear tag sire"] == np.unique(animal.index)[0],:]
                    ], axis=0
                )
                return r
        if animal.loc[:,"Sex"].to_numpy()[0] == 2 and animal.loc[:,"Year of Birth"].to_numpy()[0] == 0:
            damed_offspring_yob = data.loc[
                (data["Ear tag dam"] == np.unique(animal.index)[0]) &
                (data["Year of Birth"] != 0), "Year of Birth"
            ]
            if damed_offspring_yob.size > 0:
                data.loc[np.unique(animal.index)[0], "Year of Birth"] = np.min(damed_offspring_yob.to_numpy())[0] - 3
                data.loc[
                    (data["Year of Birth dam"] == 0) & 
                    (data["Ear tag dam"] == np.unique(animal.index)[0]),
                    "Year of Birth dam"] = np.min(damed_offspring_yob.to_numpy())[0] - 3
                r = pd.DataFrame()
                r = pd.concat([r, data.loc[np.unique(animal.index)[0],:]], axis=0)
                r = pd.concat(
                    [
                        r, 
                        data.loc[data["Ear tag dam"] == np.unique(animal.index)[0],:]
                    ], axis=0
                )
                return r
            
