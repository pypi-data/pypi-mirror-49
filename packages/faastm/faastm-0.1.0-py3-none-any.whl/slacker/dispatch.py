import logging
from .persist import load, save, STMError
from .service import CommittingService


LOG = logging.getLogger(__name__)


class Dispatcher:
    def __init__(self, srv=None, default=None, factory=None, signer=None, namespace=None, bucket=None):
        self.srv = srv
        self.default = default
        self.factory = factory
        self.signer = signer
        self.namespace = namespace
        self.bucket = bucket

    def dispatch(self, sender=None, channel=None, receivers=None, text=None):
        while True:
            LOG.debug("attempting to dispatch message %s", text)
            try:
                obj = load(channel.id, default=self.default, factory=self.factory,
                           signer=self.signer, namespace=self.namespace, bucket=self.bucket)
            except Exception as e:
                LOG.exception("something happened when constructing object to dispatch to %r", e)
                return
            LOG.debug("sending to %s", obj)
            srv = CommittingService(delegate=self.srv)
            if obj.on_message(srv=srv, sender=sender, channel=channel, receivers=receivers, text=text):
                # We have to save
                try:
                    save(channel.id, obj,
                         signer=self.signer, namespace=self.namespace, bucket=self.bucket)
                except STMError:
                    LOG.debug("STMError during commit, retrying message processing")
                    continue
            # We successfully saved (if required), so commit any pending messages to the external service
            srv.commit()
            return
