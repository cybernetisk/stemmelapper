#!/usr/bin/env python3
# coding: utf-8

# Sett antall eksemplarer i "antall" variablen
# Hvis programmet kjøres med et vilkårlig parameter
# Vil tale-lappen få en X-<nr>, og ikke stemmeseddel
# Endre riktig tekst i drawstring til å bli årstall

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from colorsys import hls_to_rgb
import sys

voteCount = 70
ballotCount = 13
year = "H2017"
outputName = "stem.pdf"

def createPage(voter):

    ballots = (A4[0] / ballotCount)
    al = 55
    document.line(0, 150, A4[0], 150)
    s = [0.1, 1, 0.2]
    if len(sys.argv) < 2:
        for i in range(ballotCount):
            document.rotate(90)
            document.drawString(25, -15 + (-ballots * i), "Seddel %2s - %s" % ((i + 1), year))

            document.rotate(-90)
            document.line(ballots * i, 150, ballots * i, 0)

            saturation = [0.4, 0.75]
            hls = hls_to_rgb(1.0 / ballotCount * i, saturation[i % 2], 0.9)

            document.setFillColorRGB(hls[0], hls[1], hls[2])
            document.roundRect((ballots * (i + 1)) - 25, 7.5, 20, 135, 10, 1, 1)
            document.setFillColorRGB(0, 0, 0)

    document.setFont("Helvetica-Bold", 300)

    append = ""
    if len(sys.argv) > 1:
        append = "X"

    document.drawCentredString((A4[0] / 2), (A4[1] / 2) + 40, append + str(voter))
    document.showPage()

    document.setFont("Helvetica-Bold", 300)
    document.line(0, 150, A4[0], 150)
    document.drawCentredString((A4[0] / 2), (A4[1] / 2) + 40, append + str(voter))

    lines = A4[0] / 5

    document.setLineWidth(10)
    for i in range(5):
        document.line(0 + (lines * i), A4[1], 0 + (lines * (i + 1)), 150)

    document.showPage()


document = canvas.Canvas(outputName, pagesize=A4)

for i in range(voteCount):
    createPage(i + 1)

document.save()