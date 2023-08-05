#!/usr/bin/env python3
import os, sys
import argparse
import pkg_resources
import textwrap
from bactinspector.commands import run_check_species, run_closest_match


def is_valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error('The file {} does not exist!'.format(arg))
    else:
        # File exists so return the filename
        return arg

def is_valid_dir(parser, arg):
    if not os.path.isdir(arg):
        parser.error('The directory {} does not exist!'.format(arg))
    else:
        # File exists so return the directory
        return arg

class Version(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(pkg_resources.require("BactInspectorMax")[0].version)
        sys.exit(0)

def parse_arguments():
    description = textwrap.dedent("""
    A module to determine the most probable species based on sequence in fasta files using refseq and Mash (https://mash.readthedocs.io/en/latest/index.html)
    It will count the species of the top ref seq mash matches and report most frequent.

    In order to use the module:
      • Specify an input directory and output directory (default is current directory)
      • Specify either a 
        • fasta file pattern with -f (e.g "*.fas") or 
        • mash sketch file pattern with -m (e.g "*.msh") if you have already sketched the fasta files
      • By default the top 10 matches will be used. Change this with -n
      • Speed things up by changing the number of parallel processes to match the cores on your computer using -p
      • If mash is not in your PATH specify the directory containing the mash executable with -mp
    """)
    # parse all arguments
    parser = argparse.ArgumentParser(description=description,formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.register('action', 'version', Version)
    parser.add_argument('-v', '--version', action='version', nargs = 0, help='print out software version')

    subparsers = parser.add_subparsers(
        help='The following commands are available. Type bactinspector <COMMAND> -h for more help on a specific commands',
        dest='command'
    )

    subparsers.required = True

    # check species sub command
    check_species_command = subparsers.add_parser('check_species',
        help='Check the most frequent matches to a species in refseq'
    )


    check_species_command.add_argument('-i', '--input_dir', help='path to input_directory', type=lambda x: is_valid_dir(parser, x), default = '.')
    check_species_command.add_argument('-o', '--output_dir', help='path to output_directory', type=lambda x: is_valid_dir(parser, x),  default = '.')
    check_species_command.add_argument('-p', '--parallel_processes', help='number of processes to run in parallel', default = 1, type = int)
    check_species_command.add_argument('-n', '--num_best_matches', help='number of best matches to return', default = 10, type = int)
    check_species_command.add_argument('-d', '--distance_cutoff', help='mash distance cutoff (default 0.05)', default = 0.05, type = float)
    check_species_command.add_argument('-s', '--stdout_summary', help='output a summary of the result to STDOUT', action='store_true')

    check_species_command.add_argument('-mp', '--mash_path', help='path to the mash executable. If not provided it is assumed mash is in the PATH')

    filetype_extension = check_species_command.add_mutually_exclusive_group(required = True)
    filetype_extension.add_argument('-f', '--fasta_file_pattern', help='pattern to match fasta files e.g "*.fas"')
    filetype_extension.add_argument('-fq', '--fastq_file_pattern', help='pattern to match fastq files e.g "*.fastq.gz"')
    filetype_extension.add_argument('-m', '--mash_sketch_file_pattern', help='pattern to match mash sketch files e.g "*.msh"')


    # closest match sub command
    closest_match_command = subparsers.add_parser('closest_match',
        help='Report the closest matches to a set of sequences'
    )


    closest_match_command.add_argument('-i', '--input_dir', help='path to input_directory', type=lambda x: is_valid_dir(parser, x), default = '.')
    closest_match_command.add_argument('-o', '--output_dir', help='path to output_directory', type=lambda x: is_valid_dir(parser, x),  default = '.')
    closest_match_command.add_argument('-p', '--parallel_processes', help='number of processes to run in parallel', default = 1, type = int)
    closest_match_command.add_argument('-r', '--ref_and_rep_only', help='only include reference and representative sequences', action='store_true')

    closest_match_command.add_argument('-mp', '--mash_path', help='path to the mash executable. If not provided it is assumed mash is in the PATH')

    filetype_extension = closest_match_command.add_mutually_exclusive_group(required = True)
    filetype_extension.add_argument('-f', '--fasta_file_pattern', help='pattern to match fasta files e.g "*.fas"')
    filetype_extension.add_argument('-fq', '--fastq_file_pattern', help='pattern to match fastq files e.g "*.fastq.gz"')
    filetype_extension.add_argument('-m', '--mash_sketch_file_pattern', help='pattern to match mash sketch files e.g "*.msh"')


    args = parser.parse_args()
    return args


def choose_command(args):
    if args.command == 'check_species':
        run_check_species(args)
    elif args.command == 'closest_match':
        run_closest_match(args)

def main():
    args = parse_arguments()
    choose_command(args)

if __name__ == "__main__":
    main()





