"""Tool To Generate Beach themed -MLH avatars"""
__version__ = "0.1.1"
from hashlib import sha256
import re
def avoid_dup(i,final,avcolor):
	current=''
	if(i<len(avcolor)):
		current=avcolor[i]
	else:
		current=avcolor[(i%len(avcolor))-1]
	while(current in final):
		i+=1
		if(i>len(avcolor)):
			current=avcolor[i%len(avcolor)-1]
		else:
			current=avcolor[i]
	final.append(current)
def generate_seavatar(string,filename='seavatar.svg'):
	#P1:Hashing the string
	h=sha256(string.encode('utf-8')).hexdigest()
	hashed_string=''
	for i in h:
		if(i.isalpha()):
			hashed_string+=str(ord(i))
		else:
			hashed_string+=i
	
	
	av_string=hashed_string[0:16]
	
	
	#P2:Defining SVG
	svg_header='<?xml version="1.0" encoding="UTF-8" standalone="no"?><!-- Created by Victor --><svg  xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 559.369 793.6992">'
	svg_circle='<path id="circle" d=" M 275.4473,154.4572 C 154.8788,154.4572 56.2319,253.1041 56.2319,373.6726 56.2319,494.241 154.8788,592.8879 275.4473,592.8879 396.0157,592.8879 494.6627,494.241 494.6627,373.6726 494.6627,253.1041 396.0157,154.4572 275.4473,154.4572 Z" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:5;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/>'
	svg_sun='<path id="sun" d=" M 371.4748,223.912 C 356.7632,223.912 344.7265,235.9487 344.7265,250.6602 344.7265,265.3717 356.7632,277.4084 371.4748,277.4084 386.1862,277.4084 398.223,265.3717 398.223,250.6602 398.223,235.9487 386.1862,223.912 371.4748,223.912 Z" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:3;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/>'
	svg_ray='<g id="sunrays"><path id="ray1" d=" M 366.7082,204.4406 Q 366.7082,204.4406 366.7082,204.4406 366.7082,204.4406 366.7082,204.4406 366.7082,204.4406 366.7082,204.4406 366.7082,204.4406 366.7082,204.4406 366.7082,204.4406 366.7082,204.4406 366.7082,204.4406 367.7327,209.0528 368.7571,213.6649 368.807,215.1213 368.857,216.5778 368.857,218.2124 368.857,219.8471 368.857,219.6679 368.857,219.4888 368.857,219.8471 368.857,220.2054 368.857,220.2054" style="fill:none;stroke:#here;stroke-width:3;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/><path id="ray2" d=" M 375.3032,281.1147 Q 375.3032,281.1147 375.3032,281.1147 375.3032,281.1147 375.3032,281.1147 375.3032,281.1147 375.3032,281.1147 375.3032,281.1147 375.3032,281.1147 375.3032,281.1147 375.3032,281.1147 Z" style="fill:none;stroke:#here;stroke-width:3;stroke-opacity:1;stroke-linecap:butt;stroke-miterlimit:4;stroke-dashoffset:0;"/><path id="ray3" d=" M 373.8706,281.8312 Q 373.8706,281.8312 373.8706,281.8312 373.8706,281.8312 373.8706,281.8312 373.8706,281.8312 373.8706,281.8312 373.8706,281.8312 373.8706,283.7383 373.8706,285.6454 373.8706,288.7581 373.8706,291.8708 373.8706,292.5836 373.8706,293.2965 373.8706,293.6548 373.8706,294.0131 373.8706,294.3899 373.8706,294.7667 373.8706,294.7667" style="fill:none;stroke:#here;stroke-width:3;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/><path id="ray4" d=" M 404.6692,251.0183 Q 404.6692,251.0183 404.6692,251.0183 404.6692,251.0183 404.6692,251.0183 404.6692,251.0183 404.6692,251.0183 404.6692,251.0183 404.6692,251.0183 404.6692,251.0183 408.4294,250.4809 412.1897,249.9435 412.7236,249.7643 413.2575,249.5851 413.6189,249.5851 413.9803,249.5851 414.3385,249.5851 414.6966,249.5851 414.6966,249.5851" style="fill:none;stroke:#here;stroke-width:3;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/><path id="ray5" d=" M 333.0447,254.6012 Q 333.0447,254.6012 333.0447,254.6012 333.0447,254.6012 333.0447,254.6012 333.0447,254.6012 333.0447,254.6012 333.0447,254.6012 333.0447,254.6012 333.0447,254.6012 333.0447,254.6012 333.0447,254.6012 333.0447,254.6012 333.0447,254.6012 336.5408,254.9311 340.0368,255.261 341.7336,255.2894 343.4303,255.3178 343.0721,255.3178" style="fill:none;stroke:#here;stroke-width:3;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/><path id="ray6" d=" M 340.9234,222.3551 Q 340.9234,222.3551 340.9234,222.3551 340.9234,222.3551 340.9234,222.3551 340.9234,222.3551 340.9234,222.3551 340.9234,222.3551 340.9234,222.3551 340.9234,222.3551 340.9234,222.3551 340.9234,222.3551 343.4302,224.1466 345.9371,225.938 346.8843,227.1167 347.8315,228.2953 347.9586,228.5498 348.0858,228.8043 348.444,228.8043 348.8021,228.8043 348.8021,228.8043" style="fill:none;stroke:#here;stroke-width:3;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/><path id="ray7" d=" M 391.0605,271.7991 Q 391.0605,271.7991 391.0605,271.7991 391.0605,271.7991 391.0605,271.7991 391.0605,271.7991 391.0605,271.7991 391.0605,271.7991 391.0605,271.7991 391.0605,271.7991 391.0605,271.7991 391.0605,271.7991 391.0605,271.7991 391.0605,271.7991 393.5674,272.874 396.0742,273.9489 396.0742,273.9489 396.0742,273.9489 397.2079,274.705 398.3417,275.4612 398.223,275.382" style="fill:none;stroke:#here;stroke-width:3;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/><path id="ray8" d=" M 396.7905,229.5209 Q 396.7905,229.5209 396.7905,229.5209 396.7905,229.5209 396.7905,229.5209 396.7905,229.5209 396.7905,229.5209 396.7905,229.5209 396.7905,229.5209 396.7905,229.5209 396.7905,229.5209 396.7905,229.5209 397.9552,227.8895 399.12,226.258 400.6226,224.0657 402.1252,221.8734 401.9647,222.1143 401.8042,222.3551 401.8042,222.3551" style="fill:none;stroke:#here;stroke-width:3;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/><path id="ray9" d=" M 341.6396,281.8312 Q 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 341.6396,281.8312 344.6657,279.1822 347.6918,276.5331 347.5307,276.6741 347.3696,276.8152 347.3696,276.8152 347.3696,276.8152 347.3696,276.8152" style="fill:none;stroke:#here;stroke-width:3;stroke-opacity:1;stroke-linecap:butt;stroke-miterlimit:4;stroke-dashoffset:0;"/></g>'
	svg_boatborder='<path id="boatborder" d=" M 150.3149,446.6175 Q 230.5695,459.5216 300.7924,444.4668 C 310.8242,479.5946 287.751,491.6385 282.1618,511.8549 219.3437,519.7408 215.4501,512.3568 186.8594,512.5718 Q 146.7321,482.4622 150.3149,446.6175 Z" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:3;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/>'
	svg_bbody='<path id="bbody" d=" M 226.9868,356.2888 233.8452,356.2888 233.8452,452.3526 226.9868,452.3526 226.9868,356.2888 Z" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:3;stroke-opacity:1;stroke-linecap:square;stroke-miterlimit:4;stroke-dashoffset:0;"/>'
	svg_bflag1='<path id="bflag" d=" M 235.9511,360.491 282.6846,419.4775 234.5314,422.8488 C 259.1215,395.7161 234.8894,397.755 235.9511,360.491 Z" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:3;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/>'
	svg_bflag2='<path id="bfalg2" d=" M 227.0114,363.4577 193.3085,410.3994 225.6897,411.7218 C 226.3506,423.6225 229.853,393.6724 227.0114,363.4577 Z" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:3;stroke-opacity:1;stroke-linecap:square;stroke-miterlimit:4;stroke-dashoffset:0;"/>'
	svg_bdesig1='<path id="bdesign" d=" M 153.1811,461.6723 302.2255,463.823 295.0599,483.1791 C 197.6078,456.654 190.4422,501.1015 153.1811,461.6723 Z" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:2;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/>'
	svg_bdesig2='<path id="bdesig2" d=" M 233.4358,496.8001 279.2956,496.8001 279.2956,501.8184 233.4358,501.8184 233.4358,496.8001 Z" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:2;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/>'
	svg_bdesig3='<path id="bdesig3" d=" M 208.9482,493.9389 C 206.1851,493.9389 203.9244,496.1996 203.9244,498.9627 203.9244,501.7257 206.1851,503.9865 208.9482,503.9865 211.7113,503.9865 213.9719,501.7257 213.9719,498.9627 213.9719,496.1996 211.7113,493.9389 208.9482,493.9389 Z" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:2;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/>'
	svg_water='<path id="water" d=" M 112.3372,519.0239 Q 178.9773,493.2156 242.0345,521.1746 C 293.2685,535.5125 348.0853,472.4257 443.3877,515.4394 Q 384.6298,580.6768 288.6109,593.5809 191.8753,601.4668 112.3372,519.0239 Z" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:3;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/>'
	svg_waterbub='<path id="waterbub" d=" M 384.06,544.0989 C 384.8482,544.0989 385.4932,543.454 385.4932,542.6657 385.4932,541.8774 384.8482,541.2325 384.06,541.2325 383.2717,541.2325 382.6268,541.8774 382.6268,542.6657 382.6268,543.454 383.2717,544.0989 384.06,544.0989 Z" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:2;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/>'
	svg_star='<path id="star1" d=" M 349.5184,546.463 352.4102,552.3223 358.8762,553.2618 354.1973,557.8227 355.3018,564.2626 349.5184,561.2221 343.735,564.2626 344.8395,557.8227 340.1606,553.2618 346.6267,552.3223 349.5184,546.463 Z" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:2;stroke-opacity:1;stroke-linecap:butt;stroke-miterlimit:4;stroke-dashoffset:0;"/><path id="star2" d=" M 186.1429,556.3448 188.409,560.4883 192.5526,562.7545 188.409,565.0206 186.1429,569.1642 183.8767,565.0206 179.7331,562.7545 183.8767,560.4883 186.1429,556.3448 Z" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:2;stroke-opacity:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dashoffset:0;"/>'
	svg_textm='<text id="mlh1" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:2;stroke-opacity:1;stroke-linecap:butt;stroke-miterlimit:4;stroke-dashoffset:0;" transform="matrix(1.3448,-0.3879,0.3879,1.3448,-416.1395,-206.943)" x="279.6845" y="423.3838" font-family="Roboto-Bold" font-size="33" font-style="normal" text-align="left">M</text>'
	svg_textl='<text id="mlh2" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:2;stroke-opacity:1;stroke-linecap:butt;stroke-miterlimit:4;stroke-dashoffset:0;" transform="matrix(1.6769,0.1365,-0.1365,1.6769,-257.3987,-498.6111)" x="279.6845" y="423.3838" font-family="Roboto-Bold" font-size="37" font-style="normal" text-align="left">L</text>'
	svg_texth='<text id="mlh3" style="fill:#here;fill-opacity:1;stroke:#000000;stroke-width:2;stroke-opacity:1;stroke-linecap:butt;stroke-miterlimit:4;stroke-dashoffset:0;" transform="matrix(1.5209,0,0,1.5209,-253.9056,-401.8094)" x="279.6845" y="423.3838" font-family="Roboto-Bold" font-size="35" font-style="normal" text-align="left">H</text>'
	
	#P3:Defining Color Palette
	water_c=['77ACF1','3EDBF0','125D98','3C8DAD','2541B2','39A9CB','00EAD3','867AE9','94D0CC','A6D6D6','2978B5','51C4D3','28B5B5','d72323','6EB6FF','7098DA','FBFAD3','A2CBF3']
	circle_c=['FDC7FF','BAE8E8','02475E','B6C9F0','F5F7B2','293B5F','47597E','FF96AD','FEDDBE','867AE9','C6FFC1','A7D0CD','EDFFA9','8FD9A8','B8B5FF','7868E6','307672','FBFAD3','C84B31','346751','47597E','DBE6FD','E0F9B5','FDFDFD','D72323','4ECCA3','81F5FF','930077','A6E4E7','FCCDE2','729D39','889E81','C6E377','111F4D','004445']
	sun_c=['F7FD04','F9B208','F98404','FC5404','FB9300','EBA83A','FFC93C','E1701A','F5F7B2']
	ray_c=['FDCA40','FF8303','EDFFA9','FFCC29','FFE268','FFFF00','F7EA00','CDC733','FFF600','FFD384','DBE6FD']
	boat_c=['98DDCA','FFAAA7','CE1212','B0EFEB','301B3F','B83B5E','30E3CA','FDFDFD','9DF3C4','FF7E67',"F73859",'D72323','17B978','F73859','1E56A0','930077','FF6464','4ECCA3','9A5B1B']
	flag1_c=['17B978','F73859','1E56A0','930077','FF6464','4ECCA3','A6E4E7','FDC7FF','A1DE93','3FBAC2','FF0000','C6E377','FBFAD3','FA4659','E43A19','B5FF7D','FF0080']
	flag2_c=['FF6464','4ECCA3','A6E4E7','FDC7FF','A1DE93','3FBAC2','17B978','F73859','1E56A0','930077','17B978','F73859','1E56A0','930077','FF0080','FF6464','4ECCA3']
	bdesig_c=['17B978','F73859','1E56A0','930077','FF6464','4ECCA3','A6E4E7','FDC7FF','A1DE93','3FBAC2','FF0000','C6E377','FBFAD3','FA4659','E43A19','B5FF7D','98DDCA','FFAAA7','CE1212','B0EFEB','301B3F','B83B5E','30E3CA','FDFDFD','9DF3C4','FF7E67',"F73859",'D72323','17B978','F73859','1E56A0','930077','FF6464','4ECCA3','FDC7FF','BAE8E8','02475E','B6C9F0','F5F7B2','293B5F','47597E','FF96AD','FEDDBE','867AE9','C6FFC1','A7D0CD','EDFFA9','8FD9A8','B8B5FF','7868E6','307672','FBFAD3','C84B31','346751','47597E','DBE6FD','E0F9B5','FDFDFD','D72323','4ECCA3','81F5FF','930077','A6E4E7','FCCDE2','729D39','889e81','C6E377','111F4D','004445','FDC7FF','BAE8E8','02475E','B6C9F0','F5F7B2','293B5F','47597E','FF96AD','FEDDBE','867AE9','C6FFC1','A7D0CD','EDFFA9','8FD9A8','B8B5FF','7868E6','307672','FBFAD3','C84B31','346751','47597E','DBE6FD','E0F9B5','FDFDFD','D72323','4ECCA3','81F5FF','930077','A6E4E7','FCCDE2','729D39','889e81','C6E377','111F4D','004445']
	pole_c=['17B978','F73859','1E56A0','930077','FF6464','4ECCA3','A6E4E7','FDC7FF','A1DE93','3FBAC2','FF0000','C6E377','FBFAD3','FA4659','E43A19','B5FF7D','98DDCA','FFAAA7','CE1212','B0EFEB','301B3F','B83B5E','30E3CA','FDFDFD','9DF3C4','FF7E67',"F73859",'D72323','17B978','F73859','1E56A0','930077','FF6464','4ECCA3','FDC7FF','BAE8E8','02475E','B6C9F0','F5F7B2','293B5F','47597E','FF96AD','FEDDBE','867AE9','C6FFC1','A7D0CD','EDFFA9','8FD9A8','B8B5FF','7868E6','307672','FBFAD3','C84B31','346751','47597E','DBE6FD','E0F9B5','FDFDFD','D72323','4ECCA3','81F5FF','98DDCA','FFAAA7','CE1212','B0EFEB','301B3F','B83B5E','30E3CA','FDFDFD','9DF3C4','FF7E67',"F73859",'D72323','17B978','F73859']
	waterbub_c=['B83B5E','30E3CA','FDFDFD','9DF3C4','FF7E67',"F73859",'D72323','17B978','F73859','1E56A0','930077','FF6464','4ECCA3','FDC7FF','BAE8E8','02475E','B6C9F0','F5F7B2','293B5F','47597E','FF96AD','FEDDBE','867AE9','C6FFC1','A7D0CD','77ACF1','3EDBF0','125D98','3C8DAD','2541B2','39A9CB','00EAD3','867AE9','94D0CC','A6D6D6','2978B5','51C4D3','28B5B5','d72323','6EB6FF','7098DA','FBFAD3']
	star_c=['F7FD04','F9B208','F98404','FC5404','FB9300','EBA83A','FFC93C','E1701A','F5F7B2','FDCA40','FF8303','EDFFA9','FFCC29','FFE268','FFFF00','F7EA00','CDC733','FFF600','FFD384','DBE6FD']
	textm_c=['CE1212','FB3640','D44000','810000','FA1E0E','E40017','F05454','A20A0A','BB2205','900D0D']
	textl_c=['1CC5DC','1597BB','8FD6E1','046582','51C2D5','125D98','3C8DAD','77ACF1','1CC5DC','1DDDE8']
	texth_c=['FFC93C','FED049','F5F7B2','E5D549','FFC93C','F7FD04','FFCC29','F7EA00','FFF600','F8F40D']
	
	#P4:Choosing color codes
	final_c=[]
	textm=textm_c[int(av_string[0])]
	final_c.append(textm)
	
	textl=textl_c[int(av_string[1])]
	if(textl in final_c):
		textl=textl_c[(int(av_string[1])+1)%(len(textl_c))]
	final_c.append(textl)
	
	texth=texth_c[int(av_string[2])]
	final_c.append(texth)
	
	i=int(av_string[3]+av_string[4])
	avoid_dup(i,final_c,circle_c)
	
	i=int(av_string[5])
	avoid_dup(i,final_c,sun_c)
	
	i=int(av_string[6]+av_string[7])
	avoid_dup(i,final_c,ray_c)
	
	i=int(av_string[8]+av_string[9])
	avoid_dup(i,final_c,boat_c)
	
	i=int(av_string[10]+av_string[11])
	avoid_dup(i,final_c,flag1_c)
	
	i=int(av_string[12]+av_string[13])
	avoid_dup(i,final_c,flag2_c)
	
	i=int(av_string[14]+av_string[15])
	avoid_dup(i,final_c,water_c)
	
	i=int(av_string[0]+av_string[1]+av_string[2])
	avoid_dup(i,final_c,bdesig_c)
	
	i=int(av_string[3]+av_string[4]+av_string[5])
	avoid_dup(i,final_c,bdesig_c)
	
	i=int(av_string[6]+av_string[7]+av_string[8])
	avoid_dup(i,final_c,bdesig_c)
	
	i=int(av_string[9]+av_string[10]+av_string[11])
	avoid_dup(i,final_c,star_c)
	
	i=int(av_string[12]+av_string[13]+av_string[14])
	avoid_dup(i,final_c,pole_c)
	
	i=int(av_string[7]+av_string[10])
	avoid_dup(i,final_c,waterbub_c)
	
	#P5:Creating SVG
	svg_textm=svg_textm.replace('here',final_c[0])
	svg_textl=svg_textl.replace('here',final_c[1])
	svg_texth=svg_texth.replace('here',final_c[2])
	svg_circle=svg_circle.replace('here',final_c[3])
	svg_sun=svg_sun.replace('here',final_c[4])
	svg_ray=svg_ray.replace('here',final_c[5])
	svg_boatborder=svg_boatborder.replace('here',final_c[6])
	svg_bflag1=svg_bflag1.replace('here',final_c[7])
	svg_bflag2=svg_bflag2.replace('here',final_c[8])
	svg_water=svg_water.replace('here',final_c[9])
	svg_bdesig1=svg_bdesig1.replace('here',final_c[10])
	svg_bdesig2=svg_bdesig2.replace('here',final_c[11])
	svg_bdesig3=svg_bdesig3.replace('here',final_c[12])
	svg_star=svg_star.replace('here',final_c[13])
	svg_bbody=svg_bbody.replace('here',final_c[14])
	svg_waterbub=svg_waterbub.replace('here',final_c[15])
	
	
	final_svg=svg_header+svg_circle+svg_sun+svg_ray+svg_boatborder+svg_bbody+svg_bflag1+svg_bflag2+svg_bdesig1+svg_bdesig2+svg_bdesig3+svg_water+svg_waterbub+svg_star+svg_textm+svg_textl+svg_texth+"</svg>"
	f=open(filename,'w')
	f.write(final_svg)
	return (final_svg)

