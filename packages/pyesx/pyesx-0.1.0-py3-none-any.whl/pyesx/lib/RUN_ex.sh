#!/usr/bin/env bash

# Sets up ESX for some common applications
# Sorry, bash scripts ain't reader-friendly...

#bindir=`dirname $0`   # finds ecosx/scripts directory

echo "start"

#------------------ PATH SETUP ----------------------------
#==========================================================
cdir="$PWD"           # set ecosx/esx_src   directory NEW: ecosx/esx/RUN
hdir="$(dirname "$(dirname "$(dirname "$(dirname "$(dirname "$PWD")")")")")"  #" finds ecosx directory
chemscripts="$hdir/chem/scripts"  # ecosx/chem/scripts directory (do.GenChem)
chembase="$hdir/chem/base_mechanismes"
chemextra="$hdir/chem/extra_mechanismes"
esdir="$hdir/esx/scripts"   # ecosx/esx/scripts directory (do.Makefile)
esrcdir="$hdir/esx/src"
esrcsafedir="$hdir/esx/src.safe" 
edatdir="$hdir/esx/"    
exdir="$hdir/esx/projects"  
out="output"


echo  SRC $chemscripts

cd $esrcdir 

make clean
rm *.o *.mod  # Since make clean alone didn't always do it!

cd $esrcsafedir 


cd $esrcdir  
#----------------- PROJECT DEFINITION ----------------------
#==========================================================
proj=$1                        # Name of the project 

exppath="$exdir/$proj/experiments"
outpath="$exdir/$proj/$out"
datapath="$exdir/$proj/data"

#----------- EXPERIENCES DEFINITIONS AND RUN ---------------------
#=================================================================
exp=$2                        # Name of the experimental serie 

#************  EXP1  ***************
# 1. CONFIGURATION FILES :
#-------------------------
cp $exppath/$exp/ESXFILE  $esrcdir/config_esx.nml          # Put in source 
cp $exppath/$exp/VEGFILE  $esrcdir/config_Veg.nml          # Put in source 
cp $exppath/$exp/LOCFILE  $esrcdir/config_Local.nml          # Put in source

# 2. CHEMICAL SCHEME :
#----------------------

if [ "$3" = 'T' ]; then
  $chemscripts/do.GenChem -b BOSCOChem -e BOSCOBVOC_EmChem16x BOSCOTracers
fi

# 3. EXTERNDATA FILES : (PreProcessed ?) 
#---------------------
cp $datapath/DATAFILE  $esrcdir/ExternData.csv

# 4. RUN PART : 
#--------------
if [ "$3" = 'T' ]; then
  make clean
  rm *.o *.mod  # Since make clean alone didn't always do it!
  $esdir/do.Makefile
  make
  chmod a+x esx_Main
fi 

# Run from the source directory and output in the output directory of the experience
./esx_Main > $outpath/RES_RUNNAME

