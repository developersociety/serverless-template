#!/usr/bin/env bash
set -e

CURRENT_DATE=$(date +%Y%m%d)

sed -i.bak -e "s|CURRENT_DATE|${CURRENT_DATE}|g" zappa_settings.yaml
rm -f zappa_settings.yaml.bak
