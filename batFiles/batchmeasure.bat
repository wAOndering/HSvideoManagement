echo off
for %%a in ("*.whiskers") do measure --face bottom "%%a" "%%a.measurements"
pause