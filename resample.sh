#!/bin/bash
set -e
#make sure you have installed libsox-fmt-all and sox
time="0.05"
br="32000"
test="0"
while getopts "sb:t:" OPTION
do
    case $OPTION in
        s)
            echo "Test resample"
            test=1
            ;;
        b)
            echo "The value of -b is $OPTARG"
            br=$OPTARG
            ;;
        t)
            echo "The value of -t is $OPTARG"
            time=$OPTARG
            ;;
        \?)
            echo "Use -f to enable ffmpeg, use -t [seconds] to modify trim time when trim is used. Default 1 second."
            exit
            ;;
    esac
done
echo "This is the audio conversion script, using ffmpeg. It will convert the input files into 44100 Hz, signed 16 bit audio files and output as raw PCM data. "
echo "*Important*: Make sure that you have *only* audio files in this directory" 
echo "This may take a long time and use a considerable amount of storage space" 
read -p "Enter extention of audio file. Include the \".\" (e.g., .wav .mp3 .flac)  "  extention
slash="/"
echo $extention
read -p "Type your input directory, (/path/to/directory/) " FILEPATHi
if [ ${FILEPATHi: -1} != "/" ] #append / if not already
then
    FILEPATHi="${FILEPATHi}/"
fi
echo $FILEPATHi
[ ! -d "$FILEPATHi" ] && echo "Directory $FILEPATHi DOES NOT exist." && exit #Throw exception if directory does not exist
read -p "Type your output directory (/path/to/directory/) " FILEPATHo
if [ ${FILEPATHo: -1} != "/" ]
then
    FILEPATHo="${FILEPATHo}/"
fi
echo $FILEPATHo
[ ! -d "$FILEPATHo" ] && echo "Directory $FILEPATHo DOES NOT exist." && exit

if [ $test == "0" ] #notest
then
     for i in $FILEPATHi*$extention ; do ffmpeg -i "$i" -acodec pcm_s32le -f sox -ac 1 -ar $br pipe: | sox -p -r 32000 -e signed-integer -b 16 -c 1 -t raw - | split -b 3200 -d --additional-suffix=.raw -a 10 - $FILEPATHo"${i%.*}" ; done 
fi

if [ $test == "1" ] #test
then 
    for i in $FILEPATHi*$extention ; do  ffmpeg -i "$i" -acodec pcm_s32le -f sox -ac 1 -ar $br pipe: | sox -p -r 44100 -e signed-integer -b 16 -c 1 $FILEPATHo"${i%.*}.wav" ; done 
fi
exit

#$FILEPATHi*$extention
#todo: make it so that ffmpeg doesnt need to convert to raw first, it can just directly go to splitted form. sox does not work also
