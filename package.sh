#!/bin/sh

cd RedOwl
zip -r ../RedOwl.zip *
cd ..
echo '#!/usr/bin/env python3' | cat - RedOwl.zip > redowl
chmod +x redowl
#mv redowl debian/
rm RedOwl.zip

debuild --no-tgz-check
rm redowl
