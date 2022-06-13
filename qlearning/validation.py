import numpy as np
import geopandas as gpd
from shapely import polygon
from functools import partial
from abc import ABC, abstractmethod

class ValidatorInterface(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def is_valid():
        pass

class IsGeoDataFrameValidator(ValidatorInterface):

    def __init__(self, featureclass: gpd.GeoDataFrame):
        self.featureclass = featureclass

    def is_valid(self) -> bool:
        return isinstance(self.featureclass, gpd.GeoDataFrame)

class IsNotEmptyValidator(ValidatorInterface):

    def __init__(self, featureclass: gpd.GeoDataFrame):
        self.featureclass = featureclass

    def is_valid(self) -> bool:
        return self.featureclass.empty

class HasIOPColumnValidator(ValidatorInterface):

    def __init__(self, featureclass: gpd.GeoDataFrame, column_name:str) -> bool:
        self.featureclass = featureclass
        self.column_name = column_name

    def is_valid(self) -> bool:
        return self.column_name in self.featureclass.columns

class HasIOPFloatValuesValidator(ValidatorInterface):

    def __init__(self, featureclass: gpd.GeoDataFrame, column_name:str) -> bool:
        self.featureclass = featureclass
        self.column_name = column_name

    def is_valid(self) -> bool:
        # TODO: Sprawdzić czy .dtype zwraca typ czy jakieś inne gówno
        return np.issubdtype(self.fetureclass[self.column_name].dtype,
                             np.floating)

class HasNormalizedValuesValidator(ValidatorInterface):

    def __init__(self, featureclass: gpd.GeoDataFrame, column_name:str) -> bool:
        self.featureclass = featureclass
        self.column_name = column_name

    def is_valid(self) -> bool:
        _min = min(self.featureclass[self.column_name].values)
        _max = max(self.featureclass[self.column_name].values)
        return -1 <= _min <= _max <= 1

class HasGeometryColumnValidator(ValidatorInterface):

    def __init__(self, featureclass: gpd.GeoDataFrame):
        self.featureclass = featureclass

    def is_valid(self) -> bool:
        return 'geometry' in self.featureclass.columns

class IsPolygonGeometryValidator(ValidatorInterface):

    def __init__(self, featureclass: gpd.GeoDataFrame):
        self.featureclass = featureclass

    def is_valid(self) -> bool:
        return any(map(lambda x: isinstance(x, Polygon), class_or_tuple=Polygon), self.fetureclass.geometry)

class IsCompleteGridValidator(ValidatorInterface):

    pass
