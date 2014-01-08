CONAPO Mexican population estimates 1990-2030
=============================================

[![Continuous Integration status](https://secure.travis-ci.org/diegovalle/conapo-2010.png)](http://travis-ci.org/diegovalle/conapo-2010)

Clean the projected and estimated *mid-year* population data at the state and
county level from the CONAPO (2010)

* Proyecciones Estatales (States) 2010-2030
* Estimaciones Estatales (States) 1990-2010
* Proyecciones Municipales (Counties) 2010-2030
* Proyecciones Municipales (Counties) 1990-2030

Original data from the [CONAPO website](http://www.conapo.gob.mx/es/CONAPO/Proyecciones)
and the data for the _Proyecciones Municipales (Counties) 1990-2030_ before 2010 come from the  Estimaciones de Población CONAPO-COLMEX 1990-2012 from the [SINAIS website](http://www.sinais.salud.gob.mx/basesdedatos/index.html)

This project is compatible with python 3

```shell
virtualenv --python=/usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
python clean_pop.py
python municipios.py
```
__The clean data is already available in the 'clean-data' directory__

```
 DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
                    Version 2, December 2004 

 Copyright (C) 2013 Diego Valle-Jones diegovalle[at]gmail.com

 Everyone is permitted to copy and distribute verbatim or modified 
 copies of this license document, and changing it is allowed as long 
 as the name is changed. 

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

  0. You just DO WHAT THE FUCK YOU WANT TO.
```

