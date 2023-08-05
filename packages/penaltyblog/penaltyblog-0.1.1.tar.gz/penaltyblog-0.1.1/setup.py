# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['penaltyblog',
 'penaltyblog.clubelo',
 'penaltyblog.footballdata',
 'penaltyblog.implied',
 'penaltyblog.poisson']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.2', 'pandas>=1.1.3', 'scipy>=1.5.0']

setup_kwargs = {
    'name': 'penaltyblog',
    'version': '0.1.1',
    'description': 'Library from http://pena.lt/y/blog for modelling and working with football (soccer) data',
    'long_description': '# Penalty Blog\n\nThe `penaltyblog` package contains code from [http://pena.lt/y/blog](http://pena.lt/y/blog) for working with football (soccer) data.\n\n## Installation\n\n`pip install penaltyblog`\n\n\n## Example\n\nThere are examples of all the functions available in the [Examples section](https://github.com/martineastwood/penaltyblog/tree/master/examples).\n\n## Download Data from football-data.co.uk\n\n`penaltyblog` contains some helper functions for downloading data from [football-data.co.uk](http://football-data.co.uk).\n\n\n### List the countries available \n\n```python\nimport penaltyblog as pb\npd.footballdata.list_countries()\n```\n\n```\n[\'belgium\',\n \'england\',\n \'france\',\n \'germany\',\n \'greece\',\n \'italy\',\n \'portugal\',\n \'scotland\',\n \'spain\',\n \'turkey\']\n```\n\n### Fetch the data\n\nThe first parameter is the country of interest, the second is the starting year of the season and the third paramater is the level of the division of interest, where `0` is the highest division (e.g. England\'s Premier League), `1` is the second highest (e.g. England\'s Championship) etc.\n\n```python\ndf = pb.footballdata.fetch_data("england", 2018, 0)\ndf[["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"]].head()\n```\n\n|    | Date                | HomeTeam     | AwayTeam       |   FTHG |   FTAG |\n|---:|:--------------------|:-------------|:---------------|-------:|-------:|\n|  0 | 2018-08-10 00:00:00 | Man United   | Leicester      |      2 |      1 |\n|  1 | 2018-08-11 00:00:00 | Bournemouth  | Cardiff        |      2 |      0 |\n|  2 | 2018-08-11 00:00:00 | Fulham       | Crystal Palace |      0 |      2 |\n|  3 | 2018-08-11 00:00:00 | Huddersfield | Chelsea        |      0 |      3 |\n|  4 | 2018-08-11 00:00:00 | Newcastle    | Tottenham      |      1 |      2 |\n\n## Predicting Goals\n\n`penaltyblog` contains models designed for predicting the number of goals scored in football (soccer) games. Although aimed at football (soccer), they may also be useful for other sports, such as hockey.\n\n### The Basic Poisson Model\n\nLet\'s start off by downloading some example scores from the awesome [football-data](http://football-data.co.uk) website.\n\n```python\nimport penaltyblog as pb\ndf = pb.footballdata.fetch_data("England", 2018, 0)\ndf[["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"]].head()\n```\n\n|    | Date                | HomeTeam     | AwayTeam       |   FTHG |   FTAG |\n|---:|:--------------------|:-------------|:---------------|-------:|-------:|\n|  0 | 2018-08-10 00:00:00 | Man United   | Leicester      |      2 |      1 |\n|  1 | 2018-08-11 00:00:00 | Bournemouth  | Cardiff        |      2 |      0 |\n|  2 | 2018-08-11 00:00:00 | Fulham       | Crystal Palace |      0 |      2 |\n|  3 | 2018-08-11 00:00:00 | Huddersfield | Chelsea        |      0 |      3 |\n|  4 | 2018-08-11 00:00:00 | Newcastle    | Tottenham      |      1 |      2 |\n\nNext, we create a basic Poisson model and fit it to the data.\n\n```python\npois = pb.PoissonGoalsModel(\n    df["FTHG"], df["FTAG"], df["HomeTeam"], df["AwayTeam"])\npois.fit()\n```\n\nLet\'s take a look at the fitted parameters.\n\n```python\npois\n```\n\n```\nModule: Penaltyblog\n\nModel: Poisson\n\nNumber of parameters: 42\nLog Likelihood: -1065.077\nAIC: 2214.154\n\nTeam                 Attack               Defence             \n------------------------------------------------------------\nArsenal              1.362                -1.062              \nBournemouth          1.115                -0.761              \nBrighton             0.634                -0.937              \nBurnley              0.894                -0.801              \nCardiff              0.614                -0.798              \nChelsea              1.202                -1.341              \nCrystal Palace       1.004                -1.045              \nEverton              1.055                -1.184              \nFulham               0.626                -0.637              \nHuddersfield         0.184                -0.712              \nLeicester            0.999                -1.145              \nLiverpool            1.532                -1.889              \nMan City             1.598                -1.839              \nMan United           1.249                -1.013              \nNewcastle            0.805                -1.153              \nSouthampton          0.891                -0.846              \nTottenham            1.264                -1.337              \nWatford              1.03                 -0.937              \nWest Ham             1.026                -1.007              \nWolves               0.916                -1.191              \n------------------------------------------------------------\nHome Advantage: 0.225\nIntercept: 0.206\n```\n\n### The Dixon and Coles Adjustment\n\nThe basic Poisson model struggles somewhat with the probabilities for low scoring games. Dixon and Coles (1997) added in an adjustment factor (rho) that modifies the probabilities for 0-0, 1-0 and 0-1 scorelines to account for this.\n\n```python\ndc = pb.DixonColesGoalModel(\n    df["FTHG"], df["FTAG"], df["HomeTeam"], df["AwayTeam"])\ndc.fit()\ndc\n```\n\n```\nModule: Penaltyblog\n\nModel: Dixon and Coles\n\nNumber of parameters: 43\nLog Likelihood: -1064.943\nAIC: 2215.886\n\nTeam                 Attack               Defence             \n------------------------------------------------------------\nArsenal              1.36                 -0.982              \nBournemouth          1.115                -0.679              \nBrighton             0.632                -0.858              \nBurnley              0.897                -0.717              \nCardiff              0.615                -0.715              \nChelsea              1.205                -1.254              \nCrystal Palace       1.007                -0.961              \nEverton              1.054                -1.102              \nFulham               0.625                -0.557              \nHuddersfield         0.18                 -0.631              \nLeicester            0.996                -1.064              \nLiverpool            1.534                -1.803              \nMan City             1.599                -1.762              \nMan United           1.251                -0.931              \nNewcastle            0.806                -1.07               \nSouthampton          0.897                -0.761              \nTottenham            1.259                -1.261              \nWatford              1.031                -0.854              \nWest Ham             1.023                -0.927              \nWolves               0.914                -1.113              \n------------------------------------------------------------\nHome Advantage: 0.225\nIntercept: 0.124\nRho: -0.041\n```\n\n\n### The Rue and Salvesen Adjustment\n\nRue and Salvesen (1999) added in an additional psycological effect factor (gamma) where Team A will under-estimate Team B if Team A is stronger than team B. They also truncate scorelines to a maximum of five goals, e.g. a score of 7-3 becomes 5-3, stating that any goals above 5 are non-informative.\n\n```python\nrs = pb.RueSalvesenGoalModel(\n    df["FTHG"], df["FTAG"], df["HomeTeam"], df["AwayTeam"])\n\nrs.fit()\nrs\n```\n\n```\nModule: Penaltyblog\n\nModel: Rue Salvesen\n\nNumber of parameters: 44\nLog Likelihood: -1061.167\nAIC: 2210.334\n\nTeam                 Attack               Defence             \n------------------------------------------------------------\nArsenal              1.435                -1.068              \nBournemouth          1.2                  -0.776              \nBrighton             0.594                -0.831              \nBurnley              0.935                -0.766              \nCardiff              0.6                  -0.712              \nChelsea              1.194                -1.281              \nCrystal Palace       1.019                -0.985              \nEverton              1.044                -1.126              \nFulham               0.641                -0.585              \nHuddersfield         0.096                -0.573              \nLeicester            0.988                -1.067              \nLiverpool            1.487                -1.768              \nMan City             1.533                -1.743              \nMan United           1.315                -1.006              \nNewcastle            0.761                -1.036              \nSouthampton          0.921                -0.814              \nTottenham            1.244                -1.274              \nWatford              1.067                -0.902              \nWest Ham             1.045                -0.961              \nWolves               0.881                -1.091              \n------------------------------------------------------------\nHome Advantage: 0.222\nIntercept: 0.141\nRho: -0.04\nGamma: 0.373\n```\n\n\n### Making Predictions\n\nTo make a prediction using any of the above models, just pass the name of the home and away teams to the `predict` function. This returns the `FootballProbabilityGrid` class that can convert the output from the model into probabilities for various betting markets.\n\n```python\nprobs = my_model.predict("Liverpool", "Stoke")\n```\n\n### Home / Draw / Away\n\n```python\n# also known as 1x2\nprobs.home_draw_away\n```\n\n```\n[0.5193995875820345, 0.3170596913687951, 0.1635407210315597]\n```\n\n### Total Goals\n\n```python\nprobs.total_goals("over", 2.5)\n```\n\n```\n0.31911650768322447\n```\n\n```python\nprobs.total_goals("under", 2.5)\n```\n\n```\n0.680883492299145\n```\n\n### Asian Handicaps\n\n```python\nprobs.asian_handicap("home", 1.5)\n```\n\n```\n0.2602616248461783\n```\n\n```python\nprobs.asian_handicap("away", -1.5)\n```\n\n```\n0.7397383751361912\n```\n\n### Model Parameters\n\nYou can access the model\'s parameters via the `get_params` function.\n\n```python\nfrom pprint import pprint\nparams = my_model.get_params()\npprint(params)\n```\n\n```\n{\'attack_Arsenal\': 1.3650671020694474,\n \'attack_Aston Villa\': 0.6807140182913024,\n \'attack_Blackburn\': 0.971135574781119,\n \'attack_Bolton\': 0.9502712140456423,\n \'attack_Chelsea\': 1.235466344414206,\n \'attack_Everton\': 0.9257685468926837,\n \'attack_Fulham\': 0.9122902202053228,\n \'attack_Liverpool\': 0.8684673939949753,\n \'attack_Man City\': 1.543379586931267,\n \'attack_Man United\': 1.4968564161865994,\n \'attack_Newcastle\': 1.1095636706231062,\n \'attack_Norwich\': 1.0424304866584615,\n \'attack_QPR\': 0.827439335780754,\n \'attack_Stoke\': 0.6248927873330669,\n \'attack_Sunderland\': 0.8510292333101492,\n \'attack_Swansea\': 0.8471368133406263,\n \'attack_Tottenham\': 1.2496040004504756,\n \'attack_West Brom\': 0.8625207332372105,\n \'attack_Wigan\': 0.8177807129177644,\n \'attack_Wolves\': 0.8181858085358248,\n \'defence_Arsenal\': -1.2192247076852236,\n \'defence_Aston Villa\': -1.0566859588325535,\n \'defence_Blackburn\': -0.7430288162188969,\n \'defence_Bolton\': -0.7268011436918458,\n \'defence_Chelsea\': -1.2065700516830344,\n \'defence_Everton\': -1.3564763976122773,\n \'defence_Fulham\': -1.1159544166204092,\n \'defence_Liverpool\': -1.3293118049518535,\n \'defence_Man City\': -1.6549894606952225,\n \'defence_Man United\': -1.5728126940204685,\n \'defence_Newcastle\': -1.1186158411320268,\n \'defence_Norwich\': -0.8865413401238464,\n \'defence_QPR\': -0.9124617361500764,\n \'defence_Stoke\': -1.0766419199030601,\n \'defence_Sunderland\': -1.2049421203955355,\n \'defence_Swansea\': -1.1077243368907703,\n \'defence_Tottenham\': -1.3160823704397775,\n \'defence_West Brom\': -1.1014569193066301,\n \'defence_Wigan\': -0.932997180492951,\n \'defence_Wolves\': -0.6618461794219439,\n \'home_advantage\': 0.2655860528422758,\n \'intercept\': 0.23467961435272489,\n \'rho\': -0.1375912978446625,\n \'rue_salvesen\': 0.1401430558820631}\n```\n\n## Implied Probabilities\n\nRemoves the overround and gets the implied probabilities from odds via a variety of methods\n\n### Multiplicative\n\nNormalizes the probabilites so they sum to 1.0 by dividing the inverse of the odds by the sum of the inverse of the odds\n\n```python\nimport penaltyblog as pb\n\nodds = [2.7, 2.3, 4.4]\npb.implied.multiplicative(odds)\n```\n\n```python\n{\'implied_probabilities\': array([0.35873804, 0.42112726, 0.2201347 ]),\n \'margin\': 0.03242570633874986,\n \'method\': \'multiplicative\'}\n```\n\n### Additive\n\nNormalizes the probabilites so they sum to 1.0 by removing an equal amount from each\n\n```python\nimport penaltyblog as pb\n\nodds = [2.7, 2.3, 4.4]\npb.implied.additive(odds)\n```\n\n```python\n{\'implied_probabilities\': array([0.3595618 , 0.42397404, 0.21646416]),\n \'margin\': 0.03242570633874986,\n \'method\': \'additive\'}\n```\n\n### Power\n\nSolves for the power coefficient that normalizes the inverse of the odds to sum to 1.0\n\n```python\nimport penaltyblog as pb\n\nodds = [2.7, 2.3, 4.4]\npb.implied.power(odds)\n```\n\n```python\n{\'implied_probabilities\': array([0.3591711 , 0.42373075, 0.21709815]),\n \'margin\': 0.03242570633874986,\n \'method\': \'power\',\n \'k\': 1.0309132393169356}\n ```\n\n### Shin\n\nUses the Shin (1992, 1993) method to calculate the implied probabilities\n\n```python\nimport penaltyblog as pb\n\nodds = [2.7, 2.3, 4.4]\npb.implied.shin(odds)\n```\n\n```python\n{\'implied_probabilities\': array([0.35934392, 0.42324385, 0.21741223]),\n \'margin\': 0.03242570633874986,\n \'method\': \'shin\',\n \'z\': 0.016236442857291165}\n ```\n\n### Differential Margin Weighting\n\nUses the differential margin approach described by Joesph Buchdahl in his `wisdom of the crowds` article\n\n```python\nimport penaltyblog as pb\n\nodds = [2.7, 2.3, 4.4]\npb.implied.differential_margin_weighting(odds)\n```\n\n```python\n{\'implied_probabilities\': array([0.3595618 , 0.42397404, 0.21646416]),\n \'margin\': 0.03242570633874986,\n \'method\': \'differential_margin_weighting\'}\n ```\n\n### Odds Ratio\n\nUses Keith Cheung\'s odds ratio approach, as discussed by Joesph Buchdahl\'s in his `wisdom of the crowds` article, to calculate the implied probabilities\n\n```python\nimport penaltyblog as pb\n\nodds = [2.7, 2.3, 4.4]\npb.implied.odds_ratio(odds)\n```\n\n```python\n{\'implied_probabilities\': array([0.35881036, 0.42256142, 0.21862822]),\n \'margin\': 0.03242570633874986,\n \'method\': \'odds_ratio\',\n \'c\': 1.05116912729218}\n ```\n\n## Rank Probability Scores\n\nBased on Constantinou and Fenton (2021), `penaltyblog` contains a function for calculating Rank Probability Scores for assessing home, draw, away probability forecasts.\n\n`predictions` is a list of home, draw, away probabilities and `observed` is the zero-based index for which outcome actually occurred.\n\n```python\nimport penaltyblog as pb\n\npredictions = [\n    [1, 0, 0],\n    [0.9, 0.1, 0],\n    [0.8, 0.1, 0.1],\n    [0.5, 0.25, 0.25],\n    [0.35, 0.3, 0.35],\n    [0.6, 0.3, 0.1],\n    [0.6, 0.25, 0.15],\n    [0.6, 0.15, 0.25],\n    [0.57, 0.33, 0.1],\n    [0.6, 0.2, 0.2],\n]\n\nobserved = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]\n\nfor p, o in zip(predictions, observed):\n    rps = pb.rps(p, o)\n    print(round(rps, 4))\n```\n\n```\n0.0\n0.005\n0.025\n0.1562\n0.1225\n0.185\n0.0913\n0.1113\n0.0975\n0.1\n```\n\n## Download ELO rating from clubelo.com\n\n### Download ELO ratings for a given date\n\n```python\nimport penaltyblog as pb\ndf = pb.clubelo.fetch_rankings_by_date(2010, 1, 1)\ndf.head()\n```\n\n|    |   Rank | Club        | Country   |   Level |     Elo | From                | To                  |\n|---:|-------:|:------------|:----------|--------:|--------:|:--------------------|:--------------------|\n|  0 |      1 | Barcelona   | ESP       |       1 | 1987.68 | 2009-12-18 00:00:00 | 2010-01-02 00:00:00 |\n|  1 |      2 | Chelsea     | ENG       |       1 | 1945.54 | 2009-12-29 00:00:00 | 2010-01-16 00:00:00 |\n|  2 |      3 | Man United  | ENG       |       1 | 1928.53 | 2009-12-31 00:00:00 | 2010-01-09 00:00:00 |\n|  3 |      4 | Real Madrid | ESP       |       1 | 1902.72 | 2009-12-20 00:00:00 | 2010-01-03 00:00:00 |\n|  4 |      5 | Inter       | ITA       |       1 | 1884.49 | 2009-12-21 00:00:00 | 2010-01-06 00:00:00 |\n\n### List all teams with ratings available\n\n```python\nimport penaltyblog as pb\nteams = pb.clubelo.list_all_teams()\nteams[:5]\n```\n\n```\n[\'Man City\', \'Bayern\', \'Liverpool\', \'Real Madrid\', \'Man United\']\n```\n\n### Download Historical ELO ratings for a given team\n\n```python\nimport penaltyblog as pb\ndf = pb.clubelo.fetch_rankings_by_team("barcelona")\ndf.head()\n```\n\n|    | Rank   | Club      | Country   |   Level |     Elo | From                | To                  |\n|---:|:-------|:----------|:----------|--------:|--------:|:--------------------|:--------------------|\n|  0 | None   | Barcelona | ESP       |       1 | 1636.7  | 1939-10-22 00:00:00 | 1939-12-03 00:00:00 |\n|  1 | None   | Barcelona | ESP       |       1 | 1626.1  | 1939-12-04 00:00:00 | 1939-12-10 00:00:00 |\n|  2 | None   | Barcelona | ESP       |       1 | 1636.73 | 1939-12-11 00:00:00 | 1939-12-17 00:00:00 |\n|  3 | None   | Barcelona | ESP       |       1 | 1646.95 | 1939-12-18 00:00:00 | 1939-12-24 00:00:00 |\n|  4 | None   | Barcelona | ESP       |       1 | 1637.42 | 1939-12-25 00:00:00 | 1939-12-31 00:00:00 |\n\n## References\n\n- Mark J. Dixon and Stuart G. Coles (1997) Modelling Association Football Scores and Inefficiencies in the Football Betting Market.\n- Håvard Rue and Øyvind Salvesen (1999) Prediction and Retrospective Analysis of Soccer Matches in a League.\n- Anthony C. Constantinou and Norman E. Fenton (2012) Solving the problem of inadequate scoring rules for assessing probabilistic football forecast models\n- Hyun Song Shin (1992) Prices of State Contingent Claims with Insider Traders, and the Favourite-Longshot Bias\n- Hyun Song Shin (1993) Measuring the Incidence of Insider Trading in a Market for State-Contingent Claims\n- Joseph Buchdahl (2015) The Wisdom of the Crowd\n',
    'author': 'Martin Eastwood',
    'author_email': 'martin.eastwood@gmx.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/martineastwood/penaltyblog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
