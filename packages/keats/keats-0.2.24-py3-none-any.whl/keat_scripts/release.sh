#!/usr/bin/env bash

EMOJI="\xE2\x9C\xA8 \xF0\x9F\x8C\xB2 \xE2\x9C\xA8"
SEP="*****"
CURRENT=$(poetry run keats v)
NAME=$(poetry run keats package)
COLOR="\e[1;31m"
CINPUT="\e[32m"
CWARN="\e[1;31m"
CINFO="\e[34m"
END="\e[0m"

COMMIT=0
PUSH=0
REPO=""
VERSION=""

echo "$EMOJI $NAME $CURRENT $EMOJI"

################################
# Version
################################
printf "$CINPUT Version (or bump): $END"
read input
if [ "$input" != "" ]; then
    VERSION=$input
fi

poetry run keats bump $VERSION
VERSION=$(poetry run keats v)
################################
# Setup
################################
printf "$CINPUT Commit changes to git (y/[n]): $END"
read input
if [ "$input" == "y" ]; then
    COMMIT=1
fi

if [ "$COMMIT" == 1 ]; then
    printf "$CINPUT Add a commit message prefix?: $END"
    read PREFIX

    printf "$CINPUT Push changes to github (y/[n]): $END"
    read input
    if [ "$input" == "y" ]; then
        PUSH=1
    fi
fi

printf "$CINPUT Would you like to publish this package to a repo?$END\n"
printf "$CINPUT New repos can be configures using $CINFO 'poetry config repositories.<reponame> <url>' $END\n"
printf "$CINPUT Repository name (example: pypi; ENTER to skip): $END"
read input
if [ "$input" != "" ]; then
    REPO=$input
fi


#################################
## Formatting
#################################
printf "\n$SEP formatting code $SEP\n"

msg="$PREFIX - formatting for release $VERSION"
printf "$CINFO $msg $END\n"
poetry run keats run format
if [ "$COMMIT" == 1 ]; then
    git add .
    git commit -m "$msg"
    echo "$?"
else
    printf "$CWARN skipping format commit$END\n"
fi


#################################
## Documentation
#################################
printf "\n$SEP updating documentation $SEP\n"
msg="$PREFIX - updating docs for release $VERSION "
printf "$CINFO $msg $END\n"
printf $msg
poetry run keats run document

if [ "$COMMIT" == 1 ]; then
    git add .
    git commit -m "$msg"
else
    printf "$CWARN skipping document commit $END\n"
fi


#################################
## Tagging
#################################
printf "\n$SEP Tagging branch $SEP\n"
if [ "$COMMIT" == 1 ]; then
    git tag $TAG
else
    printf "$CWARN skipping tagging $END\n"
fi

if [ "$PUSH" == 1 ]; then
    git push
    git push $TAG
fi


#################################
## Releasing
#################################
printf "\n$SEP Publishing $SEP\n"


if [ "$REPO" != "" ]; then
    poetry config repositories.$REPO
    printf "$CWARN Are you sure you want to publish $NAME $VERSION to $REPO ([y]/n)?: $END"
    read input
    if [ "$input" == "n" ]; then
        REPO=""
    fi

    if [ "$REPO" == "pypi" ]; then
        poetry publish --build
    elif [ "$REPO" != "" ]; then
        poetry publish --build -r $REPO
    fi
else
    printf "$CWARN skipping publishing, repo not specified $END\n"
fi