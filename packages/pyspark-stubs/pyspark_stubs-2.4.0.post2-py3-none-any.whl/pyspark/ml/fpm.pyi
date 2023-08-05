from typing import Any, Optional, Type, TypeVar
from pyspark.ml.util import *
from pyspark.ml.wrapper import JavaEstimator, JavaParams, JavaModel
from pyspark.ml.param.shared import *
from pyspark.sql.dataframe import DataFrame

P = TypeVar("P")

class HasSupport(Params):
    minSupport = ...  # type: Param
    def setMinSupport(self: P, value: float) -> P: ...
    def getMinSupport(self) -> float: ...

class HasConfidence(Params):
    minConfidence = ...  # type: Param
    def setMinConfidence(self: P, value: float) -> P: ...
    def getMinConfidence(self) -> float: ...

class HasItemsCol(Params):
    itemsCol = ...  # type: Param
    def setItemsCol(self: P, value: str) -> P: ...
    def getItemsCol(self) -> str: ...

class FPGrowthModel(JavaModel, JavaMLWritable, JavaMLReadable):
    @property
    def freqItemsets(self) -> DataFrame: ...
    @property
    def associationRules(self) -> DataFrame: ...

class FPGrowth(JavaEstimator[FPGrowthModel], HasItemsCol, HasPredictionCol, HasSupport, HasConfidence, JavaMLWritable, JavaMLReadable):
    def __init__(self, minSupport: float = ..., minConfidence: float = ..., itemsCol: str = ..., predictionCol: str = ..., numPartitions: Optional[int] = ...) -> None: ...
    def setParams(self, minSupport: float = ..., minConfidence: float = ..., itemsCol: str = ..., predictionCol: str = ..., numPartitions: Optional[int] = ...) -> FPGrowth: ...

class PrefixSpan(JavaParams):
    minSupport = ...  # type: Param
    maxPatternLength = ...  # type: Param
    maxLocalProjDBSize = ...  # type: Param
    sequenceCol = ...  # type: Param
    def __init__(self, minSupport: float = ..., maxPatternLength: int = ..., maxLocalProjDBSize: int = ..., sequenceCol: str = ...) -> None: ...
    def setParams(self, minSupport: float = ..., maxPatternLength: int = ..., maxLocalProjDBSize: int = ..., sequenceCol: str = ...) -> PrefixSpan: ...
    def findFrequentSequentialPatterns(self, dataset: DataFrame) -> DataFrame: ...
