#!/bin/bash
set -e
#make sure you have installed libsox-fmt-all and sox and ffmpeg
useffmpeg="0"
time="1"
noiselvl="0.02"
codecin="1"
codecrandom="0"
br="13000"
noiserandom="0"
slow="2"
#num_processes=5
#number to codec
function nosplit () {
pthrm="${i:rmlen}" #remove the length from i and store in new var
	if [ $codecrandom == "1" ] #enable randomization of codecs?
	then
		codecin="$((1 + $RANDOM % $slow))"
		numtocodec
		echo $codec
	fi

	if [ $noiserandom == "1" ] #enable randomization of noise levels?
	then 
		noiselvl="0.0$(((1+ $RANDOM%9)))" #random noise levels between 0.01 and 0.09
	fi
	echo $pthrm
	echo $FILEPATHo"${pthrm%.*}"
	 sox "$i" -p synth whitenoise vol $noiselvl | sox -m "$i" - -r 44100 -c 1 -t wav - | ffmpeg -y -i pipe: -codec $codec  -ac 1 -ar 8000 -ab $br -f $codec2 pipe: |  ffmpeg -f $codec2 -i pipe: -acodec pcm_s16le -f s16le -ac 1 -ar 44100 $FILEPATHo"${pthrm%.*}.raw"
}

function splitting () {
pthrm="${i:rmlen}" #remove the length from i and store in new var
	if [ $codecrandom == "1" ] #enable randomization of codecs?
	then
		codecin="$((1 + $RANDOM % $slow))"
		numtocodec
	fi

	if [ $noiserandom == "1" ] #enable randomization of noise levels?
	then 
		noiselvl="0.0$(((1+ $RANDOM%9)))" #random noise levels between 0.01 and 0.09
	fi

	 sox "$i" -p synth whitenoise vol $noiselvl | sox -m "$i" - -r 44100 -c 1 -t wav - | ffmpeg -y -i pipe: -codec $codec  -ac 1 -ar 8000 -ab $br -f $codec2 pipe: | ffmpeg -f $codec2 -i pipe: -acodec pcm_s32le -f sox -ac 1 -ar 44100 pipe: | sox -p -r 44100 -e signed-integer -b 16 -c 1 $FILEPATHo"${pthrm%.*}.raw" trim 0 $time : newfile : restart
}

function numtocodec () {
  if [ $codecin == "1" ] 
  then
	codec="gsm"
	codec2="gsm"
	br="13000"
  fi
  if [ $codecin == "3" ]  #this one is 3 now apparently
  then 
	codec="g723_1"
	codec2="g723_1"
	br="6300"
  fi
  if [ $codecin == "2" ]
  then
	codec="g726"
	codec2="wav"
	br="16000"
  fi
}

while getopts "esrt:c:" OPTION
do
	case $OPTION in
		e)
			echo "You set flag -e, codecs random, -c not effective"
			codecrandom="1"
			;;
		s)
			echo "You set flag -s, codecs random includes g732.1 Warning: slow!"
			slow="3"
			;;
		r)
			echo "You set flag -r, noise levels random"
			noiserandom="1"
			;;
		t)
			echo "The value of -t is $OPTARG"
			time=$OPTARG
			;;
		c)
			echo "The value of -c is $OPTARG"
			codecin=$OPTARG
			;;
		\?)
			echo "Use -f to enable ffmpeg, use -t [seconds] to modify trim time when trim is used. Default 1 second. use -e to randomize codecs. Use -r to randomize noise levels. Use -c to specify a codec. 1: gsm 2: G726 3: G723_1. -s enabe g732_1 codec during randomization (slow!)"
			exit
			;;
	esac
done

echo "This is the audio conversion compression It will compress the files with chosen codec, then convert to 44100 Hz, signed 16 bit audio files and output as raw PCM data. "
echo "*Important*: Make sure that you have *only* audio files in this directory" 
echo "This may take a long time and use a considerable amount of storage space" 
#read -p "Enter extention of audio file. Include the \".\" (e.g., .wav .mp3 .flac)  "  extention
slash="/"
#echo $extention
read -p "do you want to chop up the audio files into bits? (y or n)" chopyn
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


if [ $chopyn == "n" ]  #no split
then
	numtocodec
rmlen=${#FILEPATHi} #length of filepath
	for i in $FILEPATHi*
	do
	#((j=j%num_processes)); ((j++==0)) && wait
	nosplit & 
done
wait
fi



if [ $chopyn == "y" ] #split
then

	numtocodec
rmlen=${#FILEPATHi} #length of filepath
	for i in $FILEPATHi*
	do
	splitting &
done
wait
fi







exit
#$FILEPATHi*$extention
#todo: convert + split on a single line? FFMPEG extra codecs? Random noise volumes? Random codecs?
# w ffmpeg, GSM: GSM, GSM, raw
#G726: G726, wav, wav, raw
#G723_1: G723_1, G723_1, G723_1, raw *or* G723_1, wav, wav, raw
#extra codecs?
#flag paths?
#letter codecs?
#Carpetbugs




