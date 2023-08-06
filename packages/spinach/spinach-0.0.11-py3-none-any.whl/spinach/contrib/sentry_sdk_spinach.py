from sentry_sdk.hub import Hub
from sentry_sdk.integrations import Integration

from spinach import signals


class SpinachIntegration(Integration):
    """Register the Sentry SDK integration.

    Exceptions making jobs fail are sent to Sentry.

    :param send_retries: whether to also send to Sentry exceptions resulting
           in a job being retried
    """

    identifier = 'spinach'

    def __init__(self, send_retries: bool=False):
        self.send_retries = send_retries

    @staticmethod
    def setup_once():
        signals.job_started.connect(_job_started)
        signals.job_finished.connect(_job_finished)
        signals.job_failed.connect(_job_failed)
        signals.job_schedule_retry.connect(_job_schedule_retry)


def _job_started(namespace, job, **kwargs):
    hub = Hub.current
    hub.push_scope()
    with hub.configure_scope() as scope:
        scope.transaction = job.task_name
        scope.clear_breadcrumbs()


def _job_finished(namespace, job, **kwargs):
    hub = Hub.current
    hub.pop_scope_unsafe()


def _job_failed(namespace, job, **kwargs):
    hub = Hub.current
    with hub.configure_scope() as scope:
        for attr in job.__slots__:
            scope.set_extra(attr, getattr(job, attr))
    hub.capture_exception()


def _job_schedule_retry(namespace, job, **kwargs):
    hub = Hub.current
    integration = hub.get_integration(SpinachIntegration)
    if integration is None:
        return

    if integration.send_retries is False:
        return

    with hub.configure_scope() as scope:
        for attr in job.__slots__:
            scope.set_extra(attr, getattr(job, attr))
    hub.capture_exception()
