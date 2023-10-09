#!/usr/bin/env python
#

# Coverage checking script
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd

def generate_coverage_graph(covstats, basecov, outdir):

    # Read covstats file
    headers = [
        "ID",
        "Avg_fold",
        "Length",
        "Ref_GC",
        "Covered_percent",
        "Covered_bases",
        "Plus_reads",
        "Minus_reads",
        "Read_GC",
        "Median_fold",
        "Std_Dev"
    ]
    df = pd.read_csv(covstats, sep='\t', comment='#', names=headers)

    # Separating data from covstats
    finished = df[df['Avg_fold'] >= 400]
    complete = df[df['Avg_fold'] >= 100]
    complete = complete[complete['Avg_fold'] <= 400]
    check = df[df['Avg_fold'] >= 50]
    check = check[check['Avg_fold'] <= 100]

    if not len(check) == 0:
        print("ERROR, manual curation required")
    elif len(finished) > 1:
        print("ERROR, >1 finished genome")
    elif len(complete) > 1:
        print("ERROR, >1 complete genome")
    elif len(complete) + len(finished) > 1:
        print("ERROR, A finished and complete genome are present")
    elif len(finished) == 1:
        contig = finished['ID'][0]
        finished = True
    elif len(complete) == 1:
        contig = complete['ID'][0]
        finished = False

    # Checking what we're working with
    if finished:
        print("Genome has > 400 X avg read depth")
        cutoff = 400
    else:
        print("Genome has 100-400 X avg read depth")
        cutoff = 100

    # Read data from the basecov file
    headers = ["ID", "Pos", "Coverage"]
    df = pd.read_csv(basecov, sep='\t', comment='#', names=headers)

    # Separating data from basecov
    coverage = df[df['ID'] == contig]

    # Plot basecoverage
    x_values = coverage['Pos']
    y_values = coverage['Coverage']

    # Check coverage
    below_cutoff_count = sum(1 for y in y_values if y < cutoff)
    if any(y < cutoff for y in y_values):
        print(f"Warning: {below_cutoff_count} coverage values have dipped below {cutoff}")

    # Create a plot for coverage data
    plt.figure(figsize=(15, 8))
    plt.plot(x_values, 
            y_values, 
            marker = ',', 
            markersize = 0.1,
            linestyle = '-', 
            color='b')
    plt.title(f"Per base coverage for {contig}")
    plt.xlabel("Position")
    plt.ylabel("Coverage")
    plt.grid(True)

    # Control line
    plt.axhline(y=400, color='red', linestyle=':')
    plt.axhline(y=100, color='red', linestyle='-')

    # Save the plot as an image file (e.g., PNG)
    outfile = os.path.join(outdir, f"{contig}.png")
    plt.savefig(outfile, dpi = 300)

# Directories
qc_phage = '/assemble/output/mapping_QC_to_phage'
qc_host = '/assemble/output/mapping_QC_to_host'

# Running script
if os.path.exists(qc_phage):
    for file in os.listdir(qc_phage):
        print(file)
        # Setting function inputs
        dirpath = os.path.join(qc_phage, file)
        cov = os.path.join(dirpath, "covstats.tsv")
        base = os.path.join(dirpath, "basecov.tsv")

        # Running graph
        try:
            generate_coverage_graph(cov, base, dirpath)
        except Exception as e:
            print(e)
else:
    print("error")