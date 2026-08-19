# 🏗️ Concrete Slab Estimator

A simple command-line tool that estimates the concrete needed for a rectangular slab — total volume, number of bags, and a rough material cost.

Built while learning Python, drawing on my background in construction. The goal: turn a real job-site calculation I already know by hand into a clean, reusable program.

---

## What it does

Give it the dimensions of a slab and it tells you:

- 📐 Total volume in **cubic feet** and **cubic yards**
- ➕ A built-in **10% waste factor** (spillage, uneven ground)
- 🛍️ How many **40 / 60 / 80 lb bags** you'd need if buying bagged mix
- 💰 An estimated **material cost** from a price per cubic yard

---

## Example

```
==============================================
  🏗️  CONCRETE SLAB ESTIMATOR
==============================================
Enter your slab dimensions:

Length (feet):     10
Width (feet):      10
Thickness (inches): 4

==============================================
  RESULTS  (includes 10% waste)
==============================================
Volume needed : 36.7 cubic feet
              : 1.36 cubic yards

If buying bags instead of ready-mix:
  40 lb bags : 123 bags
  60 lb bags : 82 bags
  80 lb bags : 62 bags

Price per cubic yard ($): 150

💰 Estimated concrete cost: $203.70
   (materials only — labour & delivery not included)
==============================================
```

---

## How to run it

You'll need **Python 3** installed. Then:

```bash
python concrete_estimator.py
```

Answer the prompts and read your estimate. That's it.

---

## How it works

The code is organized into small, single-purpose functions:

- `get_positive_number()` — asks for input and **won't crash** on bad entries (input validation)
- `slab_volume_cubic_feet()` — the core volume math (converts inches → feet)
- `bags_needed()` — rounds up to whole bags, since you can't buy half a bag
- `main()` — runs the whole thing in order: collect → calculate → display

Domain facts (like "27 cubic feet = 1 cubic yard" and bag yields) are stored as **constants** at the top, so they're easy to find and update.

---

## Roadmap

- [ ] 🌐 Web app version (Streamlit) with a clickable live demo
- [ ] 📏 Metric units (metres / millimetres, cubic metres)
- [ ] 🧱 More materials: rebar, gravel base, forms & lumber
- [ ] 💾 Save estimates to a file

---

## About

Built by a former construction worker learning to code. First of several projects — turning hands-on trade knowledge into software. 🔨→💻
