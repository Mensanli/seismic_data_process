## Steps of CAP

***

# Disposal data

## 1. data require

run scpwaves.sh

~~~bash
#!/bin/bash
for i in $(cat ./listdown.txt)
do	
	printf "%s\n" $i	
	scp mensanli@10.16.22.22:/data/seis2/pub/waves/2018/XJ/$i/BH?.D/*121 ./20180501-121
done
~~~
## 2. meseed2sac

~~~bash
#!/bin/bash
mkdir sacevents
for w in {'HTB','LHG','STZ'}  # $(cat station.list)
do 
mkdir ./sacevents/$w.220
cd ./sacevents/$w.220
mseed2sac ../../XJ.$w.00.BH?.D.2017.220 ./
cd ../../
done
~~~



## 3. merge sacs:

mergesacs_all.sh

~~~bash
#!/bin/bash
#mkdir ./Data/2018121/cont2018121
cd Data/2018121
for x in $(cat ../../sacstation-2018121.txt)
do 
echo $x
sac << EOF
r *$x*BHN*
merge
w ../cont2018121/$x.BHN.sac
q
EOF
done	
~~~

## 4. Data  process

### 4.1 cut-data

~~~bash
sac
ch evlo xxx evla xxx 
synch
ch o gmt 20xx xxx 
evaluate to tt1 &1,o * -1
ch allt %tt1
w over
cut 0 400
r *sac
rmean;rtr;taper
~~~
### 4.2 ppk a

~~~bash
qdp on;ygrid on
ppk p 3 m on
w over
~~~

### 4.3 remove response

~~~sh
transfer from polezero s ../../pz_all to vel freq 0.05 0.1 10.0 15.0
mul 100
~~~
### 4.4 rot to r-t-z

~~~bash
ch stla xxxx stlo xxxx stel xxxx
lh             #reload dist
wh
sh rot_yk.pl
~~~

run rot_yk.pl:
~~~perl
`ls -1 *.BHZ*>1.txt`;
#!/usr/bin/perl
my @fl;
my $dir="rot_dir";
open(TXT,"1.txt");
@fl=<TXT>;chomp @fl;close(TXT);unlink "1.txt";
mkdir $dir,0750;
#first, judge the component azimuth
`ls -1 *.BHE*|awk '{print "r", \$1;print "ch cmpaz 90 cmpinc 90";print "w over";} END{print "q";}'|sac`;
`ls -1 *.BHN*|awk '{print "r", \$1;print "ch cmpaz 0 cmpinc 90";print "w over";} END{print "q";}'|sac`;
`ls -1 *.BHZ*|awk '{print "r", \$1;print "ch cmpaz 0 cmpinc 0";print "w over";} END{print "q";}'|sac`;
#second, make the three components in same lengths

foreach $fl (@fl){
        $tmp=substr($fl,0,length($fl)-5);
        $tmp2=substr($fl,0,length($fl)-7);
        open(SAC,"|sac");
        print SAC "r ${tmp}N.* ${tmp}E.*\n";
        print SAC "rot to gcp\n";
        print SAC "w $dir/${tmp2}r $dir/${tmp2}t\n";
        print SAC "q\n";
        close(SAC);
`       cp ${tmp2}BHZ* $dir/${tmp2}z`;
}
~~~
### 4.5 down-sample 

~~~bash
sac
r *
interp delta 0.08
~~~

## 5. create "weight.dat"

~~~bash
saclst kstnm a dist f *.r |gawk '{if ($4>0 && $4<400) print $2,$4,1,1,1,1,1,$3,0}' > weight.dat
saclst kstnm a dist f *.r |gawk '{if ($4>0 && $4<400) print $2,$4,2,2,1,1,1,$3,0}' | sort -nk 2
~~~
**Don't for get change the dist (2 row) to int**

***

# Create green's function:

~~~bash
sh fk.sh
~~~

fk.sh:

~~~bash
#!/bin/bash
for i in {'19','20','21','22','23','24','26','25','27','28'}
do
 fk.pl -Myk/$i -N512/0.08 -S2 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480
done
~~~

*!!!!fk.pl -Myk/15/k -N512/0.08 -S2 05 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100 105 110 115 120 125 130 135 140 145 150 155 160 165 170 175 180 185 190 195 200 205 210 215 220 225 230 235 240 245 250 255 260 265 270 275 280 285 290 295 300 305 310 315 320 325 330 335 340 345 350 355 360 365 370 375 380 385 390 395 400 405 410 415!!!!!!!*
**The green functions must match the station and source **

***

# Run cap

run cap.sh:

~~~bash
#!/bin/bash
for h in {'8','9','10','11','12','13','15','14','16','17','18','19','20','21','22','23','25','24','26','27','28'}
do 
echo yk_$h
cap.pl -H0.08 -P0.3 -S2/5/0 -T35/70 -F -D2/1/0.5 -C0.05/0.2/0.05/0.1 -W1 -Myk_$h/4.0 20180501111445
done
~~~
then you get xx_$h.ps;

To evaluate the optimal result:

~~~bash
grep -h Event 20180501111445/yk_*.out > ./20180501111445/junk.out
 ./depth.pl ./20180501111445/junk.out 20180501111445 > ./20180501111445/junk.ps
~~~


## [Back](https://mensanli.github.io/seismic_data_process/)
