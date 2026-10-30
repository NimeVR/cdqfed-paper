"""Idempotent ordering patch for DMapS (FIX 1).  Only makes the iteration ORDER of tie candidates canonical (sorted by physical-qubit
index); search routine, objective, neighbourhood and iteration counts are untouched.  usage: python patch_dmaps.py <DMapS root>"""
import sys, re, pathlib
root = pathlib.Path(sys.argv[1]) / "src"
def sub(path, old, new):
    p = root / path; s = p.read_text()
    if new in s: return "already patched: " + path
    assert old in s, "pattern not found in " + path
    p.write_text(s.replace(old, new)); return "patched: " + path
print(sub("router/car_layout_routing.py", "        return candidate_swaps\n",
          "        return sorted(candidate_swaps, key=lambda s: (self._bit_indices[s[0]], self._bit_indices[s[1]]))   # PATCH: canonical order\n"))
print(sub("mapper/local_sabre_mapper.py", "        return candidate_swaps\n",
          "        return sorted(candidate_swaps, key=lambda s: (self._bit_indices[s[0]], self._bit_indices[s[1]]))   # PATCH: canonical order\n"))

# ---- hardware objects are stored in Python sets; default hash = memory address (ASLR) => set iteration order, hence the order in which
#      chip subsets / candidates are enumerated, changes from process to process.  Give them a value-based hash.
print(sub("frontend/chips_info_reader.py", "class ScQubit:\n    def __init__(",
          "class ScQubit:\n    def __hash__(self):  # PATCH: deterministic hash\n        return hash((\"q\", self._global_idx))\n\n    def __init__("))
print(sub("frontend/chips_info_reader.py", "class ScChip:\n    def __init__(",
          "class ScChip:\n    def __hash__(self):  # PATCH: deterministic hash\n        return hash((\"c\", self._chip_idx))\n\n    def __init__("))
print(sub("frontend/chips_info_reader.py", "class Connection:\n    def __init__(",
          "class Connection:\n    def __hash__(self):  # PATCH: deterministic hash\n        return hash((\"k\", self._qubit0._global_idx, self._qubit1._global_idx))\n\n    def __init__("))
