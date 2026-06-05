import pandas as pd
import re
import random

# ============================================================
#  CONFIG
# ============================================================
ORIGINAL_FILE    = "../data/raw/raw_test.tsv"
TRANSLATED_FILE  = "../data/translated/translated_test.tsv"

ORIGINAL_TEXT_COL   = 0
TRANSLATED_TEXT_COL = 0
LABEL_COL           = 1

SAMPLE_SIZE         = 200
SAMPLE_OUTPUT       = "manual_review_200.csv"
REPORT_OUTPUT       = "test_result.log"

# Rows that should NOT be translated — subtract 1 because you added 1

#For Train dataset
#EXCEPTION_ROWS = [x - 1 for x in [40112, 40590, 15697, 24274,37961]]

# For Dev dataset
#EXCEPTION_ROWS = [x - 1 for x in [1273,1852,4490]]

#For Test dataset
EXCEPTION_ROWS = []

# ============================================================

orig  = pd.read_csv(ORIGINAL_FILE,    header=None, delimiter='\t')
trans = pd.read_csv(TRANSLATED_FILE,  header=None, delimiter='\t')

report = []
def log(msg=""):
    print(msg)
    report.append(str(msg))

log("=" * 55)
log("      GOEMOTION PERSIAN — TEST REPORT")
log("=" * 55)
log(f"Original rows:     {len(orig)}")
log(f"Translated rows:   {len(trans)}")
log(f"Exception rows:    {EXCEPTION_ROWS} (skipped in tests)")
log()

# ----------------------------------------------------------
# TEST 1: Row count & additional/missing rows
# ----------------------------------------------------------
log("[ TEST 1 ] Row Count & Additional/Missing Rows")
diff = len(trans) - len(orig)
if diff == 0:
    log(f"  ✅ PASS — Both files have {len(orig)} rows")
elif diff > 0:
    log(f"  ❌ FAIL — Translated file has {diff} EXTRA rows")
    log(f"     Extra indices: {list(range(len(orig), len(trans)))[:20]}")
else:
    log(f"  ❌ FAIL — Translated file is MISSING {abs(diff)} rows")
    log(f"     Missing from index {len(trans)} onward")
log()

min_rows   = min(len(orig), len(trans))
orig_text  = orig.iloc[:min_rows, ORIGINAL_TEXT_COL].astype(str).str.strip()
trans_text = trans.iloc[:min_rows, TRANSLATED_TEXT_COL].astype(str).str.strip()
labels     = orig.iloc[:min_rows, LABEL_COL]

# All valid indices (excluding exceptions)
valid_idx = [i for i in range(min_rows) if i not in EXCEPTION_ROWS]

# ----------------------------------------------------------
# TEST 2: Missing / empty translations (skip exceptions)
# ----------------------------------------------------------
log("[ TEST 2 ] Missing or Empty Translations")
missing = trans_text.iloc[valid_idx]
missing = missing[missing.isna() | (missing == "") | (missing == "nan")]
if len(missing) == 0:
    log(f"  ✅ PASS — No empty translations")
else:
    log(f"  ❌ FAIL — {len(missing)} empty/missing rows")
    log(f"     Indices: {list(missing.index[:20])}")
log()

# ----------------------------------------------------------
# TEST 3: Persian script validity (skip exceptions)
# ----------------------------------------------------------
log("[ TEST 3 ] Persian Script Validity")
def persian_ratio(text):
    text = str(text)
    persian = len(re.findall(r'[\u0600-\u06FF]', text))
    return persian / max(len(text), 1)

ratios = trans_text.apply(persian_ratio)
bad = ratios.iloc[valid_idx][ratios.iloc[valid_idx] < 0.3]
if len(bad) == 0:
    log(f"  ✅ PASS — All rows contain valid Persian script")
else:
    log(f"  ❌ FAIL — {len(bad)} rows have low/no Persian content")
    log(f"     Indices: {list(bad.index[:20])}")
log(f"     Avg Persian ratio: {ratios.iloc[valid_idx].mean():.2%}")
log()

# ----------------------------------------------------------
# TEST 4: Untranslated rows (skip exceptions)
# ----------------------------------------------------------
log("[ TEST 4 ] Untranslated Rows (Identical to Source)")
identical = orig_text.iloc[valid_idx] == trans_text.iloc[valid_idx]
if identical.sum() == 0:
    log(f"  ✅ PASS — No untranslated rows (exceptions excluded)")
else:
    log(f"  ❌ FAIL — {identical.sum()} rows were NOT translated")
    log(f"     Indices: {list(identical[identical].index[:20])}")
log()

# Confirm exception rows are intact
log("[ INFO  ] Exception Row Status")
for idx in EXCEPTION_ROWS:
    if idx < min_rows:
        log(f"  Row {idx+1:>6} | SRC: {orig_text.iloc[idx][:60]}")
        log(f"         | TRN: {trans_text.iloc[idx][:60]}")
log()

# ----------------------------------------------------------
# TEST 5: Suspicious length (skip exceptions)
# ----------------------------------------------------------
log("[ TEST 5 ] Suspicious Translation Length")
length_ratio = trans_text.str.len() / orig_text.str.len().replace(0, 1)
too_short = length_ratio.iloc[valid_idx][length_ratio.iloc[valid_idx] < 0.25]
if len(too_short) == 0:
    log(f"  ✅ PASS — No suspiciously short translations")
else:
    log(f"  ⚠️  WARN — {len(too_short)} suspiciously short translations")
    log(f"     Indices: {list(too_short.index[:20])}")
log(f"     Avg length ratio: {length_ratio.iloc[valid_idx].mean():.2f}")
log()

# ----------------------------------------------------------
# TEST 6: Duplicate translations (skip exceptions)
# ----------------------------------------------------------
log("[ TEST 6 ] Duplicate Translations")
dupes = trans_text.iloc[valid_idx].duplicated().sum()
if dupes == 0:
    log(f"  ✅ PASS — No duplicate translations")
else:
    log(f"  ⚠️  WARN — {dupes} duplicate translations found")
log()

# ----------------------------------------------------------
# TEST 7: Labels intact
# ----------------------------------------------------------
log("[ TEST 7 ] Labels Intact")
missing_labels = labels.isna().sum()
if missing_labels == 0:
    log(f"  ✅ PASS — All labels present ({labels.nunique()} unique labels)")
else:
    log(f"  ❌ FAIL — {missing_labels} missing labels")
log()

# ----------------------------------------------------------
# EXPORT: 500 random sample (never include exception rows)
# ----------------------------------------------------------
log("=" * 55)
log("    EXPORTING 500 RANDOM SAMPLE FOR MANUAL REVIEW")
log("=" * 55)

sample_pool    = [i for i in range(min_rows) if i not in EXCEPTION_ROWS]
random_indices = sorted(random.sample(sample_pool, min(SAMPLE_SIZE, len(sample_pool))))

sample = pd.DataFrame({
    "row_number" : [i + 1 for i in random_indices],   # +1 so matches what you see
    "original"   : orig_text.iloc[random_indices].values,
    "translated" : trans_text.iloc[random_indices].values,
    "label"      : labels.iloc[random_indices].values,
    "persian_%"  : (ratios.iloc[random_indices].values * 100).round(1),
})

sample.to_csv(SAMPLE_OUTPUT, index=False, encoding="utf-8-sig")
log(f"  ✅ Saved: {SAMPLE_OUTPUT}  ({len(sample)} rows)")
log()

with open(REPORT_OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(report))
log(f"  Report saved: {REPORT_OUTPUT}")
log("=" * 55)