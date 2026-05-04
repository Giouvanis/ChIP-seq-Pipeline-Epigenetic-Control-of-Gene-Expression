import os
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, step_name):
    print(f"\n[INFO] Running: {step_name}")
    print(f"[CMD] {' '.join(cmd)}\n")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Step failed: {step_name}") from e


def fastqc(input_fastq, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["fastqc", str(input_fastq), "-o", str(output_dir)]
    run_command(cmd, "FastQC Quality Control")


def align_reads(fastq, index_base, sam_output, threads):
    cmd = [
        "bowtie2",
        "-x", index_base,
        "-U", str(fastq),
        "-S", str(sam_output),
        "-p", str(threads)
    ]
    run_command(cmd, "Alignment with Bowtie2")


def sam_to_bam(sam_file, bam_file):
    cmd = ["samtools", "view", "-bS", str(sam_file), "-o", str(bam_file)]
    run_command(cmd, "SAM → BAM conversion")


def sort_bam(bam_file, sorted_bam):
    cmd = ["samtools", "sort", str(bam_file), "-o", str(sorted_bam)]
    run_command(cmd, "Sorting BAM")


def index_bam(sorted_bam):
    cmd = ["samtools", "index", str(sorted_bam)]
    run_command(cmd, "Indexing BAM")


def filter_bam(sorted_bam, filtered_bam, mapq=30):
    cmd = [
        "samtools", "view",
        "-b", "-q", str(mapq),
        str(sorted_bam),
        "-o", str(filtered_bam)
    ]
    run_command(cmd, "Filtering BAM (MAPQ)")


def peak_calling(treatment_bam, control_bam, output_dir, genome_size="hs"):
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "macs3", "callpeak",
        "-t", str(treatment_bam),
        "-c", str(control_bam),
        "-f", "BAM",
        "-g", genome_size,
        "-n", "chipseq_output",
        "--outdir", str(output_dir)
    ]
    run_command(cmd, "Peak Calling (MACS3)")


def main():
    parser = argparse.ArgumentParser(description="ChIP-seq Analysis Pipeline")

    parser.add_argument("--chip", required=True, help="ChIP FASTQ file")
    parser.add_argument("--control", required=True, help="Control FASTQ file")
    parser.add_argument("--index", required=True, help="Bowtie2 genome index base")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--threads", type=int, default=4)

    args = parser.parse_args()

    output_dir = Path(args.output)
    qc_dir = output_dir / "qc"
    align_dir = output_dir / "alignment"
    peak_dir = output_dir / "peaks"

    align_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Quality Control
    fastqc(Path(args.chip), qc_dir)
    fastqc(Path(args.control), qc_dir)

    # Step 2: Alignment
    chip_sam = align_dir / "chip.sam"
    control_sam = align_dir / "control.sam"

    align_reads(args.chip, args.index, chip_sam, args.threads)
    align_reads(args.control, args.index, control_sam, args.threads)

    # Step 3: Convert + Sort + Index
    chip_bam = align_dir / "chip.bam"
    control_bam = align_dir / "control.bam"

    sam_to_bam(chip_sam, chip_bam)
    sam_to_bam(control_sam, control_bam)

    chip_sorted = align_dir / "chip_sorted.bam"
    control_sorted = align_dir / "control_sorted.bam"

    sort_bam(chip_bam, chip_sorted)
    sort_bam(control_bam, control_sorted)

    index_bam(chip_sorted)
    index_bam(control_sorted)

    # Step 4: Filtering
    chip_filtered = align_dir / "chip_filtered.bam"
    control_filtered = align_dir / "control_filtered.bam"

    filter_bam(chip_sorted, chip_filtered)
    filter_bam(control_sorted, control_filtered)

    # Step 5: Peak Calling
    peak_calling(chip_filtered, control_filtered, peak_dir)

    print("\n[SUCCESS] ChIP-seq pipeline completed.")


if __name__ == "__main__":
    main()