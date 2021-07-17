echo off
for %%a in ("*.measurements") do classify "%%a" "%%a" bottom --px2mm 0.034 -n 1 --limit4.0:20.0
pause