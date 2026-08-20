"""
Concrete Estimator  (v2)
------------------------
Estimates concrete for five common structural elements — slab, wall, column,
column cap, and stairs. For each one it works out the pour volume, adds a waste
factor, recommends a concrete strength (MPa) for that element, and gives a
market-range cost estimate with ordering advice.

v1 handled a single slab with a price you typed in. v2 knows the geometry of
different elements, suggests the right strength, and estimates cost from real
2026 ballpark ready-mix ranges.

Built by a former construction worker learning Python. 🏗️
Run it with:  python concrete_estimator.py
"""

import math


# --------------------------------------------------------------------------
# CONSTANTS / DOMAIN DATA
# --------------------------------------------------------------------------
CUBIC_FEET_PER_CUBIC_YARD = 27
WASTE_FACTOR = 1.10                     # +10% for spillage / uneven ground

# The elements this tool can estimate, in menu order.
ELEMENTS = ["slab", "wall", "column", "column cap", "stairs"]

# Typical concrete strength (MPa) for each element — Ontario, freeze-thaw aware.
RECOMMENDED_MPA = {
    "slab": 25,
    "wall": 25,
    "column": 30,
    "column cap": 30,
    "stairs": 32,      # exterior, exposed to salt & freeze-thaw
}

# Ballpark ready-mix price ranges (CAD per cubic yard, delivered, 2026).
# Higher strength costs more. These are STARTING estimates — always confirm
# with a local supplier. Stored as (low, high) tuples.
PRICE_PER_YARD = {
    20: (170, 200),
    25: (185, 215),
    30: (200, 235),
    32: (210, 245),
    35: (225, 260),
}


# --------------------------------------------------------------------------
# INPUT HELPER
# --------------------------------------------------------------------------
def get_positive_number(prompt):
    """Ask for a number, re-asking until it's a valid positive one."""
    while True:
        raw = input(prompt)
        try:
            value = float(raw)
        except ValueError:
            print("  ⚠️  Please type a number.")
            continue
        if value <= 0:
            print("  ⚠️  Please enter a number greater than zero.")
            continue
        return value


# --------------------------------------------------------------------------
# GEOMETRY — one function per element. Each returns raw volume in CUBIC FEET.
# Dimensions follow how each element is actually spec'd on drawings:
#   feet for the big spans, inches for thicknesses & column sizes.
# --------------------------------------------------------------------------
def slab_volume(length_ft, width_ft, thickness_in):
    return length_ft * width_ft * (thickness_in / 12)


def wall_volume(length_ft, height_ft, thickness_in):
    # a wall is really just a vertical slab
    return length_ft * height_ft * (thickness_in / 12)


def column_volume(width_in, depth_in, height_ft):
    # rectangular column: cross-section in inches, height in feet
    return (width_in / 12) * (depth_in / 12) * height_ft


def column_cap_volume(length_in, width_in, depth_in):
    # a rectangular cap block sitting on the column (all inches)
    return (length_in / 12) * (width_in / 12) * (depth_in / 12)


def stairs_volume(num_steps, riser_in, run_in, width_ft, waist_in):
    """Concrete stairs = the triangular steps ON TOP of a sloped 'waist' slab.
    We add the two pieces together — this is how a real takeoff is done."""
    step_vol = 0.5 * (riser_in / 12) * (run_in / 12) * width_ft * num_steps

    total_rise_ft = num_steps * (riser_in / 12)
    total_run_ft = num_steps * (run_in / 12)
    slope_length_ft = math.sqrt(total_rise_ft ** 2 + total_run_ft ** 2)
    waist_vol = (waist_in / 12) * width_ft * slope_length_ft

    return step_vol + waist_vol


# --------------------------------------------------------------------------
# MENUS
# --------------------------------------------------------------------------
def choose_element():
    """Show the element menu and return the chosen element's name."""
    print("What are you pouring?")
    for i, name in enumerate(ELEMENTS, start=1):   # enumerate gives us 1, "slab" etc.
        print(f"  {i}. {name}")
    while True:
        pick = input("Choose 1-5: ").strip()
        if pick in ("1", "2", "3", "4", "5"):
            return ELEMENTS[int(pick) - 1]         # menu #1 -> list position 0
        print("  ⚠️  Please enter a number from 1 to 5.")


