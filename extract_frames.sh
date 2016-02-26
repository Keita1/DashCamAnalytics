#!/bin/sh
ffmpeg -i $1 -vf fps=0.01 $1.out%d.png
