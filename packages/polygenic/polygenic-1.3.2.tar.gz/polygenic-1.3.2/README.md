# polygenic

[![PyPI](https://img.shields.io/pypi/v/polygenic.svg)](https://pypi.python.org/pypi/polygenic)
[//]: # ![CI](https://github.com/polygenic/polygenic/workflows/CI/badge.svg)
[//]: # [![readthedocs](https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat)](https://polygenic.readthedocs.io/en/latest/?badge=latest)
[//]: # [![License](https://img.shields.io/badge/license-LGPL-blue.svg)](https://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License)
[//]: # [![Slack](https://img.shields.io/badge/Slack%20channel-%20%20-blue.svg)](https://join.slack.com/t/pygithub-project/shared_invite/zt-duj89xtx-uKFZtgAg209o6Vweqm8xeQ)
[//]: # [![Open Source Helpers](https://www.codetriage.com/pygithub/pygithub/badges/users.svg)](https://www.codetriage.com/pygithub/pygithub)
[//]: # [![codecov](https://codecov.io/gh/PyGithub/PyGithub/branch/master/graph/badge.svg)](https://codecov.io/gh/PyGithub/PyGithub)
[//]: # [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

python package for computation of polygenic scores based for particular sample

## How to install
```
pip3 install --upgrade polygenic==1.3.1
```

## How to run
```
polygenic --vcf [your_vcf_gz] --model [your_model]
```

## Building models
Models are pure python scripts tha use "sequencing query languange" called seqql.  
It is required to import language elements.
```
from polygenic.lib.model.seqql import PolygenicRiskScore
from polygenic.lib.model.seqql import ModelData
from polygenic.lib.model.category import QuantitativeCategory
```

It recommended to add variable pointing population for which score was prepared
```
trait_was_prepared_for_population = "eas"
```
The list of accepted population identifiers:
- `nfe` - Non-Finnish European ancestry
- `eas` - East Asian ancestry
- `afr` - African-American/African ancestry
- `amr` - Latino ancestry
- `asj` - Ashkenazi Jewish ancestry,
- `fin` - Finnish ancestry
- `oth` - Other ancestry

The most important part of model is model itself. Currently it is possible to use PolygenicRiskScore
```
model = PolygenicRiskScore(categories = ..., snps_and_coeffcients = ..., model_type = ...)
```

categories is a list of QuantitaveCategories
```QuantitativeCategory(from_=1.371624087, to=2.581880425, category_name='High risk')```
## Example model
```
from polygenic.lib.model.seqql import PolygenicRiskScore
from polygenic.lib.model.seqql import ModelData
from polygenic.lib.model.category import QuantitativeCategory

trait_was_prepared_for_population = "eas"

model = PolygenicRiskScore(
    categories=[
        QuantitativeCategory(from_=1.371624087, to=2.581880425, category_name='High risk'),
        QuantitativeCategory(from_=1.169616034, to=1.371624087, category_name='Potential risk'),
        QuantitativeCategory(from_=-0.346748358, to=1.169616034, category_name='Average risk'),
	    QuantitativeCategory(from_=-1.657132197, to=-0.346748358, category_name='Low risk')
    ],
    snips_and_coefficients={
	'rs10012': ModelData(effect_allele='G', coeff_value=0.369215857410143),
	'rs1014971': ModelData(effect_allele='T', coeff_value=0.075546961392531),
	'rs10936599': ModelData(effect_allele='C', coeff_value=0.086359830674748),
	'rs11892031': ModelData(effect_allele='C', coeff_value=-0.552841968657781),
	'rs1495741': ModelData(effect_allele='A', coeff_value=0.05307844348342),
	'rs17674580': ModelData(effect_allele='C', coeff_value=0.187520720836463),
	'rs2294008': ModelData(effect_allele='T', coeff_value=0.08278537031645),
	'rs798766': ModelData(effect_allele='T', coeff_value=0.093421685162235),
	'rs9642880': ModelData(effect_allele='G', coeff_value=0.093421685162235)
    },
    model_type='beta'
)
```