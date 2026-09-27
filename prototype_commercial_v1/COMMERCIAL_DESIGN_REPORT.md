# Commercial design report

## Executive result

P1-C replaces the printed P1 chassis with a sheet-metal architecture while preserving its proven kinematic principles. The visible product is black powder-coated steel, brushed aluminium, a black grip, and one red spring collar. Internal printed parts are serviceable and visually screened.

## Final CAD dimensions

- Base: 190 × 88 × 18 mm folded envelope.
- Complete released-state CAD envelope: 190 × 88 × 371.4 mm.
- Complete full-pull CAD envelope: 265.3 × 88 × 318.2 mm; the grip sweeps beyond the base length.
- Pivot centre: X58, Y44, Z76 mm.
- Side-frame inner gap: 34 mm.
- Rotating hub: 30 mm wide, Ø50 mm main body.
- Bearings: 2 × 608, nominal 8 × 22 × 7 mm.
- Lever: 5 mm steel, 300 mm pivot-to-end, three Ø10 lightening holes outside the root; nominal hand radius 245 mm.
- Grip: Ø34 × 112 mm over Ø22 mm core.
- Travel: 75° released to 50° full pull.
- Desk range: 10–55 mm; clamp throat 65 mm; M10 × 120 candidate.
- Electronics pod: 54 × 64 × 30 mm nominal outer envelope.

## Materials and processes

- Steel: base tray, left/right structural frames, lever, spring bracket, clamp bracket.
- Aluminium: left/right non-structural accent panels; commodity grip core representation.
- Printed: hub, magnet carrier, Hall window, Hall sled, electronics pod/lid, cable guide, knob, pad carrier, spring collar.
- Purchased: pivot bolt, bearings, spacers/washers, spring, grip, M3/M4/M6 hardware, M10 clamp hardware, magnet, Hall board, controller, USB.

## Mass and sheet use

- CAD steel mass: 1480 g.
- CAD aluminium mass: 27 g.
- Printed solid-volume reference mass: 266 g; actual sliced mass will be lower and profile-dependent.
- Purchased hardware planning allowance: 430 g.
- Estimated assembled mass: 2203 g.
- Steel net area per unit: 0.06284 m²; about 23 units per 1000 × 2000 sheet at 75% planning utilization.
- Aluminium net area per unit: 0.00504 m²; about 297 units per sheet at the same planning utilization.

## Pivot arrangement

M8 partial-thread bolt through 3 mm steel side frames, 2 mm external spacers, two 608 inner races, and a 15.6 mm inner-race spacer. The 30 mm carrier holds two 7.2 mm-deep pockets. Smooth shank must cross both inner races; purchased bolt shank length is MEASURE BEFORE BUILD.

## Spring and stops

One extension spring connects an M6 moving hub anchor at 45 mm radius to a three-position M6 steel anchor near X123/Z25. Spring length is 77.0 mm released, 86.5 mm mid, and 95.4 mm full. Two tangent M6 stops define endpoints independently from sensing.

## Magnetic system

The magnet follows a 55 mm radius and approaches a fixed Hall position monotonically: 24.553, 18.896, 13.394, 8.483, 6.0 mm at 0/25/50/75/100%. The right steel frame has a 38 mm capsule window around the full path; a plastic insert and aluminium outer layer preserve local non-ferromagnetic packaging. Exact field linearity is MAGNETIC-FIELD TEST REQUIRED.

## Clamp and rig mounting

The removable two-bend 3 mm steel bracket carries clamp load into four M6 base bolts. A captured/welded M10 coupling nut carries thread load. Printed parts only form the knob and pad carrier. Two 44 × 7 mm rig slots remain independent.

## Cost status

At quantity 25, the planning direct-material/component subtotal excluding assembly and packaging is **87.8 TND**, and the full planning allowance is **100.8 TND**. These are ESTIMATED/UNKNOWN_RFQ planning values, not Tunisian quotes. At 150–200 TND retail, this alpha is only plausible near the upper end unless local sheet-processing and electronics quotes beat the allowances.

## P1C-MID and P1C-PRO

MID uses powder-coated steel, brushed flat accents, commodity grip, PETG/ASA internal parts, standard 608 bearings, and Pro Micro/custom low-cost PCB. PRO retains the same tray, pivot, Hall system, clamp and mounting, then upgrades grip, accent finish/thickness, fastener finish, spring adjustment, sealed bearings, and PCB/USB module. It is not a second unrelated product.

## Required validation

No safety factor or production claim is made. Test pivot wear, lever proof load, frame spreading, base bending, stop impacts, spring fatigue, clamp slip, desk marking, Hall monotonicity near steel, USB cable retention, and finish durability before sale.
