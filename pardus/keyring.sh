#!/bin/bash

cd $HOME

apt-get install debian-keyring debian-archive-keyring

echo "Download complete, importing keyrings..."

gpg --keyring trustedkeys.gpg --import /usr/share/keyrings/debian-archive-keyring.gpg

echo "Done. Listing keyrings..."

gpg --list-keys --keyring trustedkeys.gpg

#FIXME:
cp /usr/share/keyrings/debian-archive-keyring.gpg $HOME/.gnupg/trustedkeys.gpg 
