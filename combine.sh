cat *.raw > fout.raw
sox -t raw -r 44100 -b 16 -c 1 -L -e signed-integer ./fout.raw output.wav