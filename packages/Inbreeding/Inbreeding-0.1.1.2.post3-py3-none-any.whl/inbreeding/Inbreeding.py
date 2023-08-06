#!/usr/bin/python3

import functools
import pandas as pd
import numpy as np
import multiprocessing as mp
from MultiProcessDivision.divide import divide
import gc


class Inbreeding():
    def __init__(self):
        pass

    def inbreedingCalculation(self, animals:pd.DataFrame) -> pd.DataFrame:
        splitted = divide(animals, axis=0)
        animals.loc[:,"Inbreeding"] = np.zeros(animals.index.size)
        while True:
            res = pd.Series()
            to_execute = functools.partial(self.applyInbreeding, animals)
            with mp.Pool(processes=mp.cpu_count()) as pool:
                _res = pd.concat(
                    [x for x in pool.map(to_execute, splitted) if x is not None],
                    axis=0
                )
                res = pd.concat([res, _res], axis=0)
            animals = animals.assign(
                Inbreeding = lambda animal: res.loc[animal.index]
            )
            if "previous" in locals():
                print(res, res.mean(), sep="\n\n")
                absdiff = np.abs(
                    previous.mean() - res.mean()
                )
                if absdiff < 1e-1:
                    return animals
                else:
                    previous = res
                    del res
                    gc.collect()
            else:
                previous = res
                del res
                gc.collect()

    def applyInbreeding(self, selectedAnimals:pd.DataFrame, allAnimals:pd.DataFrame) -> pd.Series:
        r = selectedAnimals.apply(
            lambda animal: self.__inbreedCoeff(animal, allAnimals),
            axis=1
        )
        r.name = "Inbreeding"
        return r

    def __inbreedCoeff(self, animal:pd.DataFrame, allAnimals:pd.DataFrame) -> pd.Series:
        try:
            sireIndex = np.where(allAnimals.index == animal.loc[:,"Ear tag sire"]) + 1
        except KeyError:
            sireIndex = 0
        try:
            damIndex = np.where(allAnimals.index == animal.loc[:,"Ear tag dam"]) + 1
        except KeyError:
            damIndex = 0
        if sireIndex <= 0 or damIndex <= 0:
            try:
                averageSire = allAnimals.loc[
                    allAnimals["Year of Birth"] == allAnimals.loc[
                        animal.loc[:,"Ear tag sire"],"Year of Birth"
                    ],"Inbreeding"
                ].mean()
            except KeyError:
                averageSire = 0
            try:
                averageDam = allAnimals.loc[
                    allAnimals["Year of Birth"] == allAnimals.loc[
                        animal.loc[:,"Ear tag dam"],"Year of Birth"], "Inbreeding"
                ].mean()
            except KeyError:
                averageDam = 0
            return pd.Series(
                data=np.min(abs(averageDam), abs(averageSire)),
                index=animal.loc[:,"Ear tag"].to_numpy()[0],
                name="Inbreeding"
            )
        else:
            return pd.Series(
                data=0.5*self.__cffa(
                    sire=animal.loc[:,"Ear tag sire"], 
                    dam=animal.loc[:,"Ear tag dam"], 
                    allAnimals=allAnimals
                ),
                index=animal.loc[:,"Ear tag"].to_numpy()[0],
                name="Inbreeding"
            )

    def __cffa(self, sire:np.int64, dam:np.int64, allAnimals:pd.DataFrame) -> np.float64:
        """
        Even though this function yields its results from index values instead of 
        ear tag values, the parameters for sire and dam are always (!!!) ear tag values and 
        never (!!!) index values
        """
        try:
            sireIndex = np.where(allAnimals.index == sire) + 1
        except KeyError:
            sireIndex = 0
        try:
            damIndex = np.where(allAnimals.index == dam) + 1
        except KeyError:
            damIndex = 0
        try:
            sireAverage = allAnimals.loc[
                allAnimals["Year of Birth"] == allAnimals.loc[sire,"Year of Birth"],
                "Inbreeding"
            ].mean()
        except KeyError:
            sireAverage = 0
        try:
            damAverage = allAnimals.loc[
                allAnimals["Year of Birth"] == allAnimals.loc[dam,"Year of Birth"],
                "Inbreeding"
            ].mean()
        except KeyError:
            damAverage = 0
        if sireIndex <= 0 or damIndex <= 0:
            return 2*min(damAverage, sireAverage)
        elif sireIndex == damIndex:
            return 1 + allAnimals.loc[sire,"Inbreeding"]
        elif sireIndex < damIndex:
            try:
                damsSire = allAnimals.loc[dam, "Ear tag sire"]
            except KeyError:
                damsSire = 0
            try:
                damsDam = allAnimals.loc[dam, "Ear tag dam"]
            except KeyError:
                damsDam = 0
            inb = 0.5*self.__cffa(
                    sire=sire, dam=damsSire, allAnimals=allAnimals
                ) + self.__cffa(sire=sire, dam=damsDam, allAnimals=allAnimals)
            return inb
        else:
            try:
                siresSire = allAnimals.loc[sire, "Ear tag sire"]
            except KeyError:
                siresSire = 0
            try:
                siresDam = allAnimals.loc[sire, "Ear tag dam"]
            except KeyError:
                siresDam = 0
            inb = 0.5*self.__cffa(
                    sire=dam, dam=siresSire, allAnimals=allAnimals
                ) + self.__cffa(sire=dam, dam=siresDam, allAnimals=allAnimals)