def measure(element):
    """Ask only for the dimensions THIS element needs, return raw cubic feet."""
    print(f"\nEnter dimensions for the {element}:")
    if element == "slab":
        L = get_positive_number("  Length (feet): ")
        W = get_positive_number("  Width (feet): ")
        T = get_positive_number("  Thickness (inches): ")
        return slab_volume(L, W, T)
    elif element == "wall":
        L = get_positive_number("  Length (feet): ")
        H = get_positive_number("  Height (feet): ")
        T = get_positive_number("  Thickness (inches): ")
        return wall_volume(L, H, T)
    elif element == "column":
        w = get_positive_number("  Column width (inches): ")
        d = get_positive_number("  Column depth (inches): ")
        H = get_positive_number("  Column height (feet): ")
        return column_volume(w, d, H)
    elif element == "column cap":
        L = get_positive_number("  Cap length (inches): ")
        W = get_positive_number("  Cap width (inches): ")
        D = get_positive_number("  Cap depth / thickness (inches): ")
        return column_cap_volume(L, W, D)
    elif element == "stairs":
        n = get_positive_number("  Number of steps: ")
        r = get_positive_number("  Riser height (inches, ~7): ")
        run = get_positive_number("  Tread run (inches, ~11): ")
        W = get_positive_number("  Stair width (feet): ")
        waist = get_positive_number("  Waist slab thickness (inches, ~6): ")
        return stairs_volume(n, r, run, W, waist)


def choose_strength(recommended):
    """Show standard strengths (flagging the recommended one) and return the pick."""
    print(f"\nConcrete strength (MPa).  Typical for this element: {recommended} MPa")
    for mpa in sorted(PRICE_PER_YARD):
        tag = "   ← recommended" if mpa == recommended else ""
        print(f"  {mpa} MPa{tag}")
    while True:
        raw = input("Enter the MPa you'll use: ").strip()
        try:
            mpa = int(raw)
        except ValueError:
            print("  ⚠️  Enter a whole number like 25.")
            continue
        if mpa in PRICE_PER_YARD:
            return mpa
        print(f"  ⚠️  Pick a standard strength: {sorted(PRICE_PER_YARD)}")


# --------------------------------------------------------------------------
# ADVICE
# --------------------------------------------------------------------------
def strength_advice(element, mpa, recommended):
    if mpa < recommended:
        return f"⚠️  {mpa} MPa is BELOW the {recommended} MPa usually spec'd for a {element}. Double-check the drawings."
    elif mpa > recommended:
        return f"ℹ️  {mpa} MPa is stronger than the usual {recommended} MPa for a {element} — fine, but you'll pay a premium."
    return f"✅ {mpa} MPa matches the typical spec for a {element}."


def round_up_to_half_yard(cubic_yards):
    """Plants batch in half-yard increments, and you always round UP —
    ordering short means a cold joint or waiting on a second truck."""
    return math.ceil(cubic_yards * 2) / 2


# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------
def main():
    print("=" * 52)
    print("  🏗️  CONCRETE ESTIMATOR  (v2)")
    print("=" * 52)

    element = choose_element()
    raw_cf = measure(element)

    volume_cf = raw_cf * WASTE_FACTOR
    cubic_yards = volume_cf / CUBIC_FEET_PER_CUBIC_YARD
    order_yards = round_up_to_half_yard(cubic_yards)

    recommended = RECOMMENDED_MPA[element]
    mpa = choose_strength(recommended)

    low_rate, high_rate = PRICE_PER_YARD[mpa]
    cost_low = order_yards * low_rate
    cost_high = order_yards * high_rate

    # -------- Results --------
    print("\n" + "=" * 52)
    print(f"  RESULTS — {element.upper()}  (includes 10% waste)")
    print("=" * 52)
    print(f"Volume needed : {volume_cf:.1f} cubic feet")
    print(f"              : {cubic_yards:.2f} cubic yards")
    print(f"Order (rounded up to half-yard): {order_yards} cubic yards\n")

    print(strength_advice(element, mpa, recommended))

    if element in ("slab", "stairs"):
        print("ℹ️  Exterior pours in freeze-thaw areas should be air-entrained (standard at 30 MPa+).")
    if order_yards < 3:
        print("⚠️  Under ~3 yd — expect a short-load fee ($40–$150). Bundling pours can avoid it.")

    print("\n" + "-" * 52)
    print(f"Strength      : {mpa} MPa")
    print(f"Estimated cost: ${cost_low:,.0f} – ${cost_high:,.0f} CAD")
    print("   (materials + delivery, ballpark — get same-spec quotes from 2–3 local suppliers)")
    print("=" * 52)


if __name__ == "__main__":
    main()
