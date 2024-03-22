#!/bin/sh
PROJECT="common"
BUCKET="selfhostedpackages"
TEAM="devtools"

# -- Generate the package file for dumb-pypi
PACKAGE=$(poetry build | awk '{print $3}' | sed -n '3p')
echo "$PACKAGE" >> packages
sort -u packages -o packages

# -- Upload package
aws s3 cp "dist/$PACKAGE" "s3://$BUCKET/packages/$TEAM/$PROJECT/$PACKAGE"

# -- Generate static files for PyPi
dumb-pypi \
    --package-list packages \
    --packages-url "https://$BUCKET.s3.us-west-2.amazonaws.com/packages/$TEAM/$PROJECT" \
    --output-dir index

# -- Upload the files in S3
aws s3 cp --recursive index/ "s3://$BUCKET/dumb-pypi/$TEAM/index/"

# -- Open static pages in the browser
open "https://$BUCKET.s3.us-west-2.amazonaws.com/dumb-pypi/$TEAM/index/index.html"

# -- Serve PyPi locally
# -- python -m http.server -b 0.0.0.0 -d index 8080