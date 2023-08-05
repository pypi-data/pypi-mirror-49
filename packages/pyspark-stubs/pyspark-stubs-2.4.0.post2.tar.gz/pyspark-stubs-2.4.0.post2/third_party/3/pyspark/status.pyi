# Stubs for pyspark.status (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class SparkJobInfo: ...
class SparkStageInfo: ...

class StatusTracker:
    def __init__(self, jtracker) -> None: ...
    def getJobIdsForGroup(self, jobGroup: Optional[Any] = ...): ...
    def getActiveStageIds(self): ...
    def getActiveJobsIds(self): ...
    def getJobInfo(self, jobId): ...
    def getStageInfo(self, stageId): ...
