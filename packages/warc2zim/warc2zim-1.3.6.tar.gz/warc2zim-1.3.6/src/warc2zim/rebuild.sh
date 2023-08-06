#!/bin/bash

python setup.py extract_messages
python setup.py update_catalog
python setup.py compile_catalog
PYTHONPATH="src" python ./src/warc2zim/main.py -u https://isago.ml --name isago --output ~/data/ --lang fr ~/data/myisago.warc
kiwix-serve -p 9999 ~/data/isago_2021-01.zim
