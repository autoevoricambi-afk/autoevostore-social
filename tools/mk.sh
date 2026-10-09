#!/bin/bash
# usage: mk.sh name
n=$1; D=3.4; F=0.5
files=($n/s*.png); k=${#files[@]}
inputs=""; filt=""
for i in $(seq 0 $((k-1))); do
  inputs="$inputs -loop 1 -t $D -i $n/s$i.png"
  filt="$filt[$i:v]scale=1080:1920,zoompan=z='min(zoom+0.0006,1.06)':d=$(python3 -c "print(int($D*30))"):x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p[v$i];"
done
prev="v0"; off=0
for i in $(seq 1 $((k-1))); do
  off=$(python3 -c "print(round($i*($D-$F),2))")
  filt="$filt[$prev][v$i]xfade=transition=fade:duration=$F:offset=$off[x$i];"
  prev="x$i"
done
total=$(python3 -c "print(round($k*$D-($k-1)*$F,2))")
ffmpeg -y -loglevel error $inputs -f lavfi -t $total -i anullsrc=r=44100:cl=stereo -filter_complex "${filt%;}" -map "[$prev]" -map $k:a -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r 30 -c:a aac -b:a 96k -movflags +faststart -shortest $n.mp4
echo $n $total
