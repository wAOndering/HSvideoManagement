echo off
for %%a in ("*.measurements") do reclassify -n 1 "%%a" "%%a"
pause