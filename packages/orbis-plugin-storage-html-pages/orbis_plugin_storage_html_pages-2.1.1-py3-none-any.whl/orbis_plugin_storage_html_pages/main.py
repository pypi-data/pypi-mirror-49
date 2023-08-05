# -*- coding: utf-8 -*-

from orbis_eval import app
from orbis_eval.libs import files
from .html_templates import html_body

import os
from palettable.tableau import Tableau_20
from operator import itemgetter


class Main(object):

    def __init__(self, rucksack):

        super(Main, self).__init__()
        self.rucksack = rucksack
        self.config = self.rucksack.open['config']
        self.data = self.rucksack.open['data']
        self.pass_name = self.rucksack.open['config']['file_name'].split(".")[0]
        self.folder = os.path.join(app.paths.output_path, "html_pages", self.pass_name)
        self.queue = self.rucksack.get_keys()

    def _get_keys(self, item):

        keys = set()
        for entity in item['gold']:
            keys.add(entity['key'])
        for entity in item['computed']:
            keys.add(entity['key'])
        return keys

    def _get_sf_colors(self, keys):

        sf_colors = {}
        colour_idx = 0
        for sf in keys:
            sf_colors[sf] = Tableau_20.hex_colors[colour_idx]
            colour_idx = 0 if colour_idx == 19 else colour_idx + 1
        return sf_colors

    def _get_gold_entities(self, item, sf_colors, gold_html):

        gold_entities = []
        if len(item['gold']) > 0:
            last_start = int(len(item['corpus']))
            last_end = int(len(item['corpus']))
            # last_word = ""
            for entity in sorted(item['gold'], key=itemgetter("end"), reverse=True):
                entity_types = self.rucksack.result_summary(specific='binary_classification')['entities']

                if entity['entity_type'] not in entity_types and len(entity_types) >= 0:
                    continue
                start_tag = '<abbr title="{}" style="background-color:{};">'.format(entity['key'], sf_colors[entity['key']])
                end_tag = '</abbr>'
                if int(entity['start']) <= int(last_start):
                    if int(entity['start']) < int(last_end):
                        entity_start = int(entity['start'])
                    else:
                        entity_start = False
                        # case = 1
                        # print("{}\t-\t{}: {} (1)\n{}\t-\t{}: {}".format(entity['start'], entity['end'], entity['surfaceForm'], last_start, last_end, last_word))
                else:
                    entity_start = False
                    # case = 2
                    # print("{}\t-\t{}: {} (2)\n{}\t-\t{}: {}".format(entity['start'], entity['end'], entity['surfaceForm'], last_start, last_end, last_word))
                if int(entity['end']) < int(last_end):
                    if int(entity['end']) < int(last_start):
                        entity_end = int(entity['end'])
                    else:
                        entity_end = False
                        # case = 3
                        # print("{}\t-\t{}: {} (3)\n{}\t-\t{}: {}".format(entity['start'], entity['end'], entity['surfaceForm'], last_start, last_end, last_word))
                else:
                    entity_end = False
                    # case = 4
                    # print("{}\t-\t{}: {} (4)\n{}\t-\t{}: {}".format(entity['start'], entity['end'], entity['surfaceForm'], last_start, last_end, last_word))
                if isinstance(entity_start, int) and entity_end:
                    gold_html = gold_html[:int(entity['end'])] + end_tag + gold_html[int(entity['end']):]
                    gold_html = gold_html[:int(entity['start'])] + start_tag + gold_html[int(entity['start']):]
                else:
                    if len(entity['key']) > 0:
                        overlap_warning = '<abbr title="{}" style="background-color:{};"><b>&#x22C2;</b></abbr>'.format(entity['key'], sf_colors[entity['key']])
                        gold_html = gold_html[:int(last_start)] + overlap_warning + gold_html[int(last_start):]
                        # print("-{}-> {}\t-\t{}: {}\n{}\t-\t{}: {}".format(case, entity['start'], entity['end'], entity['surfaceForm'], last_start, last_end, last_word))
                last_start = entity_start or last_start
                last_end = entity_end or last_end
                # last_word = entity['surfaceForm']
                gold_entities.append({
                    "surfaceForm": entity['surfaceForm'],
                    "key": entity['key'],
                    "start": entity['start'],
                    "end": entity['end'],
                    "entity_type": entity['entity_type'],
                    "background": sf_colors[entity['key']]})
        return gold_entities, gold_html

    def _get_computed_entities(self, item, sf_colors, computed_html):

        computed_entities = []
        if len(item['computed']) > 0:
            last_start = len(item['corpus'])
            last_end = len(item['corpus'])
            # last_word = ""
            for e_idx, entity in enumerate(sorted(item['computed'], key=itemgetter("document_end"), reverse=True)):
                entity_types = self.config['scoring'].get('entities', [])
                if entity['entity_type'] not in entity_types and len(entity_types) >= 0:
                    continue
                is_fp = False
                entity_id = "{},{}".format(entity['document_start'], entity['document_end'])
                is_fp = True if entity_id in self.rucksack.resultview(item['index'], specific="binary_classification")['confusion_matrix']['fp_ids'] else False
                if is_fp:
                    start_tag = '<abbr title="{}" style="background-color:{}"><s>'.format(entity['key'], sf_colors[entity['key']])
                    end_tag = '</s></abbr>'
                else:
                    start_tag = '<abbr title="{}" style="background-color:{}">'.format(entity['key'], sf_colors[entity['key']])
                    end_tag = '</abbr>'
                if int(entity['document_start']) <= int(last_start):
                    if int(entity['document_start']) < int(last_end):
                        entity_start = int(entity['document_start'])
                    else:
                        entity_start = False
                        # case = 1
                        # print("{}\t-\t{}: {} (1)\n{}\t-\t{}: {}".format(entity['document_start'], entity['document_end'], entity['surfaceForm'], last_start, last_end, last_word))
                else:
                    entity_start = False
                    # case = 2
                    # print("{}\t-\t{}: {} (2)\n{}\t-\t{}: {}".format(entity['document_start'], entity['document_end'], entity['surfaceForm'], last_start, last_end, last_word))
                if int(entity['document_end']) < int(last_end):
                    if int(entity['document_end']) < int(last_start):
                        entity_end = int(entity['document_end'])
                    else:
                        entity_end = False
                        # case = 3
                        # print("{}\t-\t{}: {} (3)\n{}\t-\t{}: {}".format(entity['document_start'], entity['document_end'], entity['surfaceForm'], last_start, last_end, last_word))
                else:
                    entity_end = False
                    # case = 4
                    # print("{}\t-\t{}: {} (4)\n{}\t-\t{}: {}".format(entity['document_start'], entity['document_end'], entity['surfaceForm'], last_start, last_end, last_word))
                if isinstance(entity_start, int) and entity_end:
                    computed_html = computed_html[:int(entity['document_end'])] + end_tag + computed_html[int(entity['document_end']):]
                    computed_html = computed_html[:int(entity['document_start'])] + start_tag + computed_html[int(entity['document_start']):]
                else:
                    if len(entity['key']) > 0:
                        if is_fp:
                            overlap_warning = '<abbr title="{}" style="background-color:{};"><s><b>&#x22C2;</b></s></abbr>'.format(entity['key'], sf_colors[entity['key']])
                        else:
                            overlap_warning = '<abbr title="{}" style="background-color:{};"><b>&#x22C2;</b></abbr>'.format(entity['key'], sf_colors[entity['key']])
                        computed_html = computed_html[:int(last_start)] + overlap_warning + computed_html[int(last_start):]
                        # print("[orbis] -{}-> {}\t-\t{}: {}\n{}\t-\t{}: {}".format(case, entity['document_start'], entity['document_end'], entity['surfaceForm'], last_start, last_end, last_word))
                last_start = entity_start or last_start
                last_end = entity_end or last_end
                # last_word = entity['surfaceForm']
                computed_entities.append({
                    "surfaceForm": entity['surfaceForm'],
                    "key": entity['key'],
                    "start": entity['document_start'],
                    "end": entity['document_end'],
                    "entity_type": entity['entity_type'],
                    "background": sf_colors[entity['key']]})
        return computed_entities, computed_html

    def _get_top_header(self):

        top_header_0 = {
            "aggregator_name": self.config['aggregation']['service']['name'],
            "aggregator_profile": self.config['aggregation']['service'].get("profile", "None"),
            "aggregator_limit": self.config['aggregation']['service'].get("limit", "None"),
            "aggregator_location": self.config['aggregation']['service']['location']
        }
        top_header_1 = {
            "aggregator_data_set": self.config['aggregation']['input']['data_set']['name'],
            "evaluator_name": self.config['evaluation']['name'],
            "scorer_name": self.config['scoring']['name'],
            "entities": ", ".join([e for e in self.rucksack.result_summary(specific='binary_classification')['entities']])
        }
        top_header_2 = {
            "has_score": self.rucksack.result_summary(specific='binary_classification')['has_score'],
            "no_score": self.rucksack.result_summary(specific='binary_classification')['no_score'],
            "empty_responses": self.rucksack.result_summary(specific='binary_classification')['empty_responses']
        }
        micro_precision = f"{self.rucksack.result_summary(specific='binary_classification')['micro']['precision']:.3f}"
        macro_precision = f"{self.rucksack.result_summary(specific='binary_classification')['macro']['precision']:.3f}"
        micro_macro_precision = "(" + "/".join([str(micro_precision), str(macro_precision)]) + ")"
        micro_recall = f"{self.rucksack.result_summary(specific='binary_classification')['micro']['recall']:.3f}"
        macro_recall = f"{self.rucksack.result_summary(specific='binary_classification')['macro']['recall']:.3f}"
        micro_macro_recall = "(" + "/".join([str(micro_recall), str(macro_recall)]) + ")"
        micro_f1_score = f"{self.rucksack.result_summary(specific='binary_classification')['micro']['f1_score']:.3f}"
        macro_f1_score = f"{self.rucksack.result_summary(specific='binary_classification')['macro']['f1_score']:.3f}"
        micro_macro_f1_score = "(" + "/".join([str(micro_f1_score), str(macro_f1_score)]) + ")"
        top_header_3 = {
            "precision": micro_macro_precision,
            "recall": micro_macro_recall,
            "f1_score": micro_macro_f1_score,
        }
        header_html_0 = """
        <b>Aggregator Name:</b>\t{aggregator_name}</br>
        <b>Aggregator Profile:</b>\t{aggregator_profile}</br>
        <b>Aggregator Limit:</b>\t{aggregator_limit}</br>
        <b>Aggregator Service:</b>\t{aggregator_name}</br>
        """.format(**top_header_0)
        header_html_1 = """
        <b>Aggregator Dataset:</b>\t{aggregator_data_set}</br>
        <b>Evaluator Name:</b>\t{evaluator_name}</br>
        <b>Scorer Name:</b>\t{scorer_name}</br>
        <b>Entities:</b>\t{entities}</br>
        """.format(**top_header_1)
        header_html_2 = """
        <b>Some Score:</b>\t{has_score}</br>
        <b>No Score:</b>\t{no_score}</br>
        <b>Empty Responses:</b>\t{empty_responses}</br>
        """.format(**top_header_2)
        header_html_3 = """
        <b>Precision (micro/macro):</b>\t{precision}</br>
        <b>Recall (micro/macro):</b>\t{recall}</br>
        <b>F1 Score (micro/macro):</b>\t{f1_score}</br>
        """.format(**top_header_3)
        return header_html_0, header_html_1, header_html_2, header_html_3

    def _get_item_header(self, key):

        item_header_0 = {
            "precision": self.rucksack.resultview(key, specific='binary_classification')['precision'],
            "recall": self.rucksack.resultview(key, specific='binary_classification')['recall'],
            "f1_score": self.rucksack.resultview(key, specific='binary_classification')['f1_score']
        }
        item_header_1 = {
            "tp": sum(self.rucksack.resultview(key, specific='binary_classification')['confusion_matrix']['tp']),
            "fp": sum(self.rucksack.resultview(key, specific='binary_classification')['confusion_matrix']['fp']),
            "fn": sum(self.rucksack.resultview(key, specific='binary_classification')['confusion_matrix']['fn'])
        }
        header_html_0 = """
        <b>Precision:</b>\t{precision:.3f}</br>
        <b>Recall:</b>\t{recall:.3f}</br>
        <b>F1 Score:</b>\t{f1_score:.3f}</br>
        """.format(**item_header_0)
        header_html_1 = """
        <b>True Positives:</b>\t{tp}</br>
        <b>False Positives:</b>\t{fp}</br>
        <b>False Negatives:</b>\t{fn}</br>
        """.format(**item_header_1)
        return header_html_0, header_html_1

    def _get_gold_html(self, item, sf_colors):

        gold_html = item['corpus']
        gold_entities, gold_html = self._get_gold_entities(item, sf_colors, gold_html)
        gold_entities_html = ""
        for entity in list(reversed(gold_entities)):
            gold_entities_html += '<p><span style="background-color:{background};"><b>{surfaceForm}</b></span> (<a href="{key}">{key}</a>): {start} - {end}: {entity_type}</p>'.format(**entity)
        return gold_html, gold_entities_html

    def _get_computed_html(self, item, sf_colors):

        computed_html = item['corpus']
        computed_entities, computed_html = self._get_computed_entities(item, sf_colors, computed_html)
        computed_entities_html = ""
        for entity in list(reversed(computed_entities)):
            computed_entities_html += '<p><span style="background-color:{background};"><b>{surfaceForm}</b></span> (<a href="{key}">{key}</a>): {start} - {end}: {entity_type}</p>'.format(**entity)
        return computed_html, computed_entities_html

    def _get_next_button(self, key):

        if key:
            next_item = os.path.join(str(key) + ".html")

            next_button = """<p><a id="next_page_link" class="btn btn-secondary" href="{url}" role="button" style="float: right;">Next Item &raquo;</a></p>""".format(url=next_item)
        else:
            next_button = ""
        return next_button

    def _get_previous_button(self, key):

        if key:
            previous_item = os.path.join(str(key) + ".html")
            previous_button = """<p><a id="previous_page_link" class="btn btn-secondary" href="{url}" role="button">&laquo; Previous Item</a></p>""".format(url=previous_item)
        else:
            previous_button = ""
        return previous_button

    def _build_html_page(self, item, next_item, previous_item, sf_colors):

        key = item['index']
        header_html_0, header_html_1, header_html_2, header_html_3 = self._get_top_header()
        header_html_4, header_html_5 = self._get_item_header(key)
        gold_html, gold_entities_html = self._get_gold_html(item, sf_colors)
        computed_html, computed_entities_html = self._get_computed_html(item, sf_colors)

        previous_button = self._get_previous_button(previous_item)
        next_button = self._get_next_button(next_item)

        html_item_dict = {
            "header_html_0": header_html_0, "header_html_1": header_html_1,
            "header_html_2": header_html_2, "header_html_3": header_html_3,
            "header_html_4": header_html_4, "header_html_5": header_html_5,
            "gold_html": gold_html, "computed_html": computed_html,
            "gold_entities_html": gold_entities_html, "computed_entities_html": computed_entities_html,
            "prev": previous_button, "next": next_button, "item_number": key
        }
        html = html_body.format(**html_item_dict)
        return html

    def run(self):

        app.logger.debug("Building HTML pages")

        timestamp = files.get_timestamp()
        folder_dir = os.path.join(self.folder + f"-{timestamp}")
        files.create_folder(folder_dir)

        for item_key in self.queue:
            item = self.rucksack.itemview(item_key)

            try:
                next_item = self.queue[self.queue.index(item_key) + 1]
            except IndexError:
                next_item = None

            try:
                previous_item = self.queue[self.queue.index(item_key) - 1]
            except IndexError:
                previous_item = None

            key = item['index']
            keys = self._get_keys(item)
            sf_colors = self._get_sf_colors(keys)
            html = self._build_html_page(item, next_item, previous_item, sf_colors)

            file_dir = os.path.join(folder_dir, str(key) + ".html")
            app.logger.debug(file_dir)
            with open(file_dir, "w") as open_file:
                open_file.write(html)
        app.logger.info("Finished building HTML pages")
