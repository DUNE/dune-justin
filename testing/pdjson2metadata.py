from inspect import ArgSpec
import sys, getopt, json, traceback, os
from metacat.webapi import MetaCatClient

Usage = """
python declare_meta.py [options] <dataset namespace>:<dataset name> <metadata_file.json> ...

Declares a file to MetaCat using the JSON file produced by ProtoDUNE DAQ (June 2022)

Dataset namespace, name - MetaCat dataset to add files to

Options:
    -n <namespace>              # file namespace, default - run type for first run in the metadata
    -m <MetaCat URL>            # default - METACAT_SERVER_URL environment variable value      
    -o (-|<output JSON file>)   # output file to write the resulting information, "-" means stdout
    -e <file.json>              # metadata to add/override, optional
"""

CoreAttributes = {
    "event_count":  "core.event_count",
    "file_type":    "core.file_type", 
    "file_format":  "core.file_format",
    "data_tier":    "core.data_tier", 
    "data_stream":  "core.data_stream", 
    "events":       "core.events",
    "first_event":  "core.first_event_number",
    "last_event":   "core.last_event_number",
    "event_count":  "core.event_count"
}


def metacat_metadata(metadata):
    
    metadata = metadata.copy()      # so that we do not modify the input dictionary in place
    
    #
    # discard native file attributes
    #
    file_name = metadata.pop("file_size", None)
    metadata.pop("checksum", None)
    metadata.pop("file_name", None)

    out = {}
    #
    # pop out and convert core attributes
    #
    runs_subruns = set()
    run_type = None
    runs = set()
    for run, subrun, rtype in metadata.pop("runs", []):
        run_type = rtype
        runs.add(run)
        runs_subruns.add(100000*run + subrun)
    out["core.runs_subruns"] = sorted(list(runs_subruns))
    out["core.runs"] = sorted(list(runs))
    out["core.run_type"] = run_type

    for name, value in metadata.items():
        if '.' not in name:
            try:    name = CoreAttributes[name]
            except KeyError:
                raise ValueError("Unknown core metadata parameter: %s = %s for file %s", (name, value, file_name))
        out[name] = value    
    out.setdefault("core.event_count", len(out.get("core.events", [])))
    return out

opts, args = getopt.getopt(sys.argv[1:], "n:m:o:e:")
opts = dict(opts)

if len(args) < 2 or "help" in args:
    print(Usage, file=sys.stderr)
    sys.exit(2)

metacat_url = opts.get("-m", os.environ.get("METACAT_SERVER_URL"))
if not metacat_url:
    print("MetaCat server URL must be specified using -m option or METACAT_SERVER_URL environment variable",
        file=sys.stderr
    )
    print(Usage)
    sys.exit(2)
client = MetaCatClient(metacat_url)

constant_namespace = opts.get("-n")
dataset_did = args[0]

extra_meta = {} if "-e" not in opts else json.load(open(opts["-e"], "r"))
assert isinstance(extra_meta, dict), "Extra metadata has to be a dictionary"
extra_meta = extra_meta or {}

files = []
for meta_fn in args[1:]:
    
    try:    input_metadata = json.load(open(meta_fn, "r"))
    except:
        print("Error reading metadata from {meta_fn}:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("\nNo file was declared", file=sys.stderr)
        sys.exit(1)

    try:    meta = metacat_metadata(input_metadata)
    except:
        print("Error converting metadata fom {meta_fn}:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("\nNo file was declared", file=sys.stderr)
        sys.exit(1)

    meta.update(extra_meta)
    file_info = {
            "namespace":    constant_namespace or input_metadata["runs"][0][2],
            "name":         input_metadata["file_name"],
            "metadata":     meta,
            "size":         input_metadata["file_size"],
            "checksums":    {   "adler32":  input_metadata["checksum"]   }
        }
    files.append(file_info)

try:    out = client.declare_files(dataset_did, files)
except Exception as e:
    print(f"Error declaring files to {dataset_did}: {e}", file=sys.stderr)
    sys.exit(1)

out_fn = opts.get("-o")
if out_fn:
    out_f = sys.stdout if out_fn == "-" else open(out_fn, "w")
    json.dump(out, out_f, indent=4, sort_keys=True)



