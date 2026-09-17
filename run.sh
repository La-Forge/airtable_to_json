#!/bin/sh
# Wrapper for the scheduled task.
#
# The heartbeat is pushed whatever the outcome, and the script exits with the
# export's own status. Chaining the push behind `&&` -- as the host crontab did
# -- means a failure pushes nothing, which is indistinguishable from a run that
# has not started yet. That hid a dead job here for days.

python3 /app/export.py
rc=$?

if [ "$rc" -eq 0 ]; then
    status=up
    msg=OK
else
    status=down
    msg=FAILED
fi

if [ -n "$UPTIME_KUMA_PUSH_URL" ]; then
    wget -q -O /dev/null -T 15 "${UPTIME_KUMA_PUSH_URL}?status=${status}&msg=${msg}-rc${rc}" || true
fi

exit "$rc"
