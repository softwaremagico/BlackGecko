#!/bin/sh

cd BlackGecko
zip -r ../BlackGecko.zip *
cd ..
echo '#!/usr/bin/env python3' | cat - BlackGecko.zip > blackgecko
chmod +x blackgecko
#mv blackgecko debian/
rm BlackGecko.zip

debuild --no-tgz-check
rm blackgecko
