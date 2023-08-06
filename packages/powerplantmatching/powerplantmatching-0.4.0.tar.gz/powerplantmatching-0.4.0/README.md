# powerplantmatching
A toolset for cleaning, standardizing and combining multiple power
plant databases.

This package provides ready-to-use power plant data for the European power system.
Starting from openly available power plant datasets, the package cleans, standardizes
and merges the input data to create a new combining dataset, which includes all the important information.
The package allows to easily update the combined data as soon as new input datasets are released.

![Map of power plants in Europe](https://user-images.githubusercontent.com/19226431/46086361-36a13080-c1a8-11e8-82ed-9f04167273e5.png)

powerplantmatching was initially developed by the
[Renewable Energy Group](https://fias.uni-frankfurt.de/physics/schramm/complex-renewable-energy-networks/)
at [FIAS](https://fias.uni-frankfurt.de/) to build power plant data
inputs to [PyPSA](http://www.pypsa.org/)-based models for carrying
out simulations for the [CoNDyNet project](http://condynet.de/),
financed by the
[German Federal Ministry for Education and Research (BMBF)](https://www.bmbf.de/en/)
as part of the
[Stromnetze Research Initiative](http://forschung-stromnetze.info/projekte/grundlagen-und-konzepte-fuer-effiziente-dezentrale-stromnetze/).


### **Warning (Nov 27 2018) - no more python2 support**

Future commits of powerplantmatching will no longer support python2. The code will probably still work in most of the cases, however please consider updating your conda environment (if installed via conda) or moving to python 3 if installed with pip only. 



### What it can do

- clean and standardize power plant data sets
- aggregate power plants units which belong to the same plant
- compare and combine different data sets
- create lookups and give statistical insight to power plant goodness
- provide cleaned data from different sources
- choose between gros/net capacity
- provide an already merged data set of six different data-sources

## Processed Data

If you are only interested in the power plant data, we provide our
current merged dataset for European power plants as a
[csv-file](https://media.githubusercontent.com/media/FRESNA/powerplantmatching/master/data/out/default/powerplants.csv). This
set combines the data of all the data sources listed in
[Data-Sources](#Data-Sources) and provides the following information:

- **Power plant name**      - claim of each database
- **Fueltype**          - {Bioenergy, Geothermal, Hard Coal, Hydro, Lignite, Nuclear, Natural Gas, Oil, Solar, Wind, Other}
- **Technology**		- {CCGT, OCGT, Steam Turbine, Combustion Engine, Run-Of-River, Pumped Storage, Reservoir}
- **Set**			- {Power Plant (PP), Combined Heat and Power (CHP), Storages (Stores)}
- **Capacity**			- \[MW\]
- **Geo-position**		- Latitude, Longitude
- **Country**           - EU-27 + CH + NO (+ UK) minus Cyprus and Malta
- **YearCommissioned**		- Commmisioning year of the powerplant
- **RetroFit**        - Year of last retrofit 
- **File**			- Source file of the data entry
- **projectID**			- Immutable identifier of the power plant


The current release together with the open version (without ESE dataset) of the processed data is stored on Zenodo: 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1889465.svg)](https://doi.org/10.5281/zenodo.1889465)

In order include all datasources, please install the package and recompile the full matched data.

The following picture compares the total capacities per fuel type
between the different data sources and the resulting dataset

![Total capacities per fuel type for the different data sources and the merged dataset.](https://user-images.githubusercontent.com/19226431/43489219-8a7506d6-951c-11e8-85dd-d772d1c76181.png)

Comparing the aggregated capacities per country and fuel type with the capacity statistics provided by the ENTSOE:

![Capacity statistics comparison](https://user-images.githubusercontent.com/19226431/44577090-77b0ba00-a790-11e8-9575-30a7868222fa.png)


## Installation

1. Make sure that [git lfs](https://git-lfs.github.com/) is installed, in case of doubt just run `git lfs install`
2. Copy or clone the repository to a directory of your choosing /path/to/powerplantmatching
   ```shell
   cd /path/to
   git clone https://github.com/FRESNA/powerplantmatching.git
   ```
3. If you use conda (if not skip this step), install the requirements from requirements.yaml into a new environment powerplantmatching and activate it.
   ```shell
   conda env create -f powerplantmatching/requirements.yaml
   source activate powerplantmatching
   ```
3. Install the package using `pip`
   ```shell
   pip install -e ./powerplantmatching'
   ```
4. Copy config_example.yaml to config.yaml.

Optional but recommended:resulting 
 

5. Download the [ESE dataset](https://goo.gl/gVMwKJ) and store it under `/path/to/powerplantmatching/data/in/projects.xls`.
6. Add your ENTSOE security token to the config.yaml file. The token can be obtained by following section 2 of the [RESTful API documentation](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_authentication_and_authorisation) of the ENTSOE-E Transparency platform.

Optional: 

7. Add your Google API key to the config.yaml file to enable geoparsing. The key can be obtained by following the [instructions](https://developers.google.com/maps/documentation/geocoding/get-api-key). 


Once set up the package, the full database is available through the python command
```python
import powerplantmatching as pm
pm.collection.matched_data()
```
Note, that for the compilation this will take its time (about 30 min for the standard data sources.) 

## Make your own configuration

You have the option to easily manipulate the resulting data. Through the   **config.yaml** file you can 

- determine the global set of **countries** and **fueltypes**

- determine which data sources to combine and which data sources should completely be contained in the final dataset

- individually filter data sources via a [pandas.DataFrame.query](http://pandas.pydata.org/pandas-docs/stable/indexing.html#the-query-method) statement set as an argument of data source name in your config.yaml (see [config_example.yaml](https://github.com/FRESNA/powerplantmatching/blob/master/config_example.yaml)).    

The [config_example.yaml](https://github.com/FRESNA/powerplantmatching/blob/master/config_example.yaml) provides an adjusted configuration for an european dataset.  
Further you can 

- scale the power plant capacities in order to match country specific statistics about total power plant capacities

- trace back which original data flew into the resulting data.   

- visualize the data

- export your powerplant data to a [PyPSA](https://github.com/PyPSA/PyPSA) or [TIMES](https://iea-etsap.org/index.php/etsap-tools/model-generators/times) model 


There is a (bit out of date) [Documentation](https://github.com/FRESNA/powerplantmatching/files/1380529/PowerplantmatchingDoc.pdf) available, which (however) gives you some more extensive insight
on the coding level.




## Data-Sources:

- OPSD - [Open Power System Data](http://data.open-power-system-data.org/) publish their [data](http://data.open-power-system-data.org/conventional_power_plants/) under a free license
- GEO - [Global Energy Observatory](http://globalenergyobservatory.org/), the data is not directly available on the website, but can be obtained from an [sqlite scraper](https://morph.io/coroa/global_energy_observatory_power_plants)
- GPD - [Global Power Plant Database](http://datasets.wri.org/dataset/globalpowerplantdatabase) provide their data under a free license
- CARMA - [Carbon Monitoring for Action](http://carma.org/plant)
- ESE - [Energy Storage Exchange](http://www.energystorageexchange.org/) provide a database for storage units. Especially the hydro storage data is of big use for a combining power plant database. Since the data is not free, it is optional and can be [downloaded separately](http://www.energystorageexchange.org/projects/advanced_search?utf8=%E2%9C%93&name_eq=&country_sort_eq%5B%5D=Austria&country_sort_eq%5B%5D=Belgium&country_sort_eq%5B%5D=Bulgaria&country_sort_eq%5B%5D=Croatia&country_sort_eq%5B%5D=Czeck+Republic&country_sort_eq%5B%5D=Denmark&country_sort_eq%5B%5D=Estonia&country_sort_eq%5B%5D=Finland&country_sort_eq%5B%5D=France&country_sort_eq%5B%5D=Germany&country_sort_eq%5B%5D=Greece&country_sort_eq%5B%5D=Hungary&country_sort_eq%5B%5D=Ireland&country_sort_eq%5B%5D=Italy&country_sort_eq%5B%5D=Latvia&country_sort_eq%5B%5D=Lithuania&country_sort_eq%5B%5D=Luxembourg&country_sort_eq%5B%5D=Netherlands&country_sort_eq%5B%5D=Norway&country_sort_eq%5B%5D=Poland&country_sort_eq%5B%5D=Portugal&country_sort_eq%5B%5D=Romainia&country_sort_eq%5B%5D=Slovakia&country_sort_eq%5B%5D=Slovenia&country_sort_eq%5B%5D=Spain&country_sort_eq%5B%5D=Sweden&country_sort_eq%5B%5D=Switzerland&country_sort_eq%5B%5D=United+Kingdom&size_kw_ll=&size_kw_ul=&kW=&size_kwh_ll=&size_kwh_ul=&kWh=&%5Bannouncement_on_ll%281i%29%5D=&%5Bannouncement_on_ll%282i%29%5D=&%5Bannouncement_on_ll%283i%29%5D=1&%5Bannouncement_on_ul%281i%29%5D=&%5Bannouncement_on_ul%282i%29%5D=&%5Bannouncement_on_ul%283i%29%5D=1&%5Bconstruction_on_ll%281i%29%5D=&%5Bconstruction_on_ll%282i%29%5D=&%5Bconstruction_on_ll%283i%29%5D=1&%5Bconstruction_on_ul%281i%29%5D=&%5Bconstruction_on_ul%282i%29%5D=&%5Bconstruction_on_ul%283i%29%5D=1&%5Bcommissioning_on_ll%281i%29%5D=&%5Bcommissioning_on_ll%282i%29%5D=&%5Bcommissioning_on_ll%283i%29%5D=1&%5Bcommissioning_on_ul%281i%29%5D=&%5Bcommissioning_on_ul%282i%29%5D=&%5Bcommissioning_on_ul%283i%29%5D=1&%5Bdecommissioning_on_ll%281i%29%5D=&%5Bdecommissioning_on_ll%282i%29%5D=&%5Bdecommissioning_on_ll%283i%29%5D=1&%5Bdecommissioning_on_ul%281i%29%5D=&%5Bdecommissioning_on_ul%282i%29%5D=&%5Bdecommissioning_on_ul%283i%29%5D=1&owner_in=&vendor_company=&electronics_provider=&utility=&om_contractor=&developer=&order_by=&sort_order=&search_page=&search_search=search).
- ENTSOe - [European Network of Transmission System Operators for Electricity](http://entsoe.eu/), annually provides statistics about aggregated power plant capacities. Their data can be used as a validation reference. We further use their [annual energy generation report from 2010](https://www.entsoe.eu/db-query/miscellaneous/net-generating-capacity) as an input for the hydro power plant classification. The [power plant dataset](https://transparency.entsoe.eu/generation/r2/installedCapacityPerProductionUnit/show) on the ENTSO-E transparency website is downloaded using the [ENTSO-E Transparency API](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html).
- IRENA - [International Renewable Energy Agency](http://resourceirena.irena.org/gateway/dashboard/) open available statistics on power plant capacities.
- BNETZA - [Bundesnetzagentur](https://www.bundesnetzagentur.de/EN/Areas/Energy/Companies/SecurityOfSupply/GeneratingCapacity/PowerPlantList/PubliPowerPlantList_node.html) open available data source for Germany's power plants


The merged dataset is available in two versions: The [bigger dataset](https://media.githubusercontent.com/media/FRESNA/powerplantmatching/master/data/out/default/powerplants_large.csv)
links the entries of the matched power plants and lists all the related
properties given by the different data-sources. The [smaller, reduced dataset](https://media.githubusercontent.com/media/FRESNA/powerplantmatching/master/data/out/default/powerplants.csv)
claims only the value of the most reliable data source being matched in the individual power plant data entry.
The considered reliability scores are:


| Dataset          | Reliabilty score |
| :--------------- | :--------------- |
| BNETZA           |                5 |
| CARMA            |                1 |
| ENTSOE           |                4 |
| ESE              |                4 |
| GEO              |                3 |
| IWPDCY           |                3 |
| OPSD             |                5 |
| UBA              |                5 |
| GPD              |                3 |



## Getting Started

A small presentation of the tool is given in the [jupyter notebook](https://github.com/FRESNA/powerplantmatching/blob/master/Example%20of%20Use.ipynb) 

## Module Structure

The package consists of ten modules. For creating a new dataset you
can make most use of the modules data, clean and match, which provide
you with function for data supply, vertical cleaning and horizontal
matching, respectively.

![Modular package structure](https://user-images.githubusercontent.com/19226431/31513014-2feef76e-af8d-11e7-9b4d-f1be929e2dba.png)

## How it works

Whereas single databases as the CARMA, GEO or the OPSD database provide non standardized and incomplete information, the datasets can complement each other and improve their reliability. 
In a first step, powerplantmatching converts all powerplant dataset into a standardized format with a defined set of columns and values. The second part consists of aggregating power plant blocks together into units. Since some of the datasources provide their powerplant records on unit level, without detailed information about lower-level blocks, comparing with other sources is only possible on unit level. In the third and name-giving step the tool combines (or matches)different, standardized and aggregated input sources keeping only powerplants units which appear in more than one source. The matched data afterwards is complemented by data entries of reliable sources which have not matched.  

The aggregation and matching process heavily relies on
[DUKE](https://github.com/larsga/Duke), a java application specialized
for deduplicating and linking data. It provides many built-in
comparators such as numerical, string or geoposition comparators.  The
engine does a detailed comparison for each single argument (power
plant name, fuel-type etc.) using adjusted comparators and weights.
From the individual scores for each column it computes a compound
score for the likeliness that the two powerplant records refer to the
same powerplant. If the score exceeds a given threshold, the two
records of the power plant are linked and merged into one data set.

Let's make that a bit more concrete by giving a quick
example. Consider the following two data sets

### Dataset 1:

|    | Name                | Fueltype   |   Classification | Country        |   Capacity |     lat |        lon |   File |
|---:|:--------------------|:-----------|-----------------:|:---------------|-----------:|--------:|-----------:|-------:|
|  0 | Aarberg             | Hydro      |              nan | Switzerland    |     14.609 | 47.0444 |  7.27578   |    nan |
|  1 | Abbey mills pumping | Oil        |              nan | United Kingdom |      6.4   | 51.687  | -0.0042057 |    nan |
|  2 | Abertay             | Other      |              nan | United Kingdom |      8     | 57.1785 | -2.18679   |    nan |
|  3 | Aberthaw            | Coal       |              nan | United Kingdom |   1552.5   | 51.3875 | -3.40675   |    nan |
|  4 | Ablass              | Wind       |              nan | Germany        |     18     | 51.2333 | 12.95      |    nan |
|  5 | Abono               | Coal       |              nan | Spain          |    921.7   | 43.5588 | -5.72287   |    nan |

and

### Dataset 2:

|    | Name              | Fueltype    | Classification   | Country        |   Capacity |     lat |     lon |   File |
|---:|:------------------|:------------|:-----------------|:---------------|-----------:|--------:|--------:|-------:|
|  0 | Aarberg           | Hydro       | nan              | Switzerland    |       15.5 | 47.0378 |  7.272  |    nan |
|  1 | Aberthaw          | Coal        | Thermal          | United Kingdom |     1500   | 51.3873 | -3.4049 |    nan |
|  2 | Abono             | Coal        | Thermal          | Spain          |      921.7 | 43.5528 | -5.7231 |    nan |
|  3 | Abwinden asten    | Hydro       | nan              | Austria        |      168   | 48.248  | 14.4305 |    nan |
|  4 | Aceca             | Oil         | CHP              | Spain          |      629   | 39.941  | -3.8569 |    nan |
|  5 | Aceca fenosa      | Natural Gas | CCGT             | Spain          |      400   | 39.9427 | -3.8548 |    nan |

where Dataset 2 has the higher reliability score. Apparently entries 0, 3 and 5 of Dataset 1 relate to the same
power plants as the entries 0,1 and 2 of Dataset 2. The toolset detects those similarities and combines them into the following set, but prioritising the values of Dataset 2:

|  | Name   | Country        | Fueltype   | Classification   |   Capacity |     lat |      lon |   File |
|---:|:------------|:---------------|:-----------|:-----------------|-----------:|--------:|---------:|-------:|
|  0 | Aarberg    | Switzerland    | Hydro      | nan              |       15.5 | 47.0378 |  7.272 |    nan |
|  1 | Aberthaw       | United Kingdom | Coal       | Thermal          |     1500 | 51.3873 | -3.4049 |    nan |
|  2 | Abono             | Spain          | Coal       | Thermal          |      921.7 | 43.5528 | -5.7231 |    nan |


## Citing powerplantmatching

If you want to cite powerplantmatching, use the following paper


- F. Gotzens, H. Heinrichs, J. Hörsch, and F. Hofmann, [Performing energy modelling exercises in a transparent way - The issue of data quality in power plant databases](https://www.sciencedirect.com/science/article/pii/S2211467X18301056?dgcid=author), Energy Strategy Reviews, vol. 23, pp. 1–12, Jan. 2019.

with bibtex


```
@article{gotzens_performing_2019,
	title = {Performing energy modelling exercises in a transparent way - {The} issue of data quality in power plant databases},
	volume = {23},
	issn = {2211467X},
	url = {https://linkinghub.elsevier.com/retrieve/pii/S2211467X18301056},
	doi = {10.1016/j.esr.2018.11.004},
	language = {en},
	urldate = {2018-12-03},
	journal = {Energy Strategy Reviews},
	author = {Gotzens, Fabian and Heinrichs, Heidi and Hörsch, Jonas and Hofmann, Fabian},
	month = jan,
	year = {2019},
	pages = {1--12}
}
```


and/or the current release stored on Zenodo with a release-specific DOI:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1889465.svg)](https://doi.org/10.5281/zenodo.1889465)



## Acknowledgements

The development of powerplantmatching was helped considerably by
in-depth discussions and exchanges of ideas and code with

- Tom Brown from Karlsruhe Institute for Technology
- Chris Davis from University of Groningen and
- Johannes Friedrich, Roman Hennig and Colin McCormick of the World Resources Institute

## Licence

Copyright 2018-2020 Fabian Gotzens (FZ Jülich), Jonas Hörsch (KIT), Fabian Hofmann (FIAS)



powerplantmatching is released as free software under the
[GPLv3](http://www.gnu.org/licenses/gpl-3.0.en.html), see
[LICENSE](LICENSE) for further information.
