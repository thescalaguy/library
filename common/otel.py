import time
from contextlib import contextmanager

from opentelemetry import metrics
from opentelemetry.metrics import Counter, Histogram
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)

_default_attributes = {"env": "dev"}
_export_interval_millis = 1 * 1e3  # 1 second
_exporter = ConsoleMetricExporter()
_metric_reader = PeriodicExportingMetricReader(exporter=_exporter, export_interval_millis=_export_interval_millis)
_provider = MeterProvider(metric_readers=[_metric_reader])

# Sets the global default meter provider
metrics.set_meter_provider(_provider)

# Creates a meter from the global meter provider
_meter = metrics.get_meter("my.meter.name")


def create_counter(name: str, unit: str, description: str) -> Counter:
    return _meter.create_counter(
        name=name,
        unit=unit,
        description=description
    )


def create_histogram(name: str, unit: str, description: str) -> Histogram:
    return _meter.create_histogram(
        name=name,
        unit=unit,
        description=description,
    )


@contextmanager
def timed(histogram: Histogram, attributes: dict[str, str] | None = None):
    t1 = time.perf_counter_ns()
    yield
    t2 = time.perf_counter_ns()
    amount = t2 - t1
    histogram.record(amount=amount, attributes=_attributes(attributes))


def increment_counter(counter: Counter, attributes: dict[str, str] | None = None) -> None:
    counter.add(amount=1, attributes=_attributes(attributes))


def _attributes(attributes: dict[str, str] | None = None) -> dict[str, str]:
    return {**attributes, **_default_attributes} if attributes else _default_attributes
