from semcat import SemCat
from conceptnet import ConceptNet
import re
import json
from argparse import ArgumentParser
import os
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


language = lambda inp, lang: re.match(f"/c/{lang}/[A-Za-z0-9_\-/]*", inp)
extract_token = lambda inp: inp.split("/")[3]
lang_test = lambda src, trg, start, end: (language(start, src) and language(end, trg)) or (language(end, src) and language(start, trg))


def generate_source_language_categories(semcat, conceptnet_path, lang_source):
    categories = {concept: set([concept]) for concept in semcat.vocab.keys()}
    root_terms = {concept: set([concept]) for concept in semcat.vocab.keys()}
    category_keys = list(semcat.vocab.keys())

    logging.info("Gathering related and similar terms...")
    i = 0
    with ConceptNet(conceptnet_path) as f:
        for relation, start, end, weight in f:
            if i % 1000000 == 0:
                logging.info(f"{i} lines processed...")
            if language(start, lang_source) and language(end, lang_source) and weight >= 1.0:
                start_token = extract_token(start)
                end_token = extract_token(end)
                if relation == "/r/RelatedTo" or relation == "/r/Synonym":
                    if start_token in category_keys:
                        categories[start_token].add(end_token)
                    if end_token in category_keys:
                        categories[end_token].add(start_token)

                if relation == "/r/FormOf" or relation == "/r/DerivedFrom":
                    if start_token in category_keys:
                        categories[start_token].add(end_token)
                        root_terms[start_token].add(end_token)
            i += 1

    # i = 0
    # logging.info("Resolving root terms...")
    # with ConceptNet(conceptnet_path) as f:
    #     for relation, start, end, weight in f:
    #         if i % 1000000 == 0:
    #             logging.info(f"{i} lines processed...")
    #         if language(start, lang_source) and language(end, lang_source) and weight >= 1.0:
    #             start_token = extract_token(start)
    #             end_token = extract_token(end)
    #             if relation == "/r/RelatedTo" or relation == "/r/Synonym":
    #                 for key in root_terms:
    #                     for item in list(root_terms[key]):
    #                         if start_token == item:
    #                             categories[key].add(end_token)
    #                         if end_token == item:
    #                             categories[key].add(start_token)
    #         i += 1
    return categories


def generate_target_language_categories(semcat, conceptnet_path, lang_source, lang_target, source_categories):
    categories = {concept: set() for concept in semcat.vocab.keys()}
    logging.info("Generating target language categories")
    i = 0

    with ConceptNet(conceptnet_path) as f:
        for relation, start, end, weight in f:
            if i % 1000000 == 0:
                logging.info(f"{i} lines processed...")
            if lang_test(lang_source, lang_target, start, end):
                if relation == "/r/RelatedTo" or relation == "/r/Synonym":
                    start_token = extract_token(start)
                    end_token = extract_token(end)
                    for key in source_categories:
                        for item in list(source_categories[key]):
                            if start_token == item:
                                categories[key].add(end_token)
                            if end_token == item:
                                categories[key].add(start_token)
            i += 1
    return categories


def run():
    parser = ArgumentParser(description='Glove interpretibility')

    parser.add_argument("--semcat_path", type=str, required=True)
    parser.add_argument("--conceptnet_path", type=str, required=True)
    # --source_categories="categories/semcat_en-en.json"
    parser.add_argument("--source_categories", type=str, required=False, default=None)
    parser.add_argument("--source_language", type=str, required=False, default="en")
    parser.add_argument("--intermediate_language", type=str, required=False, default="en")
    parser.add_argument("--target_language", type=str, required=False, default="en")
    args = parser.parse_args()

    lang_source = args.source_language
    lang_target = args.target_language
    intermediate_language = args.intermediate_language
    source_categories = args.source_categories
    semcat_path = args.semcat_path  # "data/semcat/"
    conceptnet_path = args.conceptnet_path  # "data/conceptnet-assertions-5.7.0.csv.gz"

    if not os.path.exists("categories/"):
        os.mkdir("categories")

    semcat = SemCat(semcat_path)
    if source_categories is None:
        source_categories = generate_source_language_categories(semcat, conceptnet_path, lang_source)
        fd = open(f"categories/semcat_{lang_source}-{lang_source}.json", mode="w", encoding="utf8")
        for key in source_categories:
            source_categories[key] = list(source_categories[key])
        json.dump(source_categories, fd, indent=2)
        fd.close()
    else:
        fd = open(source_categories, mode="r", encoding="utf8")
        source_categories = json.load(fd)
        fd.close()

    target_categories = generate_target_language_categories(semcat, conceptnet_path,
                                                            lang_source, lang_target, source_categories)
    fd = open(f"categories/semcat_{lang_source}-{lang_target}.json", mode="w", encoding="utf8")
    for key in target_categories:
        target_categories[key] = list(target_categories[key])
    json.dump(target_categories, fd, indent=2)
    fd.close()


if __name__ == '__main__':
    run()
