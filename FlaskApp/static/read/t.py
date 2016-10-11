# -*- coding: utf-8 -*-
import json
with open('read.json','rw') as file:
    data = json.load(file)
    with open('2.json','w') as f2:
        json.dump(data, f2, indent=4)


