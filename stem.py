#!/usr/bin/env python3

# Sett antall eksemplarer i "antall" variablen
# Hvis programmet kjøres med et vilkårlig parameter
# Vil tale-lappen få en X-<nr>, og ikke stemmeseddel
# Endre riktig tekst i drawstring til å bli årstall

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from colorsys import hls_to_rgb
import sys


VOTE_COUNT = 70
NON_MEMBER_COUNT = 20
BALLOT_COUNT = 13
YEAR = "V2019"
OUTPUT_NAME = "stem.pdf"


def _draw_ballots(amount: int):
    """Draws ballots on the bottom of the page

    :param amount: The amount of ballots to create
    """
    ballots = A4[0] / amount

    document.line(0, 150, A4[0], 150)

    for ballot in range(amount):
        document.rotate(90)
        document.drawString(
            25, -15 + (-ballots * ballot),
            "Seddel {} - {}".format(ballot + 1, YEAR)
        )

        document.rotate(-90)
        document.line(ballots * ballot, 150, ballots * ballot, 0)

        saturation = [0.4, 0.75]
        hls = hls_to_rgb(1.0 / amount * ballot, saturation[ballot % 2], 0.9)

        document.setFillColorRGB(hls[0], hls[1], hls[2])
        document.roundRect((ballots * (ballot + 1)) - 25, 7.5, 20, 135, 10, 1, 1)
        document.setFillColorRGB(0, 0, 0)


def _draw_voter(voter: int, member: bool):
    """Draws the voters number

    Will place a X in front of their name to indicate that they're
    not a member if "member" is false.

    :param voter: The number of the voter
    :param member: Is the person a member.
    """
    document.drawCentredString(
        (A4[0] / 2),
        (A4[1] / 2) + 40,
        "{}{}".format("" if member else "X", voter))

def _draw_page_lines():
    lines = A4[0] / 5
    document.setLineWidth(10)
    for line_number in range(5):
        document.line(
            lines * line_number, A4[1],
            lines * (line_number + 1), 150
        )


def create_slip(voter: int, *, member: bool):
    """"""
    # Front page
    if member:
        _draw_ballots(BALLOT_COUNT)
    document.setFont("Helvetica-Bold", 300)
    _draw_voter(voter, member)
    document.showPage()

    # Back page
    document.setFont("Helvetica-Bold", 300)
    _draw_voter(voter, member)
    _draw_page_lines()
    document.showPage()


if __name__ == "__main__":
    document = canvas.Canvas(OUTPUT_NAME, pagesize=A4)

    for voter in range(1, VOTE_COUNT):
        create_slip(voter, member=True)

    for voter in range(1, NON_MEMBER_COUNT):
        create_slip(voter, member=False)

    document.save()

