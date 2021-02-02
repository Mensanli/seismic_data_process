2. meseed2sac
```sh
#!/bin/bash
mkdir sacevents
for w in {'HTB','LHG','STZ'}  # $(cat station.list)
do 
mkdir ./sacevents/$w.220
cd ./sacevents/$w.220
mseed2sac ../../XJ.$w.00.BH?.D.2017.220 ./
cd ../../
done
```
