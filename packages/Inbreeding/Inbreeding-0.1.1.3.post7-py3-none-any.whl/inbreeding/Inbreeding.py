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
            to_execute = functools.partial(
                self.applyInbreeding, allAnimals=animals
            )
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
            lambda animal: self.__inbreedCoeff(animal=animal, allAnimals=allAnimals),
            axis=1
        )
        r.name = "Inbreeding"
        return r

    def __inbreedCoeff(self, animal:pd.Series, allAnimals:pd.DataFrame) -> pd.Series:
        etSire = animal.loc["Ear tag sire"]
        etDam = animal.loc["Ear tag sire"]
        if etSire != 0:
            try:
                print(
                    sireIndex = allAnimals.index[
                        allAnimals[allAnimals["Ear tag"] == etSire]
                    ].tolist()
                )
                sireIndex = allAnimals.index[
                    allAnimals[allAnimals["Ear tag"] == etSire]
                ].tolist()[0] + 1
                #sireIndex = np.where(allAnimals.index == animal.loc[:,"Ear tag sire"]) + 1
            except KeyError:
                sireIndex = 0
        else:
            sireIndex = 0
        if etDam != 0:
            try:
                print(
                    sireIndex = allAnimals.index[
                        allAnimals[allAnimals["Ear tag"] == etDam]
                    ].tolist()
                )
                damIndex = allAnimals.index[
                    allAnimals[allAnimals["Ear tag"] == etDam]
                ].tolist()[0] + 1
            except KeyError:
                damIndex = 0
        else:
            damIndex = 0
        
        if sireIndex <= 0 or damIndex <= 0:
            if sireIndex != 0:
                sireYOB = allAnimals.loc[sireIndex,"Year of Birth"]
                try:
                    averageSire = allAnimals.loc[
                        allAnimals["Year of Birth"] == sireYOB,
                        "Inbreeding"
                    ].mean()
                except KeyError:
                    averageSire = 0
            else:
                averageSire = 0
            if damIndex != 0:
                damYOB = allAnimals.loc[damIndex, "Year of Birth"]
                try:
                    averageDam = allAnimals.loc[
                        allAnimals["Year of Birth"] == damYOB,
                        "Inbreeding"
                    ].mean()
                except KeyError:
                    averageDam = 0
            else:
                averageDam = 0
            return pd.Series(
                data=np.min(abs(averageDam), abs(averageSire)),
                index=animal.loc["Ear tag"],
                name="Inbreeding"
            )
        else:
            inbreedCoeff = 0.5*self.__cffa(
                    sire=animal.loc["Ear tag sire"], 
                    dam=animal.loc["Ear tag dam"], 
                    allAnimals=allAnimals
                )
            return pd.Series(
                data=inbreedCoeff,
                index=animal.loc["Ear tag"],
                name="Inbreeding"
            )

    def __cffa(self, sire:np.int64, dam:np.int64, allAnimals:pd.DataFrame) -> np.float64:
        """
        Even though this function yields its results from index values instead of 
        ear tag values, the parameters for sire and dam are always (!!!) ear tag values and 
        never (!!!) index values
        """
        try:
            sireIndex = allAnimals.index[allAnimals[allAnimals["Ear tag"] == sire]][0] + 1
        except KeyError:
            sireIndex = 0
        try:
            damIndex = allAnimals.index[allAnimals[allAnimals["Ear tag"] == dam]][0] + 1
        except KeyError:
            damIndex = 0
        if sireIndex != 0:
            try:
                sireAverage = allAnimals.loc[
                    allAnimals["Year of Birth"] == allAnimals.loc[sireIndex,"Year of Birth"],
                    "Inbreeding"
                ].mean()
            except KeyError:
                sireAverage = 0
        else:
            sireAverage = 0
        if damIndex != 0:
            try:
                damAverage = allAnimals.loc[
                    allAnimals["Year of Birth"] == allAnimals.loc[damIndex,"Year of Birth"],
                    "Inbreeding"
                ].mean()
            except KeyError:
                damAverage = 0
        else:
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
