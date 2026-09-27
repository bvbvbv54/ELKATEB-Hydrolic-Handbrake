# Design decisions

## P1.0 to P1-C design map

|Disposition|P1.0 principle/component|P1-C implementation|
|---|---|---|
|Retained|M8 pivot + two 608 bearings|Same bearing architecture inside a hidden 30 mm carrier; 34 mm steel-frame gap|
|Retained|75° to 50° motion|Released, 25%, mid, 75%, and full CAD states|
|Retained|Steel lever load path|Original tapered 5 mm laser-cut mild-steel lever|
|Retained|Extension spring + independent stops|Commodity spring, M6 steel anchors, two replaceable M6 stops|
|Retained|Moving magnet / fixed Hall|Protected non-ferromagnetic window and adjustable 3–15 mm sled|
|Retained|M10 clamp and rig mount|Removable bent-steel C bracket plus independent M6 rig slots|
|Redesigned|Printed base and towers|190 × 88 mm 3 mm bent-steel tray and two bent-steel side frames|
|Redesigned|Straight 25 × 5 bar|Tapered profile with three Ø10 controlled apertures outside the root section|
|Redesigned|Separate electronics box|Tapered removable rear equipment pod integrated into silhouette|
|Hidden|Hall sled, carrier, wires, PCB, stops|Located behind side layers and removable pod/cover|
|Real structural visual part|Black side body|Powder-coated 3 mm steel frames and tray|
|Low-cost visual part|Silver machined-looking layer|Two flat 2 mm brushed-aluminium non-structural accent panels|
|Rejected|Hydraulic/red damper|Red spring collar/guide around inexpensive extension spring|
|Rejected|Billet CNC chassis, RGB, many machined caps|Laser cutting, simple bends, standard fasteners, restrained CMF|


## Visual translation

The supplied renders establish the visual hierarchy: a low black base, black inner structure, bright side layers, vertical cylindrical grip, exposed but controlled spring, clean pivot rings, and a rear equipment mass. P1-C implements that hierarchy as real manufacturing layers. The accents remain non-structural so their finish can change without revalidating the primary load path.

The right aluminium accent remains one continuous laser-cut part and covers the sensor zone. The ferromagnetic steel behind it carries the 38 mm Hall window; aluminium is non-ferromagnetic, so the continuous cosmetic layer hides the development hardware without reintroducing steel into the sensing path.

## Cost-reduction pass

The initial concept was reduced to six steel sheet parts, two aluminium parts, ten small printed parts, one commodity grip, one spring, two bearings, and standard metric hardware. Decorative pivot caps, a separate machined spring cylinder, welded cosmetic covers, and a second aluminium chassis layer were removed. The two accents share the same stock and near-identical outline. No CNC billet part is required.

## Confidence language

- CAD VERIFIED: B-Rep geometry, alignment, envelope, or interference checked.
- ANALYTICALLY CHECKED: transparent statics/geometry calculation.
- MANUFACTURING ASSUMPTION: supplier tooling, tolerances, or process pending.
- PHYSICAL TEST REQUIRED: stiffness, wear, fatigue, clamp grip, magnetic response.
- SUPPLIER QUOTE REQUIRED: local cost/availability not confirmed.
