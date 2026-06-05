# GoEmotion Persian 
![License](https://img.shields.io/badge/license-CC_BY_4.0-lightgrey.svg?style=for-the-badge)
![Language](https://img.shields.io/badge/language-Persian_(Farsi)-blue.svg?style=for-the-badge)
![Dataset Size](https://img.shields.io/badge/rows-~54K-green.svg?style=for-the-badge)
![Kaggle](https://img.shields.io/badge/kaggle-dataset-orange.svg?style=for-the-badge&logo=kaggle)

## 📖 Overview

This dataset is a Persian (Farsi) translation of the **GoEmotions** benchmark,
originally created by Google Research. GoEmotions is one of the largest
fine-grained emotion datasets available, containing Reddit comments labeled
across 27 emotion categories plus Neutral.

This Persian version makes the GoEmotions benchmark accessible for **Persian
NLP research**, enabling tasks such as emotion detection, sentiment analysis,
and multi-label text classification in Farsi.

---

## 📥 Dataset Access

The GoEmotion Persian dataset can be accessed in multiple ways:

### 1️⃣ Kaggle Dataset

The dataset is also available on Kaggle for direct use in notebooks:

👉 [https://www.kaggle.com/datasets/aydakikio/goemotion-persian](https://www.kaggle.com/datasets/aydakikio/goemotion-persian)

You can use it directly in Kaggle:

```
import pandas as pd

path = "/kaggle/input/goemotion-persian/translated_train.tsv"
df = pd.read_csv(path, sep="\t", header=None)
```

---

### 2️⃣ Download from GitHub Releases

Pre-packaged dataset versions are available in the **Releases** section:

👉 [https://github.com/aydakikio/goemotion_persian/releases](https://github.com/aydakikio/goemotion_persian/releases)

You can download:

* Raw TSV files
* Translated dataset


---
### 3️⃣ Clone the Repository (Recommended for development)

```bash
git clone https://github.com/aydakikio/goemotion_persian.git
cd goemotion_persian
```

---

## 🧭 Provenance

This dataset is a Persian translation of the **GoEmotions benchmark** created by Google Research.

The dataset was constructed using a hybrid pipeline:

### 🤖 Automated Translation

* The majority of translations were generated using:
  * **Gemini 2.5**
  * **Gemini 2.5 Lite**
* These models were used to translate English Reddit comments into Persian while preserving emotional context and label alignment.

### ✋ Manual Correction

* A subset of samples was manually translated and corrected.
* Manual review focused on:

  * untranslated or partially translated rows
  * noisy inputs (URLs, special tokens, malformed text)
  * improving fluency and cultural adaptation in Persian

### 🧪 Quality Control

* Automated validation tests were applied to ensure:

  * Persian script consistency
  * missing or empty translations detection
  * duplication filtering
  * length ratio sanity checks between source and target text

### 📊 Human Review

* A random sample of ~500 rows from each split was manually inspected to assess translation quality and consistency.

### 🔗 Reproducibility
This repository includes:

* translation pipeline implementation
* dataset preprocessing scripts
* QA / validation tools
* experiment and processing logs
* skipped / error batch tracking

---

## 🗂️ Repository Structure

```
goemotion_persian/
├── data
│   ├── raw
│   │   ├── raw_dev.tsv # 5,426 rows
│   │   ├── raw_test.tsv # 5,427 rows
│   │   └── raw_train.tsv # 43,410 rows
│   ├── test_sample
│   │   ├── dev_dataset_manual_review_200.csv #200 rows
│   │   ├── test_dataset_manual_review_200.csv #200 rows
│   │   └── train_dataset_manual_review_500.csv #500 rows
│   └── translated
│       ├── translated_dev.tsv # 5,426 rows
│       ├── translated_test.tsv # 5,427 rows
│       └── translated_train.tsv # 43,410 rows
├── source_code 
│   ├── audiot_test.py #Quality tester
|   └── translator.py #translation pipeline
├── log_files
│   ├── test
│   │   ├── dev_translate_test_1.log
│   │   ├── dev_translate_test_2.log
│   │   ├── dev_translate_test_3.log
│   │   ├── test_dataset_test_1.log
│   │   ├── test_dataset_test_2.log
│   │   ├── train_translate_test_1.log
│   │   ├── train_translate_test_2.log
│   │   └── train_translate_test_3.log
│   └── translation
│       ├── dev_translation_logs.log
│       ├── skipped_batches.log
│       ├── test_translation_logs.log
│       ├── train_translation_logs_day_1.log
│       └── train_translation_logs_day_2.log
├── README.md
└── CITATION.cff
```

---

## 🌞 Dataset Details

| Property | Value |
|---|---|
| Language | Persian (Farsi) |
| Original Language | English |
| Total Records | ~54,000 |
| Training Set | 43,410 |
| Validation Set | 5,426 |
| Test Set | 5,427 |
| Number of Labels | 27 emotions + Neutral |
| Format | TSV (tab-separated) |
| Translation Model | Gap GPT API |

---

## 🧭 Dataset Structure

Each file contains three columns with **no header row**:

| Column | Content |
|---|---|
| Column 0 | Persian translated text |
| Column 1 | Emotion label(s) |
| Column 2 | UUID |

---

## 💻 How to Use

```
import pandas as pd

# Load splits
train = pd.read_csv("data/train.tsv", sep="\t", header=None,
                    names=["text", "labels", "id"])
dev   = pd.read_csv("data/dev.tsv",   sep="\t", header=None,
                    names=["text", "labels", "id"])
test  = pd.read_csv("data/test.tsv",  sep="\t", header=None,
                    names=["text", "labels", "id"])

print(train.head())
```

> [!NOTE]
> Labels are stored as comma-separated emotion names (e.g. `joy,admiration`).
> A single text can have multiple labels.

---

## 🌿 Emotion Categories

`admiration` `amusement` `anger` `annoyance` `approval` `caring` `confusion`
`curiosity` `desire` `disappointment` `disapproval` `disgust` `embarrassment`
`excitement` `fear` `gratitude` `grief` `joy` `love` `nervousness` `optimism`
`pride` `realization` `relief` `remorse` `sadness` `surprise` `neutral`

---

## ⚓ GoEmotions Label Codes (Official)

| ID | Emotion | ID | Emotion |
|---|---|---|---|
| 0 | admiration | 14 | fear |
| 1 | amusement | 15 | gratitude |
| 2 | anger | 16 | grief |
| 3 | annoyance | 17 | joy |
| 4 | approval | 18 | love |
| 5 | caring | 19 | nervousness |
| 6 | confusion | 20 | optimism |
| 7 | curiosity | 21 | pride |
| 8 | desire | 22 | realization |
| 9 | disappointment | 23 | relief |
| 10 | disapproval | 24 | remorse |
| 11 | disgust | 25 | sadness |
| 12 | embarrassment | 26 | surprise |
| 13 | excitement | 27 | neutral |

> [!NOTE]
> These are multi label indices, a single text can have multiple active labels.

---

## 🔨 Quality Assurance

The translation pipeline included:

- Automated audit tests (Persian script validation, missing translation detection, length ratio checks, duplicate detection)
- Manual review of a 500-row random sample
- Exception handling for untranslatable rows (URLs, special tokens)

---

## ⚠️ Limitations

- Translations were generated via the **GAP GPT API** and are **not human-verified** beyond the 500-row sample review.
- Some idiomatic Reddit expressions may not translate accurately into Persian.
- Inherited label noise from the original GoEmotions dataset applies.

---

## 🔔 Original Dataset

This dataset is based on:

> Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020).
> **GoEmotions: A Dataset of Fine-Grained Emotions.**
> *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL 2020).*
> [https://arxiv.org/abs/2005.00547](https://arxiv.org/abs/2005.00547)

Original dataset links:
- GitHub: [google-research/goemotions](https://github.com/google-research/google-research/tree/master/goemotions)
- Kaggle: [debarshichanda/goemotions](https://www.kaggle.com/datasets/debarshichanda/goemotions)

---

## 🫖 Citation

If you use this dataset in your research, please cite both the original GoEmotions paper and this dataset.

**This dataset:**
```
@dataset{ayda_khoshkan_2026,
	title={GoEmotion Persian},
	url={https://www.kaggle.com/dsv/16646751},
	DOI={10.34740/KAGGLE/DSV/16646751},
	publisher={Kaggle},
	author={Ayda Khoshkan},
	year={2026}
}
```

**Original GoEmotions paper:**
```
@inproceedings{demszky-etal-2020-goemotions,
  title     = {{G}o{E}motions: A Dataset of Fine-Grained Emotions},
  author    = {Demszky, Dorottya and Movshovitz-Attias, Dana and Ko, Jeongwook
               and Cowen, Alan and Nemade, Gaurav and Ravi, Sujith},
  booktitle = {Proceedings of the 58th Annual Meeting of the Association for
               Computational Linguistics},
  year      = {2020},
  url       = {https://arxiv.org/abs/2005.00547}
}
```

---

## 🪶 License
This dataset is released under **[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)** and **Apache 2.0**.
The original GoEmotions dataset is licensed under **[CC0](https://creativecommons.org/publicdomain/zero/1.0/)** and **Apache 2.0** by Google Research.
