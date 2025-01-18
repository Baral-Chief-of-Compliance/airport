#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

echo yes | python3 manage.py collectstatic
gunicorn --timeout=70 -b 0.0.0.0:8000 airoport_project.wsgi