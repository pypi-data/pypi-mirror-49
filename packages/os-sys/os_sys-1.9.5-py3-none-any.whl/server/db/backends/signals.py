from server.dispatch import Signal

connection_created = Signal(providing_args=["connection"])
