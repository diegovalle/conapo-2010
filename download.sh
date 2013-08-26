#!/bin/bash
# States
declare -a states=("Aguascalientes" "BajaCalifornia" "BajaCaliforniaSur"
    "Campeche" "Chiapas" "Chihuahua" "Coahuila" "Colima"
    "DistritoFederal" "Durango" "Mexico" "Guanajuato"
    "Guerrero" "Hidalgo" "Jalisco" "Michoacan" "Morelos"
    "Nayarit" "NuevoLeon" "Oaxaca" "Puebla" "Queretaro"
    "QuintanaRoo" "SanLuisPotosi" "Sinaloa" "Sonora" "Tabasco"
    "Tamaulipas" "Tlaxcala" "Veracruz" "Yucatan" "Zacatecas")


#make dirs to hold the projections and past information
mkdir -p data/state-projections
mkdir -p data/state-indicators
mkdir -p data/municipalities

#Projections
#DE LAS ENTIDADES FEDERATIVAS 2010 - 2030
for i in {1..32}
do
    curl -o data/state-projections/${states[$i-1]}.xlsx http://www.conapo.gob.mx/work/models/CONAPO/Proyecciones/2010_2050/Estatales/${states[$i-1]}.xlsx
    sleep 2
done
#download the projections at the national level
curl -o data/state-projections/RepublicaMexicana.xlsx http://www.conapo.gob.mx/work/models/CONAPO/Proyecciones/2010_2050/RepublicaMexicana.xlsx

# Past population
# DE LAS ENTIDADES FEDERATIVAS 1990-2010
for i in {1..32}
do
    curl -o data/state-indicators/${states[$i-1]}.xlsx http://www.conapo.gob.mx/work/models/CONAPO/Indicadores_Basicos_1990_2010/Entidades_Federativas_1990_2010/${states[$i-1]}.xlsx
    sleep 2
done
#download the indicators at the national level
curl -o data/state-indicators/RepublicaMexicana.xlsx http://www.conapo.gob.mx/work/models/CONAPO/Indicadores_Basicos_1990_2010/Nacional_1990_2010/RepublicaMexicana.xlsx

#Municipalities
curl -o data/Municipales2010_2030.zip http://www.conapo.gob.mx/work/models/CONAPO/Resource/1247/1/images/Municipales2010_2030.zip
unzip data/Municipales2010_2030.zip -d data/municipalities
rm -rf data/Municipales2010_2030.zip

#DE LAS ENTIDADES FEDERATIVAS 2010 - 2030
#http://www.conapo.gob.mx/work/models/CONAPO/Proyecciones/2010_2050/Estatales/Aguascalientes.xlsx

# DE LAS ENTIDADES FEDERATIVAS 1990-2010
#curl -o http://www.conapo.gob.mx/work/models/CONAPO/Indicadores_Basicos_1990_2010/Entidades_Federativas_1990_2010/Aguascalientes.xlsx
