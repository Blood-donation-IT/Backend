from snowflake import SnowflakeGenerator
from src.domain.services.i_id_generator import IIDGenerator


class SnowflakeIDGenerator(IIDGenerator):
    def __init__(
        self,
        instance: int,
        timestamp: int = 946684800000,
        epoch: int = 0,
        seq: int = 0,
    ):
        self._generator = SnowflakeGenerator(
            instance=instance,
            timestamp=timestamp,
            epoch=epoch,
            seq=seq,
        )

    def generate(self) -> int:
        return next(self._generator)
