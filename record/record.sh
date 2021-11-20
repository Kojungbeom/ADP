#!/bin/bash

echo Enter Duration:
read duration
echo Enter Hardware Number:
read HW_num
echo Enter File Name:
read f_name
echo "$duration, $HW_num"

arecord $f_name -D $HW_num -f S16_LE -r 16000 -c 8 -d $duration
