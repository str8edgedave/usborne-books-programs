10 rem haunted house adventure
20 rem ***********************
30 rem this version for "microsoft" basic
40 rem requires a minimum of 16k
50 rem select "text mode" if necessary
60 rem *******************************
70 v=25:w=36:g=18
80 gosub 1600
90 print chr$(147);"haunted house"
100 print "--------------"
110 print "your location"
120 print d$(rm)
130 print "exits:";
140 for i=1 to len(r$(rm))
150 print mid$(r$(rm),i,1);",";
160 next i
170 print
180 for i=1 to g
190 if l(i)=rm and f(i)=0 then print "you can see ";o$(i);" here"
200 next i
210 print "============================"
220 print m$:m$="what"
230 input "what will you do now ";q$
240 v$="":w$="":vb=0:ob=0
250 for i=1 to len(q$)
260 if mid$(q$,i,1)=" " and v$="" then v$=left$(q$,i-1)
270 if mid$(q$,i+1,1)<>" " and v$<>"" then w$=mid$(q$,i+1,len(q$)-1):i=len(q$)
280 next i
290 if w$="" then v$=q$
300 for i=1 to v
310 if v$=v$(i) then vb=i
320 next i
330 for i=1 to w
340 if w$=o$(i) then let ob=i
350 next i
359 rem *** error message override conditions ***
360 if w$>"" and ob=0 then m$="that’s silly"
370 if vb=0 then vb=v+1
380 if w$="" then m$="i need two words"
390 if vb>v and ob>0 then m$="you can’t ‘"+q$+"'"
400 if vb>v and ob=0 then m$="you don’t make sense"
410 if vb<v and ob>0 and c(ob)=0 then m$="you don’t have ‘"+w$+"'"
420 if f(26)=1 and rm=13 and int(rnd(1) * 3)<>2 and vb<>21 then m$="bats attacking!":goto 90
430 if rm=44 and int(rnd(1) * 2)=1 and f(24)<>1 then f(27)=1
440 if f(0)=1 then ll=ll-1
450 if ll<1 then f(0)=0
455 if vb>14 then goto 465
460 on vb gosub 500,570,640,640,640,640,640,640,640,980,980,1030,1070,1140
463 goto 470
465 on vb-14 gosub 1180,1220,1250,1300,1340,1380,1400,1430,1460,1490,1510,1590
470 if ll=10 then m$="your candle is waning!"
480 if ll=1 then m$="your candle is out!"
490 goto 90
499 rem *** help ***
500 print "words i know:"
510 for i=1 to v
520 print v$(i);",";
530 next i
540 m$="":print
550 gosub 1580
560 return
569 rem *** carrying ***
570 print "your are carrying:"
580 for i=1 to g
590 if c(i)=1 then print o$(i);",";
600 next i
610 m$="":print
620 gosub 1580
630 return
639 rem *** movement ***
640 d=0
650 if ob=0 then d=vb-3
660 if ob=19 then d=1
670 if ob=20 then d=2
680 if ob=21 then d=3
690 if ob=22 then d=4
700 if ob=23 then d=5
710 if ob=24 then d=6
720 if rm=20 and d=5 then d=1
730 if rm=20 and d=6 then d=3
740 if rm=22 and d=6 then d=2
750 if rm=22 and d=5 then d=3
760 if rm=36 and d=6 then d=1
770 if rm=36 and d=5 then d=2
780 if f(14)=1 then m$="crash! you fell out of the tree!":f(14)=0:return
790 if f(27)=1 and rm=52 then m$="ghosts will not let you move":return
800 if rm=45 and c(1)=1 and f(34)=0 then m$="a magical barrier to the west":return
810 if (rm=26 and f(0)=0) and (d=1 or d=4) then m$="you need a light":return
820 if rm=54 and c(15) <> 1 then m$="you’re stuck!":return
830 if c(15)=1 and not (rm=53 or rm=54 or rm=55 or rm=47) then m$="you can’t carry a boat!":return
840 if (rm>26 and rm<30) and f(0)=0 then m$="too dark to move":return
850 f(35)=0:rl=len(r$(rm))
860 for i=1 to rl
870 u$=mid$(r$(rm),i,1)
880 if (u$="n" and d=1 and f(35)=0) then rm=rm-8:f(35)=1
890 if (u$="s" and d=2 and f(35)=0) then rm=rm+8:f(35)=1
900 if (u$="w" and d=3 and f(35)=0) then rm=rm-1:f(35)=1
910 if (u$="e" and d=4 and f(35)=0) then rm=rm+1:f(35)=1
920 next i
930 m$="ok"
940 if f(35)=0 then m$="can’t go that way!"
950 if d<1 then m$="go where?"
960 if rm=41 and f(23)=1 then r$(49)="sw":m$="the door slams shut!":f(23)=0
970 return
979 rem *** get and take ***
980 if ob>g then m$="i can’t get "+w$:return
981 rem print "l(ob): " + l(ob) + " rm " + rm;
985 if l(ob) <> rm then m$="it isn’t here"
990 if f(ob) <> 0 then m$="what "+w$+"?"
1000 if c(ob)=1 then m$="you already have it"
1010 if ob>0 and l(ob)=rm and f(ob)=0 then c(ob)=1:l(ob)=65:m$="you have the "+w$
1020 return
1029 rem *** open ***
1030 if rm=43 and (ob=28 or ob=29) then f(17)=0:m$="drawer open"
1040 if rm=28 and ob=25 then m$="it’s locked"
1050 if rm=38 and ob=32 then m$="that’s creepy!":f(2)=0
1060 return
1069 rem *** examine ***
1070 if ob=30 then f(18)=0:m$="something here!"
1080 if ob=31 then m$="that’s disgusting!"
1090 if (ob=28 or ob=29) then m$="there is a drawer"
1100 if ob=33 or ob=5 then gosub 1140
1110 if rm=43 and ob=35 then m$="there is something beyond..."
1120 if ob=32 then gosub 1030
1130 return
1139 rem *** read ***
1140 if rm=42 and ob=33 then m$="they are demonic works"
1150 if (ob=3 or ob=36) and c(3)=1 and f(34)=0 then m$="use this word with care ‘xzanfar'"
1160 if c(5)=1 and ob=5 then m$="the script is in an alien tongue"
1170 return
1179 rem *** say ***
1180 m$="ok ‘"+w$+"'"
1190 if c(3)=1 and ob=34 then m$="*magic occurs*": if rm<>45 then rm=int(rnd(1) * 64)
1200 if c(3)=1 and ob=34 and rm=45 then f(34)=1
1210 return
1219 rem *** dig ***
1220 if c(12)=1 then m$="you made a hole"
1230 if c(12)=1 and rm=30 then m$="dug the bars out":d$(rm)="hole in wall":r$(rm)="nse"
1240 return
1249 rem *** swing ***
1250 if c(14) <> 1 and rm=7 then m$="this is no time to play games"
1260 if ob=14 and c(14)=1 then m$="you swung it"
1270 if ob=13 and c(13)=1 then m$="whoosh"
1280 if ob=13 and c(13)=1 and rm=43 then r$(rm)="wn":d$(rm)="study with secret room":m$="you broke the thin wall"
1290 return
1299 rem *** climb ***
1300 if ob=14 and c(14)=1 then m$="it isn’t attached to anything!"
1310 if ob=14 and c(14)<>1 and rm=7 and f(14)=0 then m$="you see thick forest and cliff south":f(14)=1:return
1320 if ob=14 and c(14)<>1 and rm=7 and f(14)=1 then m$="going down!":f(14)=0
1330 return
1339 rem *** light ***
1340 if ob=17 and c(17)=1 and c(8)=0 then m$="it will burn your hands"
1350 if ob=17 and c(17)=1 and c(9)=0 then m$="nothing to light it with"
1360 if ob=17 and c(17)=1 and c(9)=1 and c(8)=1 then m$="it casts a flickering light":f(0)=1
1370 return
1379 rem *** unlight ***
1380 if f(0)=1 then f(0)=0:m$="extinguished"
1390 return
1399 rem *** spray ***
1400 if ob=26 and c(16)=1 then m$="hissss"
1410 if ob=26 and c(16)=1 and f(26)=1 then f(26)=0:m$="pfft! got them"
1420 return
1429 rem *** use ***
1430 if ob=10 and c(10)=1 and c(11)=1 then m$="switched on":f(24)=1
1440 if f(27)=1 and f(24)=1 then m$="whizz - vacuumed the ghosts up!":f(27)=0
1450 return
1459 rem *** unlock ***
1460 if rm=43 and (ob=27 or ob=28) then gosub 1030
1470 if rm=28 and ob=25 and f(25)=0 and c(18)=1 then f(25)=1:r$(rm)="sew":d$(rm)="huge open door":m$="the key turns!"
1480 return
1489 rem *** leave ***
1490 if c(ob)=1 then c(ob)=0:l(ob)=rm:m$="done"
1500 return
1509 rem *** score ***
1510 s=0
1520 for i=1 to g
1530 if c(i)=1 then s=s+1
1540 next i
1550 if s=17 and c(15)<>1 and rm<>57 then print "you have everything":print "return to the gate for final score"
1560 if s=17 and rm= 57 then print "double score for reaching here!":s=s*2
1570 print "your score=";s:if s>18 then print "well done! you finished the game":end
1580 input "press return to continue"; q$
1590 return
1600 dim r$(63), d$(63), o$(w),v$(v)
1610 dim c(w),l(g),f(w)
1620 data 46,38,35,50,13,18,28,42,10,25,26,4,2,7,47,60,43,32
1630 for i=1 to g
1640 read l(i)
1650 next i
1660 data "help","carrying","go","n","s","w","e","u","d","get","take","open","examine","read","say"
1665 data "dig","swing","climb","light","unlight","spray","use","unlock","leave","score"
1680 for i=1 to v
1690 read v$(i)
1700 next i
1710 data "se","we","we","swe","we","we","swe","ws"
1720 data "ns","se","we","nw","se","w","ne","nsw"
1730 data "ns","ns","se","we","nwud","se","wsud","ns"
1740 data "n","ns","nse","we","we","nsw","ns","ns"
1750 data "s","nse","nsw","s","nsud","n","n","ns"
1760 data "ne","nw","ne","w","nse","we","w","ns"
1770 data "se","nsw","e","we","nw","s","sw","nw"
1780 data "ne","nwe","we","we","we","nwe","nwe","w"
1790 for i=0 to 63
1800 read r$(i)
1810 next i
1820 data "dark corner","overgrown garden","by large woodpile","yard by rubbish"
1825 data "weedpatch","forest","thick forest","blasted tree"
1840 data "corner of house","entrance to kitchen","kitchen & grimy cooker","scullery door"
1845 data "room with inches of dust","rear turret room","clearing by house","path"
1860 data "side of house","back of hallway","dark alcove","small dark room"
1865 data "bottom of spiral staircase","wide passage","slippery steps","clifftop"
1880 data "near crumbling wall","gloomy passage","pool of light","impressive vaulted hallway"
1885 data "hall by thick wooden door","trophy room","cellar with barred window","cliff path"
1900 data "cupboard with hanging coat","front hall","sitting room","secret room"
1905 data "steep marble stairs","dining room","deep cellar witih coffin"," cliff path"
1920 data "closet","front lobby","library of evil books","study with desk & hole in wall"
1925 data "weird cobwebby room","very cold chamber","spooky room","cliff path by marsh"
1940 data "rubble-strewn verandah","front porch","front tower","sloping corridor"
1945 data "upper gallery","marsh by wall","marsh","soggy path"
1960 data "by twisted railing","path through iron gate","by railings","beneath front tower"
1965 data "debris from crumbling facade","large fallen brickwork","rotting stone arch","crumbling clifftop"
1980 for i=0 to 63
1990 read d$(i)
2000 next i
2010 data "painting","ring","magic spells","goblet","scroll","coins","statue","candlestick"
2012 data "matches","vacuum","batteries","shovel","axe","rope","boat","aerosol","candle","key"
2014 data "north","south","west","east","up","down"
2016 data "door","bats","ghosts","drawer","desk","coat","rubbish"
2018 data "coffin","books","xzanfar","wall","spells"
2060 for i=1 to w
2070 read o$(i)
2080 next i
2090 f(18)=1:f(17)=1:f(2)=1:f(26)=1:f(28)=1:f(23)=1:ll=60:rm=57:m$="ok"
2100 return

