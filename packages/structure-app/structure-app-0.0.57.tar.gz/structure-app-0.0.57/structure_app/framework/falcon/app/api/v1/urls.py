from config import app
from config import api

from .views import (
    HealthCheckView
)

app.add_route(
    '/health',
    HealthCheckView()
)
