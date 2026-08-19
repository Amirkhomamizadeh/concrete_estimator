"""
Concrete Slab Estimator
------------------------
A simple command-line tool that estimates the concrete needed for a
rectangular slab: total volume, number of bags, and a rough material cost.

Built by a former construction worker learning Python. 🏗️
Run it with:  python concrete_estimator.py
"""

import math


# --------------------------------------------------------------------------
# CONSTANTS — the "known facts" of the concrete world.
# We put them up here (in CAPS by convention) so they're easy to find/change.
# --------------------------------------------------------------------------
CUBIC_FEET_PER_CUBIC_YARD = 27          # 27 cu ft = 1 cu yd (concrete is ordered by the yard)
WASTE_FACTOR = 1.10                     # add 10% for spillage / uneven ground

# How much each bag of concrete mix fills, in cubic feet (standard yields):
BAG_YIELDS_CU_FT = {
    40: 0.30,   # a 40 lb bag fills ~0.30 cu ft
    60: 0.45,   # a 60 lb bag fills ~0.45 cu ft
    80: 0.60,   # an 80 lb bag fills ~0.60 cu ft
}


# --------------------------------------------------------------------------
# HELPER FUNCTIONS — each one does ONE small job. This is how real code is
# organized: small, named, reusable pieces instead of one giant blob.
# --------------------------------------------------------------------------
def get_positive_number(prompt):
    """Ask the user for a number, and keep asking until they give a valid,
    positive one. This is 'input validation' — it stops the program from
    crashing when someone fat-fingers a letter instead of a number."""
    while True:
        raw = input(prompt)
        try:
            value = float(raw)          # try to turn their text into a number
        except ValueError:
            print("  ⚠️  Please type a number (like 12 or 4.5).")
            continue                    # go back to the top of the loop and re-ask
        if value <= 0:
            print("  ⚠️  Please enter a number greater than zero.")
            continue
        return value                    # good input — hand it back and exit the loop


def slab_volume_cubic_feet(length_ft, width_ft, thickness_inches):
    """Volume of the slab in cubic feet.
    Thickness comes in INCHES (that's how slabs are spec'd), but length and
    width are in FEET, so we convert thickness to feet first (12 in = 1 ft)."""
    thickness_ft = thickness_inches / 12
    return length_ft * width_ft * thickness_ft


def bags_needed(cubic_feet, bag_size_lb):
    """How many bags of a given size to fill this volume.
    We round UP (math.ceil) because you can't buy 0.4 of a bag."""
    yield_per_bag = BAG_YIELDS_CU_FT[bag_size_lb]
    return math.ceil(cubic_feet / yield_per_bag)


# --------------------------------------------------------------------------
# MAIN PROGRAM — this is the "recipe" that uses the helpers above in order.
# --------------------------------------------------------------------------
def main():
    print("=" * 46)
    print("  🏗️  CONCRETE SLAB ESTIMATOR")
    print("=" * 46)
    print("Enter your slab dimensions:\n")

    # 1) Collect the inputs
    length = get_positive_number("Length (feet):     ")
    width = get_positive_number("Width (feet):      ")
    thickness = get_positive_number("Thickness (inches): ")

    # 2) Do the math
    raw_volume = slab_volume_cubic_feet(length, width, thickness)
    volume = raw_volume * WASTE_FACTOR                       # add the waste buffer
    cubic_yards = volume / CUBIC_FEET_PER_CUBIC_YARD

    # 3) Show the material results
    print("\n" + "=" * 46)
    print("  RESULTS  (includes 10% waste)")
    print("=" * 46)
    print(f"Volume needed : {volume:.1f} cubic feet")
    print(f"              : {cubic_yards:.2f} cubic yards")
    print("\nIf buying bags instead of ready-mix:")
    for size in (40, 60, 80):
        print(f"  {size} lb bags : {bags_needed(volume, size)} bags")

    # 4) Optional cost estimate
    print()
    price = get_positive_number("Price per cubic yard ($): ")
    cost = cubic_yards * price
    print(f"\n💰 Estimated concrete cost: ${cost:,.2f}")
    print("   (materials only — labour & delivery not included)")
    print("=" * 46)


# --------------------------------------------------------------------------
# This line means: "only run main() if this file was run directly."
# It's a standard Python pattern you'll see everywhere. More on it below.
# --------------------------------------------------------------------------
if __name__ == "__main__":
    main()
