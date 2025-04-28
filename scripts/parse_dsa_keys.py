#! /usr/bin/env python

import json
import sys
import re

class GiveUp(Exception):
    pass

if len(sys.argv) != 3:
    raise GiveUp("Syntax: parse_dsa_keys [in_file] [out_file]");

(in_file, out_file) = sys.argv[1:]
with open(in_file, 'r') as f:
    lines = f.readlines()

def rec_valid(r):
    return "seed" in rec and "sk" in rec and "pk" in rec

results = [ ]
rec = { }
RE_SEED = re.compile(r"(.*)Keygen - Seed = (.*)")
SK = re.compile(r"Keygen - SK: = (.*)")
PK = re.compile(r"Keygen - PK after pkEncode: = (.*)")
for l in lines:
    m = RE_SEED.match(l);
    if m is not None:
        if rec_valid(rec):
            results.append(rec)
        rec = { "seed": m.group(2).strip() }
    m = SK.match(l)
    if m is not None:
        rec["sk"] = m.group(1).strip()
    m = PK.match(l)
    if m is not None:
        rec["pk"] = m.group(1).strip()

if rec_valid(rec):
    results.append(rec)
with open(out_file, 'w') as f:
    json.dump(results, f, indent=2)
print(f"Wrote {len(results)} entries")
