from django.dispatch import Signal

notify = Signal(providing_args=[  # pylint: disable=invalid-name
    'recipient', 'sender', 'verb', 'action_object', 'target', 'description',
    'timestamp', 'level', 'start_date', 'end_date', 'target_audience', 'is_sent',
])
