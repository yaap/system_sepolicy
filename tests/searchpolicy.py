#!/usr/bin/env python3
#
# Copyright 2021 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import tempfile

import policy

def do_main(libpath):
    parser = argparse.ArgumentParser(
        description="SELinux policy rule search tool. Intended to have a "
            + "similar API as sesearch, but simplified to use only code "
            + "available in AOSP")
    parser.add_argument("policy", help="Path to the SELinux policy to search.",
                        nargs="?")
    tertypes = parser.add_argument_group("TE Rule Types")
    tertypes.add_argument("-A", "--allow", action="append_const",
                        const="allow", dest="tertypes",
                        help="Search allow rules.")
    genfs = parser.add_argument_group("Genfscon Statements")
    genfs.add_argument("--genfs", action="store_true",
                        help="Display genfscon statements.")
    expr = parser.add_argument_group("Expressions")
    expr.add_argument("-s", "--source",
                      help="Source type/attribute of the TE rule.")
    expr.add_argument("-t", "--target",
                      help="Target type/attribute of the TE rule or genfscon.")
    expr.add_argument("-c", "--class", dest="tclass",
                      help="Comma separated list of object classes.")
    expr.add_argument("-p", "--perms", metavar="PERMS",
                      help="Comma separated list of permissions.")
    expr.add_argument("-f", "--fs",
                      help="Filesystem for genfscon statements.")

    args = parser.parse_args()

    if not args.tertypes and not args.genfs:
        parser.error("Must specify \"--allow\" or \"--genfs\"")

    if not args.policy:
        parser.error("Must include path to policy")

    pol = policy.Policy(args.policy, None, libpath)

    if args.genfs:
        for fs, path, context, _ in pol.QueryGenfs(fs=args.fs, target=args.target):
            print("genfscon " + fs + " " + path + " " + context)

    if args.tertypes:
        if args.source:
            scontext = {args.source}
        else:
            scontext = set()
        if args.target:
            tcontext = {args.target}
        else:
            tcontext = set()
        if args.tclass:
            tclass = set(args.tclass.split(","))
        else:
            tclass = set()
        if args.perms:
            perms = set(args.perms.split(","))
        else:
            perms = set()

        TERules = pol.QueryTERule(scontext=scontext,
                               tcontext=tcontext,
                               tclass=tclass,
                               perms=perms)

        # format rules for printing
        rules = []
        for r in TERules:
            if len(r.perms) > 1:
                rules.append("allow " + r.sctx + " " + r.tctx + ":" + r.tclass +
                             " { " + " ".join(sorted(r.perms)) + " };")
            else:
                rules.append("allow " + r.sctx + " " + r.tctx + ":" + r.tclass +
                             " " + " ".join(sorted(r.perms)) + ";")

        for r in sorted(rules):
            print(r)


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        lib_path = policy.ReadLibsepolwrap(temp_dir)
        do_main(lib_path)
