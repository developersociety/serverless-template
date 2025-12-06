import os
from pathlib import Path

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

# Add more Sentry data to help diagnose bugs
try:
    SENTRY_RELEASE = (
        (Path(__file__).resolve().parent.parent / Path(".sentry-release")).read_text().strip()
    )
except FileNotFoundError:
    SENTRY_RELEASE = None

if os.environ.get("SENTRY_DSN"):
    sentry_sdk.init(
        release=SENTRY_RELEASE,
        integrations=[AwsLambdaIntegration(timeout_warning=True)],
    )

app = Flask(__name__)

from . import views  # noqa:E402,F401
