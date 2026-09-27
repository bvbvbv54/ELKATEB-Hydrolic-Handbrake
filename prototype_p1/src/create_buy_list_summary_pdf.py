"""Create the concise P1 Tunisia shopping summary and coupon guide PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "P1_BUY_LIST_SUMMARY_TUNISIA.pdf"

NAVY = colors.HexColor("#182433")
BLUE = colors.HexColor("#2878B5")
LIGHT = colors.HexColor("#EDF3F7")
GREEN = colors.HexColor("#237A57")
GREEN_BG = colors.HexColor("#E9F6EF")
AMBER = colors.HexColor("#A86400")
AMBER_BG = colors.HexColor("#FFF3DF")
RED = colors.HexColor("#A13D35")
GRAY = colors.HexColor("#67717D")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D5DDE5"))
    canvas.line(14 * mm, 13 * mm, 196 * mm, 13 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(14 * mm, 8 * mm, "ELKATEB P1 - Tunisia buy list - checked 27 Sep 2026")
    canvas.drawRightString(196 * mm, 8 * mm, f"Page {doc.page}")
    canvas.restoreState()


def make_table(data, widths, font=7.2):
    head = ParagraphStyle(
        "TableHead", fontName="Helvetica-Bold", fontSize=font,
        leading=font + 2, textColor=colors.white,
    )
    cell = ParagraphStyle(
        "TableCell", fontName="Helvetica", fontSize=font,
        leading=font + 2, textColor=colors.HexColor("#27313B"),
    )
    rows = []
    for row_index, row in enumerate(data):
        style = head if row_index == 0 else cell
        rows.append([Paragraph(str(value), style) for value in row])
    table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C8D1DA")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for index in range(1, len(rows)):
        commands.append(("BACKGROUND", (0, index), (-1, index), colors.white if index % 2 else LIGHT))
    table.setStyle(TableStyle(commands))
    return table


def link(label, url):
    return f"<link href='{url}' color='#2878B5'><u>{label}</u></link>"


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "Title", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=23, leading=27, textColor=NAVY, alignment=0, spaceAfter=6,
    )
    subtitle = ParagraphStyle(
        "Subtitle", parent=styles["Normal"], fontSize=10.5, leading=14,
        textColor=GRAY, spaceAfter=10,
    )
    h1 = ParagraphStyle(
        "H1", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=15, leading=19, textColor=NAVY, spaceBefore=5, spaceAfter=7,
    )
    h2 = ParagraphStyle(
        "H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=11.5, leading=14, textColor=BLUE, spaceBefore=6, spaceAfter=4,
    )
    body = ParagraphStyle(
        "Body", parent=styles["BodyText"], fontSize=9, leading=12.5,
        textColor=colors.HexColor("#27313B"), spaceAfter=5,
    )
    small = ParagraphStyle("Small", parent=body, fontSize=7.5, leading=10)
    total = ParagraphStyle(
        "Total", parent=body, fontName="Helvetica-Bold", fontSize=11,
        leading=15, backColor=GREEN_BG, borderColor=GREEN,
        borderWidth=0.9, borderPadding=8, spaceBefore=6, spaceAfter=7,
    )
    warning = ParagraphStyle(
        "Warning", parent=body, backColor=AMBER_BG, borderColor=AMBER,
        borderWidth=0.8, borderPadding=7, spaceBefore=5, spaceAfter=8,
    )

    online = [
        ["Buy", "Exact product", "Shop / online link", "Unit", "Line total"],
        ["4", "608-2RS bearing, 8 x 22 x 7 mm", link("Tunisie Roulements", "https://tunisie-roulements.tn/produit/roulement-608-2rs/"), "3.500", "14.000 TND"],
        ["1", "Arduino Pro Micro, ATmega32U4, 5 V / 16 MHz", link("CoThings product", "https://cothings.net/products/arduino-pro-micro-mini-usb-atmega32u4-5v-16mhz"), "28.000", "28.000 TND"],
        ["2", "SS49E linear Hall sensor", link("Tuni Smart product", "https://tuni-smart-innovation.com/products/capteur-a-effet-hall-lineaire-ss49e-oh49e"), "2.500", "5.000 TND"],
        ["1", "JST 2.54 mm, 3-pin female cable + male header", link("Didactico product", "https://didactico.tn/produit/cable-connecteur-femelle-jst-2-54-3pin-connecteur-male/"), "1.500", "1.500 TND"],
        ["1", "USB-A to Micro-USB data cable, 1 m", link("Didactico product", "https://didactico.tn/produit/cable-usb-micro-usb-1m-bleu/"), "6.000", "6.000 TND"],
        ["1", "DRS-6 heat-shrink, 6 mm, 2:1", link("Didactico product", "https://didactico.tn/produit/gaine-thermoretractable-drs-6/"), "2.200", "2.200 TND"],
        ["2", "Neodymium magnet, rectangular 20 x 10 x 2 mm", link("Celectronix product", "https://www.celectronix.com/autres-mecanique/7498-aimant-cylindrique-de-n-odyme-16-mm-de-diam-tre-x-1-8-mm-d-paisseur-copie-.html"), "1.499", "2.998 TND"],
    ]

    story = [
        Spacer(1, 4 * mm),
        Paragraph("P1 Buy List Summary - Tunisia", title),
        Paragraph("What to buy for the first complete printed prototype, with direct product links and a clear budget total.", subtitle),
        Paragraph("1. Exact online products", h1),
        make_table(online, [12 * mm, 62 * mm, 54 * mm, 24 * mm, 30 * mm], font=7.0),
        Paragraph("<b>Confirmed-price online subtotal: 59.698 TND</b> (before delivery).", total),
        Paragraph(
            "The magnet is a locally available candidate, not a drop-in fit. The released holder was made around a 10 x 5 x 3 mm block. "
            "If the 20 x 10 x 2 mm magnet is purchased, measure it with calipers and print only a revised magnet coupon/holder before the structural set.",
            warning,
        ),
        Paragraph("Optional printing material", h2),
    ]

    filament = [
        ["Choice", "Product / planning basis", "Price", "What it means"],
        ["If Amine has enough PETG", "Use his stock after slicer confirmation", "0 TND purchase", "Ask for remaining grams and actual slicer estimate"],
        ["Minimum new spool", link("LUME PETG 1.75 mm, 1 kg", "https://www.celectronix.com/filament-petg/8156--074-0-barre-led-tv-lg-43uk6565-7led-3v-44-5cm.html"), "86.000 TND", "Covers the 685 g final-parts estimate, but little reprint reserve"],
        ["Recommended development stock", "Two 1 kg PETG spools", "172.000 TND", "Covers coupons, all final parts and useful reprint reserve"],
    ]
    story += [make_table(filament, [42 * mm, 58 * mm, 30 * mm, 52 * mm], font=7.1)]
    story += [
        Paragraph("Current engineering estimates: coupons 233 g; final 19 parts 685 g; all 27 pieces 918 g. Amine's real slicer result replaces these planning values.", small),
        PageBreak(),
        Paragraph("2. Buy locally from a quincaillerie / metal shop", h1),
    ]

    hardware = [
        ["Group", "Exact requirement", "Budget"],
        ["Steel", "1 x 25 x 5 x 280 mm flat bar; 2 x 25 x 3 x 180 mm reinforcement strips", "13-30 TND"],
        ["M8 pivot stack", "1 x M8 x 90 class 8.8 partially threaded bolt; 1 nyloc; washers/shims; 8 ID x about 10 OD x 13.6 mm spacer", "10-25 TND"],
        ["M6 bolts", "4 x 35; 2 x 40; 4 x 25; 10 x 30; 1 x 45; plus 2 rig bolts to suit rig", "20-35 TND incl. nuts/washers"],
        ["M6 nuts/washers", "At least 25 nyloc nuts and 40 washers, including large load-spreading washers", "Included above"],
        ["M4 hardware", "4 x M4x35; 2 x M4x30; 4 x M4x20; 1 x M4x40; matching washers/nylocs", "6-12 TND"],
        ["M3 hardware", "5 x M3x20; 2 x M3x12; 4 x M3x10; nuts/washers; 4 x M3 heat-set inserts", "4-8 TND"],
        ["Spring trials", "Extension springs: 15-20 mm OD, 60-100 mm hook-to-hook; buy light and medium samples", "10-25 TND"],
        ["Desk clamp", "M10 x 100 screw/rod; M10 coupling nut about 30 mm; swivel foot; 46 mm lower rubber; 90 x 62 x 2-3 mm upper rubber", "16-40 TND"],
    ]
    story += [make_table(hardware, [38 * mm, 104 * mm, 40 * mm], font=7.1)]
    story += [
        Paragraph("<b>Local mechanical estimate: 79-175 TND.</b> These are planning allowances, not confirmed shop quotations.", warning),
        Paragraph("Totals", h2),
    ]

    totals = [
        ["Scenario", "Estimated cash total"],
        ["Hardware + electronics, Amine supplies filament", "139-235 TND"],
        ["Hardware + electronics + one new 1 kg PETG spool", "225-321 TND"],
        ["Hardware + electronics + recommended two PETG spools", "311-407 TND"],
    ]
    story += [make_table(totals, [112 * mm, 70 * mm], font=8.0)]
    story += [
        Paragraph("The total excludes delivery, tools, failed prints and optional spare fastener packs. Call/check stock before paying because web prices and availability can change.", small),
        Paragraph("Suggested shops", h2),
        Paragraph("<b>Bearings:</b> Tunisie Roulements, 6 Rue Chedly Kallala, Lafayette, Tunis 1002. <b>Bolts:</b> SEGEMO, 10 Rue Aid Jaberi, Tunis 1000. <b>Electronics:</b> CoThings, Route X near Stade Bardo; Tuni Smart, 1 Rue Pierre Mendes France, Ariana; Didactico, Cite des Martyrs, Sfax. <b>Magnet:</b> Celectronix, Centre Said, Avenue Habib Bourguiba, Megrine.", body),
        PageBreak(),
        Paragraph("3. The eight test pieces: directory and reason", h1),
        Paragraph("Send this folder to the printer:", body),
        Paragraph("<b>C:\\Users\\moham\\OneDrive\\Documents\\Handbrake-Elkateb\\<br/>prototype_p1\\printer_handoff_amine\\<br/>01_CALIBRATION_FIRST\\</b>", warning),
        Paragraph("Why eight? They are eight different tests. They are not eight versions of the same part. Print each file once for the first calibration run.", body),
    ]

    coupons = [
        ["File", "Why it is printed"],
        ["COUPON_608_POCKETS_DEPTH_7.stl", "Chooses the correct single-bearing pocket fit for Amine's printer/material."],
        ["COUPON_608_POCKETS_DEPTH_14.stl", "Checks the deeper two-bearing hub pocket; deep holes can print differently."],
        ["COUPON_M8_CLEARANCE.stl", "Selects the M8 pivot clearance using the actual smooth bolt shank."],
        ["COUPON_M6_CLEARANCE.stl", "Selects clearance for the structural M6 bolts."],
        ["COUPON_M6_NUT_TRAPS.stl", "Selects the nut-trap across-flats size so nuts fit without spinning."],
        ["COUPON_MAGNET_POCKETS.stl", "Checks magnet retention. Revise this coupon only if using the 20 x 10 x 2 mm local magnet."],
        ["COUPON_HALL_GAP_JIG.stl", "Tests Hall response at 3, 5, 8, 10, 12 and 15 mm gaps."],
        ["COUPON_LOADED_BEARING_WALL.stl", "Checks representative PETG bearing-wall cracking/deformation before the full hub is printed."],
    ]
    story += [make_table(coupons, [75 * mm, 107 * mm], font=7.5)]
    story += [
        Paragraph("After the first run", h2),
        Paragraph("1. Test every coupon with the actual purchased hardware. 2. Record the winning hole/pocket/nut-trap sizes and send photos/measurements. 3. Only failed or changed coupons are reprinted. 4. Regenerate P1.1. 5. Print the 19 final functional parts - not the old uncalibrated set.", body),
        Paragraph("The number 18 refers to the later mixed-material P1-C design. The mostly printed P1/P1.1 prototype has 19 final printed parts.", warning),
    ]

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm,
        topMargin=14 * mm, bottomMargin=18 * mm,
        title="P1 Buy List Summary - Tunisia",
        author="ELKATEB Handbrake Project",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUT)


if __name__ == "__main__":
    build()
