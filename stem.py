#!/usr/bin/env python3

# Sett antall eksemplarer i "antall" variablen
# Hvis programmet kjøres med et vilkårlig parameter
# Vil tale-lappen få en X-<nr>, og ikke stemmeseddel
# Endre riktig tekst i drawstring til å bli årstall

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from colorsys import hls_to_rgb
import sys


VOTE_COUNT = 50
NON_MEMBER_COUNT = 20
BALLOT_COUNT = 10
YEAR = "V2019"
OUTPUT_NAME = "stem.pdf"

BALLOT_HEIGHT = 200


def _draw_ballots_front(amount: int):
    """Draws ballots on the bottom of the page

    :param amount: The amount of ballots to create
    """
    # The line above the ballots
    document.line(0, BALLOT_HEIGHT, A4[0], BALLOT_HEIGHT)

    ballot_size = A4[0] / amount
    for ballot in range(amount):
        document.rotate(90)
        document.drawCentredString(
            BALLOT_HEIGHT / 2, -15 + (-ballot_size * ballot),
            "Seddel {} - {}".format(ballot + 1, YEAR)
        )

        document.rotate(-90)
        hue = 1.0 / (amount / 2) * (ballot // 2)
        hls = hls_to_rgb(hue if ballot % 2 else (hue + .5) % 1, 0.6, 0.8)
        document.setFillColorRGB(hls[0], hls[1], hls[2])
        document.roundRect((ballot_size * (ballot + 1)) - 25, 7.5, 20, BALLOT_HEIGHT - 15, 10, 1, 1)
        document.setFillColorRGB(0, 0, 0)

        # Separator to next ballot
        document.line(ballot_size * ballot, BALLOT_HEIGHT, ballot_size * ballot, 0)


def _draw_ballots_back(amount: int, choices: int = 6):
    """Draws ballots on the bottom of the page

    :param amount: The amount of ballots to create
    """
    # The line above the ballots
    document.line(0, BALLOT_HEIGHT, A4[0], BALLOT_HEIGHT)

    ballot_size = A4[0] / amount
    for ballot in range(amount):

        document.rotate(90)
        # Create the choice
        for choice in range(0, choices // 2):
            document.drawString(
                5,
                -15 - (ballot_size * (choice - choices // 2) / (choices // 2)) - ballot_size * (ballot + 1),
                "{}.".format(choice + 1)
            )

        for choice in range(choices // 2, choices):
            document.drawString(
                BALLOT_HEIGHT / 2,
                -15 - (ballot_size * (choice - choices // 2) / (choices // 2)) - ballot_size * ballot,
                "{}.".format(choice + 1)
            )

        document.rotate(-90)
        # Separator to next ballot
        document.line(ballot_size * ballot, BALLOT_HEIGHT, ballot_size * ballot, 0)


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


def _draw_page_lines(amount_lines: int = 5):
    """Draws lines accross the page

    :param amount_lines: The amount of lines that will get created
    """
    lines = A4[0] / amount_lines
    document.setLineWidth(10)
    for line_number in range(amount_lines):
        document.line(
            lines * line_number, A4[1],
            lines * (line_number + 1), BALLOT_HEIGHT
        )


def create_slip(voter: int, *, member: bool):
    """Creates a two sided slip.

    :param voter: The voter's number
    :param member: Is this slip for a member?
    """
    # Front page
    if member:
        _draw_ballots_front(BALLOT_COUNT)
    document.setFont("Helvetica-Bold", 300)
    _draw_voter(voter, member)
    document.showPage()

    # Back page
    if member:
        _draw_ballots_back(BALLOT_COUNT)
    document.setFont("Helvetica-Bold", 300)
    _draw_voter(voter, member)
    _draw_page_lines()
    document.showPage()


if __name__ == "__main__":
    document = canvas.Canvas(OUTPUT_NAME, pagesize=A4)

    for voter in range(1, VOTE_COUNT):
        create_slip(voter, member=True)

    # These are for non-member participants of the general assembly
    for voter in range(1, NON_MEMBER_COUNT):
        create_slip(voter, member=False)

    document.save()

