[link1](https://www.cyberciti.biz/faq/how-to-run-command-or-code-in-parallel-in-bash-shell-under-linux-or-unix)
[link2](https://zenodo.org/record/1146014)


# for file name ref
*TODO in Git Bash naming convention*
  
time find . -type f -name '*.*' | parallel trace {} {}.measurements



## Batch files
Used to be able to have an overview of the content of the `*.bat` (files)

They are usually run with:
1. whiskers
2. measure
3. classify (reclassify is usually not run)

#### BATCH WHISKERS
`echo off
for %%a in ("*.mp4") do trace "%%a" "%%~na.whiskers"
pause`

#### BATCH MEASURE 
`echo off
for %%a in ("*.whiskers") do measure --face bottom "%%a" "%%a.measurements"
pause`

#### BATCH CLASSIFY 
`echo off
for %%a in ("*.measurements") do classify "%%a" "%%a" bottom --px2mm 0.034 -n 1 --limit4.0:20.0
pause`

#### BATCH RECLASSIFY
`echo off
for %%a in ("*.measurements") do reclassify -n 1 "%%a" "%%a"
pause`
