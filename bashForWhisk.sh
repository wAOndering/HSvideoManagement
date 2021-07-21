#[link1](https://www.cyberciti.biz/faq/how-to-run-command-or-code-in-parallel-in-bash-shell-under-linux-or-unix)
#[link2](https://zenodo.org/record/1146014)

## Batch files
#Used to be able to have an overview of the content of the `*.bat` (files)

#They are usually run with:
#1. whiskers
#2. measure
#3. classify (reclassify is usually not run)

#########################################
# Shell script in Gitbash with parallel
#########################################
# for file name ref
#TODO in Git Bash naming convention*
  
time find . -type f -name '*49_l*_p[1-3]*.mp4' | parallel trace {} {}.measurements
time find . -type f -name '49_l*_p[1-3]*.mp4' | parallel trace {} {}.measurements # this is good to test echo is equivalent of print

time find . -type f -name '*.mp4' | parallel trace {} {.}.whiskers
time find . -type f -name '*.whiskers' | parallel measure --face bottom {} {.}.measurements
time find . -type f -name '*.measurements' | parallel classify {} {} bottom --px2mm 0.034 -n 1 --limit4.0:20.0


#########################################
# Shell script for bat files 
#########################################
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
