import os
from argparse import ArgumentParser
import gzip


def run():
    parser = ArgumentParser(description='Glove interpretibility')

    parser.add_argument("--conceptnet_path", type=str, required=True)
    args = parser.parse_args()

    with gzip.open(args.conceptnet_path, mode="r") as f:
        with gzip.open("data/conceptnet-assertions-5.7.0_reduced.csv.gz", mode="w") as g:
            for line in f:
                if line.decode("utf-8").split("\t")[1] in ["/r/RelatedTo", "/r/Synonym", "/r/FormOf", "/r/DerivedFrom"]:
                    g.write(line)


if __name__ == '__main__':
    run()
