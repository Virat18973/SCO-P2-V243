# Hospet Sinter Burden Control — v40.0

Streamlit dashboard + Colab backend for the sinter burden cost optimisation (PuLP / CBC linear programme).

## Files (deploy these together in one folder)

| File | Purpose |
|---|---|
| `app.py` | Streamlit dashboard |
| `optimizer.py` | Backend model (the dashboard and the notebook run the same code) |
| `master_chemistry_uploader.py` | Thin wrapper around the backend Excel loader |
| `Master_Chemistry_Input_Template.xlsx` | New master workbook template (with an Instructions sheet) |
| `requirements.txt` | `streamlit`, `pandas`, `numpy`, `PuLP>=2.8,<4`, `openpyxl` |
| `Sinter_Burden_Optimizer_v40_backend.ipynb` | Colab backend — ONE code cell (model + widgets UI) |

Run locally: `pip install -r requirements.txt` then `streamlit run app.py`.

## What the model does now

1. **Return sinter is a share of the charged mix** (charged mix = fresh burden + BFR poured).
   * **BF Returns (BFR)**: 17 % of the charged mix (editable 17–20 %). Chemistry-only: adds chemistry and sinter mass, **not in the burden, Rs 0**.
   * **IOL Fines**: 5–8 % of the charged mix (default 8 %). A physical burden material — in the burden and in the cost.
   * Total return sinter is shown against the usual 20–25 % range (warning only).
   * BFR poured = b/(1−b) × fresh burden. Net sinter (1,000 kg) is made by the fresh materials; the BFR-derived sinter is added on top and chemistry is measured on the gross sinter.
   * If BFR is marked unavailable, or its stock cannot cover the planning horizon, its chemistry share is reduced automatically.
2. **Iron ores follow the RM stock ratio.** Tech Max no longer drives ore usage and the old 3 % ore floor is gone. Works with 2, 3 or 4 ores. The ratio is a *soft* target — quality limits always win.
   * **Mill Scale is untouched**: always 5–15 % of the burden, outside the ratio.
   * **Inventory weight** dial (Inputs → Inventory Rules): 1 = follow the stock ratio as closely as chemistry allows, 0 = pure cost. The dashboard shows the *price of following the stock ratio* against the pure-cost recipe.
3. **Recycle materials keep fixed rates** (Tech Min = Tech Max).
4. **Flux is chosen by chemistry requirement and cost.** No hard-coded flux shares, no "relaxed flux" tier. Optional Tech Min/Max still apply to flux (default template: quicklime floor 40 / cap 65 kg/t; dolomite minimum is not forced). A 25 % total-flux guard remains (editable).
5. **Coke (KSL / Local) usage follows dry stock × quality index (FC × CV).** The 40–60 % split is gone. Total coke still comes from the heat balance / FeO logic. CV and FC are entered per fuel on Inputs → Coke & Fuel and are used by the solver.
6. **Planning horizon**: production tonnes + days. RM stock over the horizon is a hard cap on every material (converted to dry with moisture, or entered as dry).
7. **Objective order**: hard quality limits → FeO closeness → inventory ratio → cost. The ore "suitability" stage was removed.
8. **Quality-relaxed status**: when ores or IOL are short, SiO₂ may widen to 6.2 %; the run is labelled *Relaxed* (not *Optimal*).
9. **Productivity** now responds to the recipe: net sinter t/h = feed × 1000 / charged mix; productivity = net sinter / strand area, reduced by the fines loss.
10. **Scenario analysis** runs at the same production as the main run; the BFR knock-out now has an effect.
11. **Inventory Usage page**: target vs actual share, tonnes used, % of stock used and days of cover per material.

## Master workbook — do the Tech Min / Tech Max columns still matter?

Only for two things, and both are **optional** (blank = no limit):

* **Flux limits** you want to keep (e.g. quicklime floor 40 / cap 65 kg/t).
* **Recycle fixed rates** (Tech Min = Tech Max, e.g. 10 kg/t).

Iron ores, coke, IOL and BFR **ignore** these columns (their use is driven by stock). Old masters that still carry ore Tech Max values load fine; those values are ignored for ores unless you tick "Also apply Tech Min/Max to iron ores and coke". Sheet names do not matter; columns are matched by header.

## Known limitations / to confirm with the plant

* Template prices and stocks are example values — replace them with current data.
* Productivity: strand area default (50 m²) is a **placeholder**; the feed-rate basis (charged mix, dry) must be confirmed. Fines % is 0 in the template.
* The FeO / heat-balance coefficients are the provisional v39 model, unchanged. Calibrate against plant coke / FeO history.
* The coke quality index (FC × CV) is a modelling choice for "quality"; identical coke properties give a 50/50 split at equal stock.
* At inventory weight 1.0 the recipe can cost noticeably more than the pure-cost recipe; the dashboard shows the exact premium. Use the dial to trade stock balance against cost.
* Back-test against real plant days before using the numbers for decisions.
