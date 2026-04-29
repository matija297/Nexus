# README.md
Projekt Nexus – Tehnička dokumentacija
Izvršni sažetak

Cilj projekta je analiza podataka iz kratera Jezero na Marsu radi izrade automatiziranog navigacijskog sustava. Ulazni podaci uključuju telemetriju (lokacije, uzorke), a izlaz je optimizirani navigacijski nalog za robotsku jedinicu.

Metodologija obrade podataka

Podaci su obrađeni korištenjem Python skripti i DataFrame struktura. Uklonjeni su senzorski šumovi poput ekstremnih vrijednosti temperature i anomalija u pH. Primijenjeni su logički filtri radi osiguranja točnosti analize.

Geoprostorna analiza i vizualizacija

Rezultati su prikazani kroz grafove i mape:

korelacija parametara
toplinske karte
raspodjela metana

Satelitska mapa koristi extent mapping za precizno pozicioniranje podataka na GPS koordinatama.
