"""Create the P1.0 Tunisia purchase and calibration guide PDF."""

from pathlib import Path
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "P1_TUNISIA_PURCHASE_GUIDE.pdf"

NAVY = colors.HexColor("#182433")
BLUE = colors.HexColor("#2878B5")
LIGHT = colors.HexColor("#EDF3F7")
GREEN = colors.HexColor("#2A7A55")
AMBER = colors.HexColor("#B66B00")
RED = colors.HexColor("#A33A32")
GRAY = colors.HexColor("#66717D")


def P(text, style):
    return Paragraph(text, style)


def money(value):
    return value if isinstance(value, str) else f"{value:.3f} TND"


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D8DEE5"))
    canvas.line(14 * mm, 13 * mm, 196 * mm, 13 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(14 * mm, 8 * mm, "ELKATEB P1.0 - prototype purchasing guide - 27 Sep 2026")
    canvas.drawRightString(196 * mm, 8 * mm, f"Page {doc.page}")
    canvas.restoreState()


def styled_table(data, widths, header=True, font=7.6):
    header_style = ParagraphStyle(
        "TableHeader",
        fontName="Helvetica-Bold",
        fontSize=font,
        leading=font + 2,
        textColor=colors.white,
    )
    cell_style = ParagraphStyle(
        "TableCell",
        fontName="Helvetica",
        fontSize=font,
        leading=font + 2,
        textColor=colors.HexColor("#27313B"),
    )
    wrapped = []
    for row_index, row in enumerate(data):
        style = header_style if header and row_index == 0 else cell_style
        wrapped.append([Paragraph(str(value).replace("&", "&amp;"), style) for value in row])
    table = Table(wrapped, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), font),
        ("LEADING", (0, 0), (-1, -1), font + 2),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CAD2DA")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for row in range(1, len(data)):
        commands.append(("BACKGROUND", (0, row), (-1, row), colors.white if row % 2 else LIGHT))
    table.setStyle(TableStyle(commands))
    return table


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("TitleX", parent=styles["Title"], fontName="Helvetica-Bold",
                           textColor=NAVY, fontSize=24, leading=28, alignment=TA_LEFT,
                           spaceAfter=8)
    subtitle = ParagraphStyle("Subtitle", parent=styles["Normal"], textColor=GRAY,
                              fontSize=11, leading=15, spaceAfter=14)
    h1 = ParagraphStyle("H1X", parent=styles["Heading1"], textColor=NAVY,
                        fontSize=16, leading=20, spaceBefore=8, spaceAfter=8)
    h2 = ParagraphStyle("H2X", parent=styles["Heading2"], textColor=BLUE,
                        fontSize=12, leading=15, spaceBefore=7, spaceAfter=5)
    body = ParagraphStyle("BodyX", parent=styles["BodyText"], fontSize=9.2,
                          leading=13, textColor=colors.HexColor("#27313B"), spaceAfter=6)
    small = ParagraphStyle("SmallX", parent=body, fontSize=7.5, leading=10)
    callout = ParagraphStyle("Callout", parent=body, backColor=LIGHT,
                             borderColor=BLUE, borderWidth=0.8, borderPadding=8,
                             spaceBefore=5, spaceAfter=10)
    warning = ParagraphStyle("Warning", parent=body, backColor=colors.HexColor("#FFF1E1"),
                             borderColor=AMBER, borderWidth=0.8, borderPadding=8,
                             spaceBefore=5, spaceAfter=10)

    story = []
    story += [
        Spacer(1, 10 * mm),
        P("P1.0 Tunisia Purchase and Calibration Guide", title),
        P("Mostly printed sim-racing handbrake - Monday coupon plan, complete hardware list, local suppliers, and current price evidence", subtitle),
        P("Revision 1 - 27 September 2026", h2),
        P("<b>Decision:</b> print all eight coupon STLs once. They test different interfaces, not eight alternatives for one dimension. After the winning fits are measured, update the calibration parameters and regenerate P1.1 before printing the structural set.", callout),
        P("The functional P1 prototype has <b>19 printed parts</b>. The number 18 belongs to the later P1-C commercial mixed-material design; do not use 18 when ordering or printing P1.0.", warning),
        Spacer(1, 5 * mm),
        P("Budget snapshot", h1),
    ]

    budget = [
        ["Scope", "Planning cash requirement", "Confidence"],
        ["Mechanical hardware only", "Approximately 95-170 TND", "Engineering allowance; local per-piece quotes needed"],
        ["Electronics and sensor", "Approximately 45-60 TND", "Most items have current local listing evidence"],
        ["Complete purchased hardware", "Approximately 150-230 TND", "Excludes PETG, delivery, tools and failed prints"],
        ["PETG consumed by final 19 parts", "About 59 TND at 685 g / 86 TND per kg", "Engineering mass estimate; actual slicer result controls [S21]"],
        ["Recommended PETG stock", "2 x 1 kg = about 172 TND", "Includes coupons, development and reprint reserve [S21]"],
        ["Startup cash with two PETG spools", "Approximately 322-402 TND", "Hardware plus development filament; excludes delivery/tools"],
        ["Consumed value per successful unit", "Likely below cash purchase", "Packs, spare bearings and spring trials leave reusable stock"],
    ]
    story += [styled_table(budget, [52 * mm, 58 * mm, 72 * mm], font=8.1), Spacer(1, 4 * mm)]
    story += [P("Prices and stock were checked online on 27 September 2026. A displayed price is not a reservation. Call before travelling, especially for exact bolt lengths, springs, magnets, and steel stock.", small)]

    story += [PageBreak(), P("1. Monday: print and test all eight coupons", h1)]
    coupons = [
        ["File", "What it tests", "Physical item required"],
        ["COUPON_608_POCKETS_DEPTH_7.stl", "608 fit at 7 mm bearing depth", "Actual 608-2RS bearing"],
        ["COUPON_608_POCKETS_DEPTH_14.stl", "Deep/two-bearing pocket behaviour", "Actual 608-2RS bearing"],
        ["COUPON_M8_CLEARANCE.stl", "8.0/8.2/8.4/8.6 mm pivot clearances", "The actual M8 pivot bolt smooth shank"],
        ["COUPON_M6_CLEARANCE.stl", "6.0/6.2/6.4/6.6 mm bolt clearances", "Representative M6 bolt"],
        ["COUPON_M6_NUT_TRAPS.stl", "10.0/10.2/10.4/10.6 mm AF nut traps", "Actual M6 nuts"],
        ["COUPON_MAGNET_POCKETS.stl", "Nominal/+0.1/+0.2/+0.3 magnet fits", "Final candidate magnet"],
        ["COUPON_HALL_GAP_JIG.stl", "3/5/8/10/12/15 mm sensing experiments", "Magnet, SS49E, Pro Micro and multimeter"],
        ["COUPON_LOADED_BEARING_WALL.stl", "Representative bearing-wall strength and cracking", "Bearing, M8 bolt, washers and hand load"],
    ]
    story += [styled_table(coupons, [62 * mm, 66 * mm, 54 * mm], font=7.4)]
    story += [Spacer(1, 5 * mm), P("After testing", h2)]
    for text in [
        "Record the selected bearing diameter, M8 and M6 hole, M6 nut-trap size, magnet pocket, and printer/material/profile.",
        "Measure the bearing OD/width, bolt shank diameter, nut across-flats, magnet dimensions, steel-bar thickness, and coupling-nut dimensions with calipers.",
        "Send the results back. P1 parameters must be updated and P1.1 regenerated. Do not print the old 19 structural files immediately after choosing a coupon.",
        "After regeneration, print the eight-part mechanical core first. Add sensor/electronics and the six clamp parts only after the core passes no-spring and light-spring tests.",
    ]:
        story.append(P("- " + text, body))

    story += [PageBreak(), P("2. Exact mechanical shopping list", h1)]
    mech = [
        ["Qty", "Item/specification", "Use and buying note", "Price status"],
        ["1", "Mild-steel flat bar 25 x 5 x 280 mm", "Main lever. Confirm actual 25/5 mm before P1.1.", "QUOTE REQUIRED; allow 5-12 TND"],
        ["2", "Steel strips 25 x 3 x 180 mm", "Base reinforcement; four 6.6 mm holes each.", "QUOTE REQUIRED; allow 8-18 TND/pair"],
        ["4", "608-2RS, 8 x 22 x 7 mm", "Two installed and two coupon/spares.", "CONFIRMED 3.500 TND each; 14 TND total [S1]"],
        ["1", "M8 x 90 class 8.8 partially threaded bolt", "Pivot. Smooth shank must cross both inner races.", "EXACT LENGTH/SHANK QUOTE REQUIRED"],
        ["1", "8 ID x about 10 OD x 13.6 mm spacer tube", "Between the two bearing inner races.", "CUSTOM CUT / 3-8 TND allowance"],
        ["2 sets", "M8 washers/precision shims, 2.2 mm each side", "Equal tower-to-bearing spacer stacks, max 16 mm OD.", "MEASURE AND SELECT"],
        ["1", "M8 nyloc nut", "Pivot retention; do not overtighten.", "Local fastener shop"],
        ["1 set", "Extension springs, 15-20 mm OD, 60-100 mm hook length", "Buy several light/medium rates. CAD hook distance is 69.76-85.82 mm.", "QUOTE REQUIRED; allow 10-25 TND"],
        ["1", "M10 x 100 steel screw/rod", "Desk clamp; steel thread only.", "Local fastener shop; allow 3-7 TND"],
        ["1", "M10 coupling nut, about 30 mm, about 17 mm AF", "Captured clamp thread. Measure before P1.1.", "QUOTE REQUIRED; allow 3-8 TND"],
        ["1", "M10 swivel levelling foot/pad", "Lower clamp contact, compatible with 46 mm carrier.", "QUOTE REQUIRED; allow 5-15 TND"],
        ["1+1", "46 mm lower rubber and 90 x 62 x 2-3 mm upper rubber", "Desk protection and grip.", "ESTIMATED 5-10 TND"],
    ]
    story += [styled_table(mech, [13 * mm, 53 * mm, 76 * mm, 40 * mm], font=6.9)]

    story += [Spacer(1, 5 * mm), P("M6 structural fasteners", h2)]
    m6 = [
        ["Qty", "Size", "Location"],
        ["4", "M6 x 35", "Pivot towers through base/backing strips"],
        ["2", "M6 x 40", "Steel lever through hub"],
        ["2", "M6 x 25", "Spring module to base"],
        ["2", "M6 x 30", "Fixed and moving steel spring anchors"],
        ["1", "M6 x 45", "Moving travel-stop pin"],
        ["2", "M6 x 25 + rubber tips + locknuts", "Adjustable release/full-pull stops"],
        ["4", "M6 x 30", "Clamp interface through base"],
        ["4", "M6 x 30", "Clamp butt-joint connections"],
        ["2", "M6 rig bolts, length to suit rig", "Rig mounting with washers at least 18 mm OD"],
        ["25+", "M6 nyloc nuts", "Buy spares"],
        ["40+", "M6 standard and large washers", "Load spreading and adjustment"],
    ]
    story += [styled_table(m6, [18 * mm, 48 * mm, 116 * mm], font=7.5)]
    story += [P("Budget 20-35 TND for the M6 assortment if bought locally by piece. Online benchmark: Brico Direct lists 10 M6 x 20 stainless bolts at 4.500 TND and 10 M6 nut/washer sets at 2.500 TND; the required lengths still need local confirmation [S2].", small)]

    story += [PageBreak(), P("3. Small fasteners and electronics", h1)]
    small_hw = [
        ["Qty", "Item", "Use", "Buying note"],
        ["4", "M4 x 35 + washers + nylocs", "Two stop blocks", "Buy 6"],
        ["2", "M4 x 30 + washers + nylocs", "Hall fixed bracket", "Buy 4"],
        ["4", "M4 x 20 + washers + nylocs", "Electronics enclosure base", "Buy 6"],
        ["1", "M4 x 40 + nyloc", "Grip retention", "Buy 2"],
        ["4", "M3 x 20 + nuts", "Hall sled clamping", "Buy 6"],
        ["2 + 1", "M3 x 12 and M3 x 20", "Magnet holder/keeper", "Buy spares"],
        ["4", "M3 x 10 + four M3 heat-set inserts", "Electronics cover only", "Heat-set inserts are not structural"],
        ["2", "M2.5/M3 board screws", "Only after Hall PCB is measured", "Do not pre-drill from an assumed board"],
    ]
    story += [styled_table(small_hw, [17 * mm, 53 * mm, 66 * mm, 46 * mm], font=7.3)]

    electronics = [
        ["Qty", "Component", "Current local evidence", "Recommended action"],
        ["1", "Arduino Pro Micro 5 V / 16 MHz ATmega32U4", "CoThings: 28.000 TND, listed in stock [S3]", "Buy 1; USB cable not included"],
        ["2", "SS49E/49E linear Hall sensor", "Didactico: 2.400 TND; 2B Trading: 2.450 TND [S4/S5]", "Buy 2 so one is spare"],
        ["1 pair", "3-pin JST connector/cable", "Didactico JST 2.54 pair: 1.500 TND [S6]", "Verify pitch before soldering"],
        ["1", "Micro-USB data cable", "Little Son 1 m data/charge cable: 7.500 TND [S7]", "Must carry data, not charge-only"],
        ["1", "6 mm heat-shrink", "Didactico: 2.200 TND [S8]", "For 3-wire sensor loom"],
        ["2", "10 x 5 x 3 mm NdFeB block magnet", "Exact Tunisian listing not confirmed", "Current P1 pocket candidate; do not substitute silently"],
        ["candidate", "20 x 10 x 2 mm rectangular NdFeB magnet", "Celectronix: 1.499 TND, listed in stock [S19]", "Best locally listed rectangular candidate; requires revised magnet coupon/holder"],
        ["candidate", "12 x 4 mm circular NdFeB magnet", "SELI: 1.800 TND, listed in stock [S20]", "Compact local candidate; requires revised magnet coupon/holder"],
        ["optional", "10 x 2 mm N35 disc magnet", "2B Trading: 1.200 TND [S9]", "Experimental alternative only; requires matching pocket/calibration"],
        ["as needed", "Flexible 3-core wire, solder, cable ties", "Didactico/CoThings/local electronics", "Allow 5-10 TND"],
    ]
    story += [Spacer(1, 5 * mm), styled_table(electronics, [15 * mm, 51 * mm, 65 * mm, 51 * mm], font=6.9)]

    story += [PageBreak(), P("4. Where to buy in Tunisia", h1)]
    vendors = [
        ["Supplier", "Useful items", "Address/contact", "Status"],
        ["Tunisie Roulements", "608-2RS", "6 Rue Chedly Kallala, Lafayette, Tunis 1002. 71 287 737 / 58 578 870.", "608 listing and price confirmed [S1/S10]"],
        ["Brico Direct", "Fastener packs, nuts, washers, ties, tools", "71bis Avenue Louis Braille, Tunis 1082. 71 100 950.", "Prices are benchmarks; call for exact lengths [S2/S11]"],
        ["SEGEMO - Maison du boulon", "M3/M4/M6/M8/M10 bolts, nylocs, washers, shims", "10 Rue Aid Jaberi, Tunis 1000. 71 253 878.", "Range confirmed; prices by counter quote [S12]"],
        ["CoThings", "Pro Micro and electronics", "Route X, near Stade Bardo, Bardo, Tunis. 29 750 003 / 27 772 264.", "Pro Micro price/stock listed [S3/S13]"],
        ["Little Son", "Pro Micro alternative, USB cable, M3 hardware", "1 Rue de Piree, Tunis 1001. 58 114 788.", "Pro Micro listed 35 TND; cable 7.5 TND [S7/S14]"],
        ["Tuni Smart Innovation", "SS49E, magnets, heat-shrink", "1 Rue Pierre Mendes France, Ariana 2080. 51 954 443 / 51 954 448.", "SS49E in stock; many magnets currently out of stock [S15]"],
        ["Celectronix", "20 x 10 x 2 mm rectangular magnet, electronics, PETG", "Centre Said, Avenue Habib Bourguiba, Megrine. 79 295 570 / 27 582 469 / 28 581 332.", "Magnet 1.499 TND; LUME PETG 1 kg 86 TND, listings in stock [S19/S21]"],
        ["SELI", "12 x 4 mm circular magnet and magnet alternatives", "08 Rue Chedhly Kallela, 1st floor, Boumhel 2097. 29 002 608 / 92 168 725 / 55 560 037.", "12 x 4 magnet listed in stock at 1.800 TND [S20]"],
        ["Didactico", "Hall, JST, heat-shrink, wire", "Cite des Martyrs, Rue Mohamed Salah, Imm. Bouzguenda A01, Sfax. 54 776 776 / 99 707 685.", "Listings/prices confirmed; delivery in Tunisia [S4/S6/S8/S16]"],
        ["MTR Ressorts", "Extension-spring prototype or small batch", "ZI El Ons, Route de Tunis Km 10, Sakiet Ezzit 3021 Sfax. 98 333 883 / 98 331 896.", "Local manufacturer; quotation required [S17]"],
        ["ITI / Ressorts Mohamed Benaissa", "Extension spring in Tunis", "11 Rue Abderrahmen Azzem, Montplaisir, Tunis 1002. 71 908 311.", "Local manufacturer; quotation required [S18]"],
    ]
    story += [styled_table(vendors, [31 * mm, 43 * mm, 72 * mm, 36 * mm], font=6.6)]

    story += [Spacer(1, 5 * mm), P("What to say at the quincaillerie", h2)]
    story.append(P("Show the fastener table and say: 'Je veux des vis metriques zinguées ou classe 8.8, avec rondelles et ecrous Nylstop. Pour l'axe M8, il me faut une partie lisse qui traverse deux roulements 608; le filetage ne doit pas rouler dans les bagues.' Ask them to measure the smooth shank before you buy.", callout))
    story.append(P("For the spring supplier: ask for a small selection of extension springs with closed hooks, 15-20 mm outside diameter and 60-100 mm free hook-to-hook length. Explain that the installed hook distance changes from about 69.8 to 85.8 mm and that the first unit is for force testing, not a production order.", body))
    story.append(P("For the magnet: the Celectronix 20 x 10 x 2 mm rectangular magnet is the closest useful locally listed shape, while SELI's 12 x 4 mm disc is the more compact option. Neither is a drop-in fit for the released 10 x 5 x 3 mm pocket. Buy one or two samples if convenient, measure them with calipers, and send the dimensions; only the magnet coupon and holder then need to be revised before structural printing.", warning))

    story += [PageBreak(), P("5. Assembly purchase gates", h1)]
    gates = [
        ["Gate", "Must be available/measured", "Do not proceed if"],
        ["Coupon gate", "608, M8 sample, M6 bolt/nut, magnet, printer profile", "You cannot physically select the fit"],
        ["P1.1 regeneration", "Winning coupon sizes and real hardware dimensions", "The existing P1.0 fit assumptions are still unverified"],
        ["Mechanical core", "Base/towers/hub/grip, steel lever/strips, bearings, pivot stack, stops", "Threads touch bearing races or towers spread"],
        ["Spring gate", "Light spring, steel anchors, positive mechanical stops", "Spring becomes the travel stop or rubs printed parts"],
        ["Clamp gate", "M10 steel screw/nut, swivel foot, rubber pads", "Any primary clamp thread is printed plastic"],
        ["Sensor gate", "Magnet mechanically retained, fixed SS49E, 3-wire loom", "Magnet or sensor can collide with the lever"],
        ["Electronics gate", "Pro Micro and data-capable USB cable", "Windows does not enumerate the USB HID device"],
    ]
    story += [styled_table(gates, [34 * mm, 78 * mm, 70 * mm], font=7.2)]
    story += [Spacer(1, 6 * mm), P("Important limitations", h2)]
    for text in [
        "Do not buy a precision production spring before the first pull-force test.",
        "Do not allow threaded M8 sections to act as the bearing journal if a smooth-shank bolt or 8 mm shaft is available.",
        "Do not print all 19 parts from the uncalibrated P1.0 export merely because one coupon looks correct; all critical coupon results must be transferred into P1.1.",
        "The listed prices exclude delivery and may change. 'Confirmed' means the retailer displayed the item/price at research time, not that stock has been reserved.",
        "Structural capacity remains a physical-test question. Stop at cracking, whitening, permanent deformation, bearing movement, or fastener loosening.",
    ]:
        story.append(P("- " + text, body))

    story += [PageBreak(), P("6. Source register", h1)]
    sources = [
        ("S1", "Tunisie Roulements - 608-2RS, 3.500 TND", "https://tunisie-roulements.tn/produit/roulement-608-2rs/"),
        ("S2", "Brico Direct - visserie listings and pack prices", "https://brico-direct.tn/208-vis-et-boulons"),
        ("S3", "CoThings - Pro Micro 5V/16MHz, 28.000 TND", "https://cothings.net/products/arduino-pro-micro-mini-usb-atmega32u4-5v-16mhz"),
        ("S4", "Didactico - SS49E, 2.400 TND", "https://didactico.tn/categorie-produit/capteurs-prototypage/capteurs/capteurs-magnetiques-hall/"),
        ("S5", "2B Trading - SS49E, 2.450 TND", "https://2btrading.tn/transistor-igbt/4950-capteur-effet-hall-49e-oh49e-ss49e.html"),
        ("S6", "Didactico - JST 3-pin pair, 1.500 TND", "https://didactico.tn/categorie-produit/connectique-cables-boitiers/"),
        ("S7", "Little Son - 1 m Micro-USB data cable, 7.500 TND", "https://little-son.tn/2-accueil?page=2"),
        ("S8", "Didactico - 6 mm heat-shrink, 2.200 TND", "https://didactico.tn/produit/gaine-thermoretractable-drs-6/"),
        ("S9", "2B Trading - 10 x 2 mm N35 disc magnet, 1.200 TND", "https://2btrading.tn/2-accueil?page=80"),
        ("S10", "Tunisie Roulements contact", "https://tunisie-roulements.tn/contact/"),
        ("S11", "Brico Direct store/contact", "https://brico-direct.tn/magasins"),
        ("S12", "SEGEMO contact", "https://www.segemo.tn/contact/"),
        ("S13", "CoThings store location", "https://cothings.net/pages/emplacement-du-magazin"),
        ("S14", "Little Son Pro Micro listing, 35.000 TND", "https://little-son.tn/accueil/97-arduino-pro-micro-atmega-32u4.html"),
        ("S15", "Tuni Smart SS49E and store address", "https://tuni-smart-innovation.com/products/capteur-a-effet-hall-lineaire-ss49e-oh49e"),
        ("S16", "Didactico store/contact", "https://didactico.tn/a-propos-didactico/"),
        ("S17", "MTR Ressorts", "https://mtr-ressorts.tn/fr"),
        ("S18", "ITI Tunisie", "https://iti.com.tn/presentation/"),
        ("S19", "Celectronix - 20 x 10 x 2 mm rectangular neodymium magnet, 1.499 TND, listed in stock", "https://www.celectronix.com/autres-mecanique/7498-aimant-cylindrique-de-n-odyme-16-mm-de-diam-tre-x-1-8-mm-d-paisseur-copie-.html"),
        ("S20", "SELI - 12 x 4 mm circular neodymium magnet, 1.800 TND, listed in stock", "https://seli.tn/product-category/aimant-et-electro-aimant/"),
        ("S21", "Celectronix - LUME PETG 1.75 mm, 1 kg, 86.000 TND, multiple colors listed in stock", "https://www.celectronix.com/filament-petg/8156--074-0-barre-led-tv-lg-43uk6565-7led-3v-44-5cm.html"),
    ]
    for sid, label, url in sources:
        story.append(P(f"<b>{sid}</b> - <link href='{url}' color='#2878B5'>{label}</link><br/><font size='7'>{url}</font>", small))

    story += [Spacer(1, 8 * mm), P("Prepared from the released P1.0 BOM and current public Tunisian retailer/manufacturer pages. This is a prototype purchasing plan, not a supplier quotation or guarantee of compatibility.", callout)]

    doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=14 * mm, leftMargin=14 * mm,
                            topMargin=15 * mm, bottomMargin=18 * mm,
                            title="P1.0 Tunisia Purchase and Calibration Guide",
                            author="ELKATEB Handbrake Project")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUT)


if __name__ == "__main__":
    build()
