from django.apps import AppConfig


class MoonTrackerConfig(AppConfig):
    name = 'moon_tracker'

    def ready(self):
        import moon_tracker.signals
