from src.domain.services.i_id_generator import IIDGenerator
from snowflake import SnowflakeGenerator

class SnowflakeIDGenerator(IIDGenerator):
    def __init__(self,worker_id:int=1):
        self._generator:SnowflakeGenerator = SnowflakeGenerator(worker_id=worker_id)
    def generate(self) -> int:
        return next(self._generator)
    