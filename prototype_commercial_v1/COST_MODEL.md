# Cost model

All local fabrication values are planning allowances until replaced by Tunisian supplier quotations. `reports/cost_model.csv` carries the status of every line and unit-cost scenarios for 1/5/10/25/50 units.

|Retail TND|35% direct BOM|40% direct BOM|45% direct BOM|
|---:|---:|---:|---:|
|150|52.50|60.00|67.50|
|175|61.25|70.00|78.75|
|200|70.00|80.00|90.00|
|250|87.50|100.00|112.50|
|275|96.25|110.00|123.75|
|300|105.00|120.00|135.00|

Quantity-25 planning direct BOM excluding assembly/packaging: **87.8 TND**. Full planning allowance including those two categories: **100.8 TND**. BOM is not profit; labor, packaging, failures, warranty, marketing, payment fees, tax and overhead remain separate business costs.

The five largest planning pressures are electronics, grip, fasteners, laser cutting, and assembly/powder coating. The cost-down pass retained one folded base, removed CNC billet parts, reduced aluminium to two flat accents, standardized commodity bearings, and shared MID/PRO architecture.
