#!/bin/bash
set -o errexit
/usr/sbin/nginx -g "error_log /dev/stdout info;"
exec "$@"