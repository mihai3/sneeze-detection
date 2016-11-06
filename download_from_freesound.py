#!/usr/bin/env python

import oauth2
import re
import argparse
import json
import logging

import time

import sys

import freesound
import os
import urlparse


def get_freesound_client(credentials):
    logging.info("connecting to freesound")

    freesound_client = freesound.FreesoundClient()
    freesound_client.set_token(credentials["API_TOKEN"])


    return freesound_client


def load_credentials():
    credentials = {}
    with open("CREDENTIALS") as c:
        for line in c.readlines():
            m = re.match("([^=]*)=(.*)", line)
            if m is not None:
                key, val = m.groups()
                credentials[key] = val  # TODO escape
                logging.info("credentials: found %s", key)
    return credentials


def main(args):
    credentials = load_credentials()

    if not os.path.isdir(args.output_dir):
        logging.info("creating dir %s", args.output_dir)
        os.mkdir(args.output_dir)

    ids = []

    if args.json_input:
        with open(args.json_input) as f:
            for obj in json.load(f):
                if obj is None or "id" not in obj:
                    logging.warning("skipping obj!")
                else:
                    ids.append(obj["id"])

    if args.urltxt_input:
        with open(args.urltxt_input) as f:
            for line in f.readlines():
                m = re.match("https://.*/([0-9]+)/.*", line)
                if m is not None:
                    ids.append(int(m.group(1)))

    logging.info("loading %s ids", len(ids))

    client = get_freesound_client(credentials)

    cnt = 0
    last_ts = time.time()

    for i in ids:
        if os.path.exists(os.path.join(args.output_dir, "%s.mp3" % str(i))):
            logging.info("skipping %s", i)
            continue

        snd = client.get_sound(i)
        logging.info("retrieving %s", i)
        snd.retrieve_preview(args.output_dir, "%s.mp3" % str(snd.id))
        cnt += 1

        if cnt >= 60 and time.time() - last_ts < 65:
            logging.info("sleeping")
            time.sleep(5 + (65 - (time.time() - last_ts)))
            cnt = 0
            last_ts = time.time()

if __name__ == "__main__":
    _parser = argparse.ArgumentParser()

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    _parser.add_argument("--json-input", default=None, help="Load list of objects with 'id' attribute from JSON file (e.g. not_really_similar.json)")
    _parser.add_argument("--urltxt-input", help="Load list ob objects by parsing URLs (e.g. from sneeezes.txt)")
    _parser.add_argument("--output-dir", default="sounds")

    _args = _parser.parse_args()
    main(_args)