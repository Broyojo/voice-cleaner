#!/bin/bash
set -e
#make sure you have installed libsox-fmt-all and sox
useffmpeg="0"
time="1"
while getopts "ft:" OPTION
do
    case $OPTION in
        f)
            echo "You set flag -f, using ffmpeg"
            useffmpeg="1"
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
read -p "do you want to chop up the audio files into 1 second bits? (y or n)" chopyn
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
if [ $chopyn == "n" ]  && [ $useffmpeg = "0" ] #sox option no split
then
    for i in $FILEPATHi*$extention ; do sox "$i" -b 16 -e signed-integer -r 44100 -c 1 "${i%.*}.raw" ; done
fi
if [ $chopyn == "n" ]  && [ $useffmpeg = "1" ] #ffmpeg option no split
then 
    for i in $FILEPATHi*$extention ; do ffmpeg -y  -i "$i"  -acodec pcm_s16le -f s16le -ac 1 -ar 44100 "${i%.*}.raw" ; done    
fi
if [ $chopyn == "y" ] && [ $useffmpeg = "0" ] #sox option split
then
    for i in $FILEPATHi*$extention ; do sox "$i" -b 16 -e signed-integer -r 44100 -c 1 "${i%.*}.raw"  trim 0 $time : newfile : restart ; done 
fi
if [ $chopyn == "y" ] && [ $useffmpeg = "1" ] #sox option split
then 
    echo "ffmpeg does not support file splitting into raw at the moment."
fi
exit
#$FILEPATHi*$extention
#todo: make it so that ffmpeg doesnt need to convert to raw first, it can just directly go to splitted form. sox does not work also
