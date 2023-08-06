import argparse
from .main import main


def cli(args=None):
    parser = argparse.ArgumentParser(description='Test file')

    parser.add_argument('configuration_file', action='store', type=str,
                        help='The JSON file defining the Dtest, Spark, and tests configurations')

    args = parser.parse_args()

    main(config_file=args.configuration_file)
