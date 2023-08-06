# Introduction

It is used to generate tables of scores for bridge games

````
pip install pbr # install package
pbr sample      # download sample xlsx for reference: record.xlsx
                # edit xlsx for team and add data in first sheet (sheet name with datetime like 2021-05-19)
pbr record.xlsx # check result, mostly record.html
````

see sample [https://xrgopher.gitlab.io/pbrats](https://xrgopher.gitlab.io/pbrats)

## Guideline

In sheet `team`

````
host	guest
gopher	zyj
lhylllll	xjtuzhu
lihao	wingzero
````

In sheet `2021-05-12`, set this as default

````
id	1	2	3	4	5	6	7	8
gopher	W3NT+2	S2D+1	S1H=	S3NT-2	S5Hx=	N4SX-3	S3NT+2	W1NT=
zyj	W3NT+1	S2D+2	S1H=	S3NT-3	W5CX-1	N4SX-3	S3NT+2	E1S=
xjtuzhu	W3NT+1	S2D+2	S1H=	S3NT-3	W5CX-3	N4SX-2	S3NT+2	W1NT-1
lihao	W3NT+2	S2D+1	S1H=	S3NT-2	W5CX-2	N4SX-3	S3NT+2	W1NT=
wingzero	W3NT+2	S2D=	S1H=	S3NT-2	W5CX-3	N4SX-5	S3NT+2	S1NT-2
lhylllll	W3NT+1	S2D+2	S1H+1	S3NT-1	W5CX-3	N4SX-3	S3NT+2	W1NT-1
````

# Contact

* gopher in xinrui app

# Credits

* inspired with http://www.bridgeconex.com/IndexBC.aspx
* some codes are from https://github.com/anntzer/redeal