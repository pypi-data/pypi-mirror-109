import time
from ..flows.internals.base_operator import BaseOperator
from ..data import Reader
from ..data.formats import json
from ..errors.time_exceeded import TimeExceeded


class ReaderOperator(BaseOperator):
    def __init__(
        self, *args, time_out: int = -1, signal_format: str = "{cursor}", **kwargs
    ):
        """
        This reader which will stop reading after a given time.

        Parameters:
            time_out: integer (optional)
                The number of seconds to run before bailing, default is -1, which is
                treated as 1 year (non-leap)
            signal_format: string (optional)
                The format of the detail in the exception. The default is '{cursor}'
                which is replaced with the reader cursor value.
        Yields:
            tuple

        Raises:
            TimeExceeded
        """
        super().__init__(*args, **kwargs)
        self.reader = Reader(**kwargs)
        if time_out < 0:
            time_out = 315569652  # one year (365 days)
        self.time_out = time_out + time.time()
        self.signal_format = signal_format

    def execute(self, data, context):
        for row in self.reader:
            if time.time() > self.time_out:
                signal = self.signal_format.replace(
                    "{cursor}", json.serialize(self.reader.cursor)
                )
                raise TimeExceeded(signal)
            yield row, context
