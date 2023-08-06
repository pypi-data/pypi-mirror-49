@echo off

:: We do support UTF-8 encoding only.
SET PYTHONIOENCODING=UTF-8
python -m neptune.internal.cli.main %*
