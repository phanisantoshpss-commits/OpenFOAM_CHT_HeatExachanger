#!/usr/bin/env python3

import argparse
import csv
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("ERROR: matplotlib is not installed.")
    print("Install it with:")
    print("    python3 -m pip install matplotlib")
    sys.exit(1)


parser = argparse.ArgumentParser(
    description="Sample OpenFOAM temperature at a coordinate and plot T vs time."
)

parser.add_argument(
    "--point",
    nargs=3,
    type=float,
    metavar=("X", "Y", "Z"),
    required=True,
    help="Probe coordinate: x y z"
)

parser.add_argument(
    "--region",
    required=True,
    help="OpenFOAM region, e.g. region1, region2, pipeWall"
)

parser.add_argument(
    "--field",
    default="T",
    help="Field to sample. Default: T"
)

parser.add_argument(
    "--interpolation",
    default="cellPoint",
    choices=["cell", "cellPoint"],
    help="Interpolation method. Default: cellPoint"
)

args = parser.parse_args()

x, y, z = args.point
region = args.region
field = args.field
interpolation = args.interpolation

case_dir = Path(__file__).resolve().parent
system_dir = case_dir / "system"

if not system_dir.exists():
    print(f"ERROR: system directory not found in:\n{case_dir}")
    sys.exit(1)

print("=" * 65)
print(" OpenFOAM temperature probe")
print("=" * 65)
print(f"Case          : {case_dir}")
print(f"Region        : {region}")
print(f"Field         : {field}")
print(f"Coordinate    : ({x}, {y}, {z})")
print(f"Interpolation : {interpolation}")
print("=" * 65)

time_dirs = []

for item in case_dir.iterdir():
    if not item.is_dir():
        continue

    try:
        time_value = float(item.name)
        time_dirs.append((time_value, item))
    except ValueError:
        pass

time_dirs.sort(key=lambda p: p[0])

if not time_dirs:
    print("ERROR: No numerical time directories found.")
    sys.exit(1)

print(f"\nFound {len(time_dirs)} time directories")
print(f"First time : {time_dirs[0][0]}")
print(f"Last time  : {time_dirs[-1][0]}")

existing_field_files = []

for time_value, time_dir in time_dirs:
    region_field = time_dir / region / field
    if region_field.exists():
        existing_field_files.append(region_field)

if not existing_field_files:
    print()
    print("ERROR:")
    print(f"Could not find {region}/{field} in any numerical time directory.")
    print()
    print("For example, expected something like:")
    print(f"    5/{region}/{field}")
    print()
    print("Check the region name.")
    sys.exit(1)

print(
    f"Found {field} in {len(existing_field_files)} "
    f"of {len(time_dirs)} time directories."
)

function_name = "pythonTemperatureProbe"
probe_dict = system_dir / "pythonTemperatureProbeDict"

dictionary_text = f"""
FoamFile
{{
    format      ascii;
    class       dictionary;
    location    "system";
    object      pythonTemperatureProbeDict;
}}

{function_name}
{{
    type                probes;
    libs                ("libsampling.so");

    region              {region};

    fields
    (
        {field}
    );

    probeLocations
    (
        ({x} {y} {z})
    );

    fixedLocations      true;
    interpolationScheme {interpolation};

    writeControl        timeStep;
    writeInterval       1;
}}
"""

probe_dict.write_text(dictionary_text)

print(f"\nCreated temporary dictionary:")
print(f"    {probe_dict}")

# OpenFOAM Foundation v12 writes region-specific function-object output as:
# postProcessing/<region>/<functionObjectName>/<time>/<field>
output_root = case_dir / "postProcessing" / region / function_name

if output_root.exists():
    shutil.rmtree(output_root)

command = [
    "foamPostProcess",
    "-dict",
    str(probe_dict),
    "-region",
    region,
    "-field",
    field
]

print("\nRunning:")
print(" ".join(command))
print()

try:
    subprocess.run(
        command,
        cwd=case_dir,
        check=True
    )

except FileNotFoundError:
    print()
    print("ERROR: foamPostProcess was not found.")
    print()
    print("Make sure OpenFOAM 12 is sourced first, for example:")
    print()
    print("    source /opt/openfoam12/etc/bashrc")
    print()
    sys.exit(1)

except subprocess.CalledProcessError:
    print()
    print("ERROR: foamPostProcess failed.")
    print()
    print("Check:")
    print("  1. region name")
    print("  2. coordinate lies inside the region")
    print("  3. T exists for that region")
    print("  4. OpenFOAM environment is sourced")
    sys.exit(1)

if not output_root.exists():
    print()
    print("ERROR: Probe output directory was not created:")
    print(output_root)
    sys.exit(1)

probe_files = []

for p in output_root.rglob(field):
    if p.is_file():
        probe_files.append(p)

if not probe_files:
    print()
    print(f"ERROR: Could not find probe output for field {field}.")
    print(f"Look inside:\n{output_root}")
    sys.exit(1)

temperature_data = {}

for probe_file in probe_files:
    with open(probe_file, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            try:
                time_value = float(parts[0])
                value_string = parts[1].strip("()")
                temperature = float(value_string)
                temperature_data[time_value] = temperature
            except ValueError:
                continue

if not temperature_data:
    print()
    print("ERROR: No valid probe data could be read.")
    print()
    print("The point may be outside the selected region.")
    sys.exit(1)

times = sorted(temperature_data.keys())
temperatures = [temperature_data[t] for t in times]

print("\n" + "=" * 45)
print(f"{'Time [s]':>15} {'Temperature [K]':>22}")
print("=" * 45)

for t, T in zip(times, temperatures):
    print(f"{t:15.6g} {T:22.6f}")

print("=" * 45)

point_tag = (
    f"x{x:g}_y{y:g}_z{z:g}"
    .replace("-", "m")
    .replace(".", "p")
)

csv_file = case_dir / f"temperature_vs_time_{region}_{point_tag}.csv"

with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Time [s]", "Temperature [K]"])

    for t, T in zip(times, temperatures):
        writer.writerow([t, T])

plt.figure(figsize=(9, 6))

plt.plot(
    times,
    temperatures,
    marker="o",
    markersize=3,
    linewidth=1.5
)

plt.xlabel("Time [s]")
plt.ylabel("Temperature [K]")
plt.title(
    f"Temperature vs Time\n"
    f"Region: {region}, Point: ({x:g}, {y:g}, {z:g})"
)
plt.grid(True, alpha=0.3)
plt.tight_layout()

png_file = case_dir / f"temperature_vs_time_{region}_{point_tag}.png"

plt.savefig(
    png_file,
    dpi=300,
    bbox_inches="tight"
)

print()
print("Results written to:")
print(f"CSV  : {csv_file}")
print(f"Plot : {png_file}")
print()

plt.show()

try:
    probe_dict.unlink()
except OSError:
    pass
