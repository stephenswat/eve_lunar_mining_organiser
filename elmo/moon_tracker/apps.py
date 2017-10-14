from django.apps import AppConfig


class MoonTrackerConfig(AppConfig):
    name = 'moon_tracker'
    verbose_name = 'Moon Scan Tracker'

    def ready(self):
        import moon_tracker.signals
