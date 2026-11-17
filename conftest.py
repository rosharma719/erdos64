# Root-level pytest configuration.
# Archived bundles under kb/runs/*/ (source_archive/, packets/, handoff/) contain test files that
# duplicate module names elsewhere and hard-code /mnt/data paths; they are records,
# not part of the live test suite.
collect_ignore_glob = ["kb/runs/*/source_archive/*", "kb/runs/*/packets/*", "kb/runs/*/handoff/*"]
