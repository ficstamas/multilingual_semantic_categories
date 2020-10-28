from semcat import SemCat
from conceptnet import ConceptNet
import re
import json
from argparse import ArgumentParser
import os
import logging
from relations import ALLOWED_RELATIONS, SEARCH_TERMS_INV
import asyncio

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


language = lambda inp, lang: re.match(f"/c/{lang}/[A-Za-z0-9_\-/]*", inp)
extract_token = lambda inp: inp.split("/")[3]
lang_test = lambda src, trg, start, end: (language(start, src) and language(end, trg)) or (language(end, src) and language(start, trg))


def generate_source_language_categories(conceptnet_path, lang_source):
    """
    Generates semantic categories in lang_source language
    Parameters
    ----------
    conceptnet_path
        Path to conceptnet
    lang_source
        Source language
    Returns
    -------
        dict:
            Generated categories
    """
    categories = {concept: set([concept]) for concept in ALLOWED_RELATIONS.keys()}
    category_keys = list(ALLOWED_RELATIONS.keys())

    logging.info("Gathering related and similar terms...")
    i = 0
    with ConceptNet(conceptnet_path) as f:
        for relation, start, end, weight in f:
            if i % 1000000 == 0:
                logging.info(f"[1/4] {i} lines processed...")
            # Language test
            if lang_test(lang_source, lang_source, start, end):
                start_token = extract_token(start)
                end_token = extract_token(end)

                if start_token in ALLOWED_RELATIONS:
                    if relation in ALLOWED_RELATIONS[start_token]:
                        if relation == "/r/RelatedTo" and weight >= 1.0:
                            categories[start_token].add(end_token)
                        elif relation != "/r/RelatedTo":
                            categories[start_token].add(end_token)
                if start_token in SEARCH_TERMS_INV:
                    if relation in ALLOWED_RELATIONS[SEARCH_TERMS_INV[start_token]]:
                        if relation == "/r/RelatedTo" and weight >= 1.0:
                            categories[SEARCH_TERMS_INV[start_token]].add(end_token)
                        elif relation != "/r/RelatedTo":
                            categories[SEARCH_TERMS_INV[start_token]].add(end_token)

                if end_token in ALLOWED_RELATIONS:
                    if relation in ALLOWED_RELATIONS[end_token]:
                        if relation == "/r/RelatedTo" and weight >= 1.0:
                            categories[end_token].add(start_token)
                        elif relation != "/r/RelatedTo":
                            categories[end_token].add(start_token)
                if end_token in SEARCH_TERMS_INV:
                    if relation in ALLOWED_RELATIONS[SEARCH_TERMS_INV[end_token]]:
                        if relation == "/r/RelatedTo" and weight >= 1.0:
                            categories[SEARCH_TERMS_INV[end_token]].add(start_token)
                        elif relation != "/r/RelatedTo":
                            categories[SEARCH_TERMS_INV[end_token]].add(start_token)

            i += 1
    return categories


async def generate_intermediate_language_categories(conceptnet_path, lang_source, lang_mid, lang_target, source):
    """
    Translates semantic categories to an intermediate language, and further transforms it to the target language
    Parameters
    ----------
    conceptnet_path
        Path to ConceptNet
    lang_source
        Source Language
    lang_mid
        Middle Language
    lang_target
        Target Language
    source
        Semantic Categories in source language
    Returns
    -------

    """
    categories_from_source = {concept: set() for concept in ALLOWED_RELATIONS.keys()}
    categories_to_target = {concept: set() for concept in ALLOWED_RELATIONS.keys()}

    logging.info("Generating intermediate language categories...")
    i = 0
    with ConceptNet(conceptnet_path) as f:
        for relation, start, end, weight in f:
            if i % 1000000 == 0:
                logging.info(f"[2/4] {i} lines processed...")

            if lang_test(lang_source, lang_mid, start, end):
                start_token = extract_token(start)
                end_token = extract_token(end)
                if relation == "/r/RelatedTo" or relation == "/r/Synonym":
                    for key in source:
                        for item in list(source[key]):
                            if start_token == item:
                                categories_from_source[key].add(end_token)
                            if end_token == item:
                                categories_from_source[key].add(start_token)
            i += 1

    logging.info("Generating target language categories from intermediate categories...")

    i = 0
    with ConceptNet(conceptnet_path) as f:
        for relation, start, end, weight in f:
            if i % 1000000 == 0:
                logging.info(f"[3/4] {i} lines processed...")

            if lang_test(lang_mid, lang_target, start, end):
                start_token = extract_token(start)
                end_token = extract_token(end)
                if relation == "/r/RelatedTo" or relation == "/r/Synonym":
                    for key in categories_from_source:
                        for item in list(categories_from_source[key]):
                            if start_token == item:
                                categories_to_target[key].add(end_token)
                            if end_token == item:
                                categories_to_target[key].add(start_token)
            i += 1
    return categories_to_target


async def generate_target_language_categories(conceptnet_path, lang_source, lang_target, source_categories):
    """
    Translates semantic categories from source language to target language
    Parameters
    ----------
    conceptnet_path
    lang_source
    lang_target
    source_categories

    Returns
    -------

    """
    categories = {concept: set() for concept in ALLOWED_RELATIONS.keys()}
    logging.info("Generating target language categories")
    i = 0

    with ConceptNet(conceptnet_path) as f:
        for relation, start, end, weight in f:
            if i % 1000000 == 0:
                logging.info(f"[4/4] {i} lines processed...")
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


async def parallelization(conceptnet_path, lang_source, lang_intermediate, lang_target, source_categories):
    """
    It would run both translations in parallel, but due to the resource it can not be happen
    Parameters
    ----------
    conceptnet_path
    lang_source
    lang_intermediate
    lang_target
    source_categories

    Returns
    -------

    """
    results = await asyncio.gather(generate_intermediate_language_categories(conceptnet_path, lang_source,
                                                                             lang_intermediate, lang_target,
                                                                             source_categories),
                                   generate_target_language_categories(conceptnet_path, lang_source, lang_target,
                                                                       source_categories)
                                   )
    return results[0], results[1]


def run():
    parser = ArgumentParser(description='Glove interpretibility')

    parser.add_argument("--conceptnet_path", type=str, required=True)
    parser.add_argument("--source_language", type=str, required=False, default="en")
    parser.add_argument("--intermediate_language", type=str, required=False, default="en")
    parser.add_argument("--target_language", type=str, required=False, default="en")
    args = parser.parse_args()

    lang_source = args.source_language
    lang_target = args.target_language
    lang_intermediate = args.intermediate_language
    conceptnet_path = args.conceptnet_path

    if not os.path.exists("categories/"):
        os.mkdir("categories")

    # Generating categories
    source_categories = generate_source_language_categories(conceptnet_path, lang_source)
    # Translating categories to a middle and target language
    validation_categories, target_categories = asyncio.run(
        parallelization(conceptnet_path, lang_source, lang_intermediate, lang_target, source_categories)
    )

    # Producing output categories by taking the intersection of the category words of target language and
    # the indirectly translated one
    output_categories = {concept: set() for concept in ALLOWED_RELATIONS.keys()}

    for key in validation_categories:
        c1: set
        c1 = validation_categories[key]
        c2: set
        c2 = target_categories[key]
        output_categories[key] = c1.intersection(c2)

    # Saving to file
    fd = open(f"categories/semcat_{lang_source}-{lang_intermediate}-{lang_target}.json", mode="w", encoding="utf8")
    for key in output_categories:
        output_categories[key] = list(output_categories[key])
    json.dump(output_categories, fd, indent=2)
    fd.close()


if __name__ == '__main__':
    run()
