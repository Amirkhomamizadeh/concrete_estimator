# 🏗️ Concrete Estimator

A command-line tool that estimates concrete for five common structural elements — **slab, wall, column, column cap, and stairs**. For each one it calculates the pour volume, adds a waste factor, recommends a concrete strength, and gives a market-range cost estimate with ordering advice.

Built while learning Python, drawing on my background in construction.

---

## What it does

- 🧱 Handles **5 element types**, each with its own real geometry (stairs = triangular steps on a sloped waist slab, columns by cross-section, etc.)
- 📐 Calculates volume in cubic feet and cubic yards, plus a **10% waste factor**
- 🎯 Recommends a **concrete strength (MPa)** for the element and flags your choice if it's under-spec
- 💰 Estimates cost as a **market range** (CAD, 2026 ballpark) and rounds the order up to the next half-yard
- 🚩 Warns about **short-load fees** and **freeze-thaw / air-entrainment** on exterior pours

---

## Example

```
====================================================
  🏗️  CONCRETE ESTIMATOR  (v2)
====================================================
What are you pouring?
  1. slab
  2. wall
  3. column
  4. column cap
  5. stairs
Choose 1-5: 5

Enter dimensions for the stairs:
  Number of steps: 10
  Riser height (inches, ~7): 7
  Tread run (inches, ~11): 11
  Stair width (feet): 4
  Waist slab thickness (inches, ~6): 6

Concrete strength (MPa).  Typical for this element: 32 MPa
  ...
Enter the MPa you'll use: 25

====================================================
  RESULTS — STAIRS  (includes 10% waste)
====================================================
Volume needed : 35.7 cubic feet
              : 1.32 cubic yards
Order (rounded up to half-yard): 1.5 cubic yards

⚠️  25 MPa is BELOW the 32 MPa usually spec'd for a stairs. Double-check the drawings.
ℹ️  Exterior pours in freeze-thaw areas should be air-entrained (standard at 30 MPa+).
⚠️  Under ~3 yd — expect a short-load fee ($40–$150). Bundling pours can avoid it.

----------------------------------------------------
Strength      : 25 MPa
Estimated cost: $278 – $322 CAD
====================================================
```

---

## How to run it

You'll need **Python 3**. Then:

```bash
python concrete_estimator.py
```

Pick an element, enter the dimensions, choose a strength, and read your estimate.

---

## How it works

- **One geometry function per element** — `slab_volume`, `wall_volume`, `column_volume`, `column_cap_volume`, `stairs_volume` — each returning volume in cubic feet
- **Menu-driven input** — the tool asks only for the dimensions the chosen element actually needs
- **Dictionary lookups** for recommended strength and price ranges, keeping the domain data separate from the logic
- **Input validation** so bad entries never crash the program

---

## Version history

- **v2** — Added multiple element types (slab, wall, column, column cap, stairs) with real geometry, concrete strength (MPa) selection with spec advice, and market-range cost estimates with ordering warnings.
- **v1** — Single rectangular slab: volume, bag counts, and a basic cost from a price you entered.

---

## Roadmap

- [ ] 🌐 Web app version (Streamlit) with a clickable live demo
- [ ] 📏 Metric units (metres, cubic metres)
- [ ] 🧱 Round columns (sonotube) and tapered caps
- [ ] 💾 Save estimates to a file

---

## About

Built by a former construction worker learning to code — turning hands-on trade knowledge into software, one version at a time. 🔨→💻
