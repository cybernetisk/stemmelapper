#!/usr/bin/env python
#coding: utf-8

# Sett antall eksemplarer i "antall" variablen
# Hvis programmet kjøres med et vilkårlig parameter
# Vil tale-lappen få en X-<nr>, og ikke stemmeseddel
# Endre riktig tekst i drawstring til å bli årstall

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import sys
def forside(nr):
	#antall eksemplarer
	antall = 6
	aarstall = "H2012"

	a=(A4[0]/antall)
	al=55 #Tekst mot midten, hoyere er mer mot midt
	d.line(0, 150, A4[0], 150)
	s = [0.1, 1, 0.2]
	if len(sys.argv)<2:
		for x in xrange(antall):
			d.drawString(a*x+al-50, 130, "Seddel %s" % (x+1))
			d.drawString(a*x+al-50, 118, aarstall)
			d.line(a*x, 150, a*x, 0)
			#Her setter man fargene som skal være på stemmeseddele
			d.setFillColorRGB(x%2,0+(x/6.0),0+(x/10.0))
			d.roundRect((a*(x+1))-25,7.5,20,135,10,1,1)
			d.setFillColorRGB(0,0,0)

	d.setFont("Helvetica-Bold", 300)
	if len(sys.argv)>1:
		ekstra = "X"
	else:
		ekstra = ""
	d.drawCentredString((A4[0]/2), (A4[1]/2)+40, ekstra+str(nr))
	d.showPage()
	
	d.setFont("Helvetica-Bold", 300)
	d.line(0, 150, A4[0], 150)
	d.drawCentredString((A4[0]/2), (A4[1]/2)+40, ekstra+str(nr))

	l=A4[0]/5

	d.setLineWidth(10)
	for x in xrange(5):
		d.line(0+(l*x), A4[1], 0+(l*(x+1)), 150)
	d.save()
#BEGIN SCRIPT
d = canvas.Canvas("temp.pdf",pagesize=A4)

for x in xrange(50):
	forside(x+1)
	d.save()
