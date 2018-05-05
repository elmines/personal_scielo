#!/bin/bash

TITLE=es-en-gma-biological
SOURCE_LANG=es
DEST_LANG=en

TAR=${TITLE}.tar

ORIG_DIR=`pwd`
TAR_PATH=$ORIG_DIR/$TAR

TEMP_DIR=/scratch-local/ualelm
mkdir $TEMP_DIR
cd $TEMP_DIR

python3 $ORIG_DIR/gen_corpora.py --tar   $TAR_PATH               \
                                 --langs $SOURCE_LANG $DEST_LANG \
                                 --title $TITLE
cp ${TITLE}.$SOURCE_LANG $ORIG_DIR/
cp ${TITLE}.$DEST_LANG $ORIG_DIR/
cd $ORIG_DIR
rm -rf $TEMP_DIR
