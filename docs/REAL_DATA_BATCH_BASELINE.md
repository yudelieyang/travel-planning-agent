# Phase O5 controlled-data baseline

Captured before Phase O5 snapshot generation on 2026-09-16 from
`data/travel/us/cities.json`. Candidate notation is
`id | mock name | price/unit | planner tags | rating/reviews`; row order is the existing deterministic
price/ID order when no preference matches. This file records controlled behavior only and is not an
OSM source artifact.

| City | Category | Controlled candidates in deterministic order |
|---|---|---|
| New York City | attractions | `nyc-a3 | Mock Riverside Park | 0/per_person_visit | parks | 4.8/3200`; `nyc-a1 | Mock City Art Museum | 25/per_person_visit | museums,art | 4.7/2100`; `nyc-a2 | Mock History Museum | 30/per_person_visit | museums,history | 4.6/1750` |
| New York City | hotel | `nyc-h1 | Mock Midtown Lodge | 120/per_person_night | central,budget | 4.1/780`; `nyc-h2 | Mock Garden Inn | 150/per_person_night | quiet | 4.3/460`; `nyc-h3 | Mock Skyline Hotel | 250/per_person_night | central,luxury | 4.7/990` |
| New York City | food | `nyc-f1 | Mock Green Kitchen | 18/per_person_meal | vegetarian,vegan | 4.5/620`; `nyc-f2 | Mock Market Cafe | 22/per_person_meal | vegetarian | 4.3/480`; `nyc-f3 | Mock Harbor Table | 35/per_person_meal | seafood | 4.6/850` |
| New York City | transport | `nyc-t1 | Mock Walking Allowance | 0/per_person_day | walking | null`; `nyc-t2 | Mock Transit Day Allowance | 12/per_person_day | public transit | 4.5/2400`; `nyc-t3 | Mock Taxi Day Allowance | 50/per_person_day | taxi | 4.0/710` |
| Chicago | attractions | `chi-a3 | Mock Lakefront Park | 0/per_person_visit | parks,walking | 4.8/2100`; `chi-a2 | Mock City History Center | 18/per_person_visit | museums,history | 4.5/790`; `chi-a1 | Mock Lakeside Art Hall | 24/per_person_visit | museums,art | 4.7/1400` |
| Chicago | hotel | `chi-h1 | Mock Loop Budget Lodge | 95/per_person_night | budget,central | 4.1/560`; `chi-h2 | Mock Lakeside Inn | 135/per_person_night | quiet | 4.4/430`; `chi-h3 | Mock Magnificent Hotel | 225/per_person_night | luxury,central | 4.7/840` |
| Chicago | food | `chi-f2 | Mock Green Loop Cafe | 17/per_person_meal | vegetarian,vegan | 4.4/410`; `chi-f1 | Mock Deep Dish Kitchen | 19/per_person_meal | pizza,local | 4.6/970`; `chi-f3 | Mock Lake Table | 31/per_person_meal | seafood | 4.5/530` |
| Chicago | transport | `chi-t1 | Mock Walking Allowance | 0/per_person_day | walking | null`; `chi-t2 | Mock Rail Day Allowance | 10/per_person_day | public transit | 4.4/1500`; `chi-t3 | Mock Taxi Day Allowance | 44/per_person_day | taxi | 4.0/390` |
| Washington DC | attractions | `wdc-a1 | Mock National History Hall | 0/per_person_visit | museums,history | 4.8/2400`; `wdc-a2 | Mock Capital Art Gallery | 0/per_person_visit | museums,art | 4.7/1850`; `wdc-a3 | Mock Monument Garden | 0/per_person_visit | parks,history,walking | 4.8/3100` |
| Washington DC | hotel | `wdc-h1 | Mock District Lodge | 110/per_person_night | budget,central | 4.1/510`; `wdc-h2 | Mock Capitol Garden Inn | 155/per_person_night | quiet | 4.4/480`; `wdc-h3 | Mock Federal Hotel | 240/per_person_night | luxury,central | 4.7/720` |
| Washington DC | food | `wdc-f1 | Mock District Greens | 18/per_person_meal | vegetarian,vegan | 4.4/430`; `wdc-f2 | Mock Capital Grill Counter | 24/per_person_meal | grilled,local | 4.5/590`; `wdc-f3 | Mock Potomac Table | 33/per_person_meal | seafood | 4.6/680` |
| Washington DC | transport | `wdc-t1 | Mock Walking Allowance | 0/per_person_day | walking | null`; `wdc-t2 | Mock Metro Day Allowance | 11/per_person_day | public transit | 4.5/1700`; `wdc-t3 | Mock Taxi Day Allowance | 46/per_person_day | taxi | 4.0/420` |
| Miami | attractions | `mia-a3 | Mock Palm Park | 0/per_person_visit | parks,walking | 4.7/1300`; `mia-a2 | Mock Bay History Center | 16/per_person_visit | museums,history | 4.4/520`; `mia-a1 | Mock Coastal Art Museum | 23/per_person_visit | museums,art | 4.6/910` |
| Miami | hotel | `mia-h1 | Mock Downtown Budget Lodge | 105/per_person_night | budget,central | 4.0/470`; `mia-h2 | Mock Palm Garden Inn | 145/per_person_night | quiet | 4.3/390`; `mia-h3 | Mock Ocean Luxury Hotel | 260/per_person_night | luxury,central | 4.7/920` |
| Miami | food | `mia-f1 | Mock Calle Cafe | 16/per_person_meal | cuban,local | 4.6/770`; `mia-f2 | Mock Palm Greens | 19/per_person_meal | vegetarian,vegan | 4.4/380`; `mia-f3 | Mock Ocean Table | 34/per_person_meal | seafood | 4.7/880` |
| Miami | transport | `mia-t1 | Mock Walking Allowance | 0/per_person_day | walking | null`; `mia-t2 | Mock Transit Day Allowance | 9/per_person_day | public transit | 4.1/620`; `mia-t3 | Mock Taxi Day Allowance | 48/per_person_day | taxi | 4.0/350` |
| Denver | attractions | `den-a3 | Mock City Mountain Park | 0/per_person_visit | parks,outdoors | 4.8/1450`; `den-a2 | Mock Frontier History Hall | 17/per_person_visit | museums,history | 4.5/540`; `den-a1 | Mock Mountain Art Museum | 21/per_person_visit | museums,art | 4.6/760` |
| Denver | hotel | `den-h1 | Mock Union Budget Lodge | 92/per_person_night | budget,central | 4.1/470`; `den-h2 | Mock Mountain Garden Inn | 128/per_person_night | quiet | 4.4/405`; `den-h3 | Mock Summit Hotel | 215/per_person_night | luxury,central | 4.7/690` |
| Denver | food | `den-f1 | Mock Mile High Cafe | 16/per_person_meal | local,casual | 4.5/560`; `den-f2 | Mock Mountain Greens | 18/per_person_meal | vegetarian,vegan | 4.4/370`; `den-f3 | Mock Alpine Table | 29/per_person_meal | grilled,local | 4.6/610` |
| Denver | transport | `den-t1 | Mock Walking Allowance | 0/per_person_day | walking | null`; `den-t2 | Mock Rail Day Allowance | 10/per_person_day | public transit | 4.3/780`; `den-t3 | Mock Taxi Day Allowance | 43/per_person_day | taxi | 4.1/340` |
| Seattle | attractions | `sea-a3 | Mock Evergreen Park | 0/per_person_visit | parks,outdoors | 4.8/1720`; `sea-a2 | Mock Northwest History Hall | 19/per_person_visit | museums,history | 4.5/610`; `sea-a1 | Mock Sound Art Museum | 24/per_person_visit | museums,art | 4.7/980` |
| Seattle | hotel | `sea-h1 | Mock Market Budget Lodge | 108/per_person_night | budget,central | 4.1/530`; `sea-h2 | Mock Sound Garden Inn | 148/per_person_night | quiet | 4.4/420`; `sea-h3 | Mock Skyline Hotel | 245/per_person_night | luxury,central | 4.7/790` |
| Seattle | food | `sea-f1 | Mock Market Chowder | 18/per_person_meal | seafood,local | 4.6/890`; `sea-f2 | Mock Evergreen Kitchen | 19/per_person_meal | vegetarian,vegan | 4.5/460`; `sea-f3 | Mock Sound Table | 32/per_person_meal | seafood | 4.7/730` |
| Seattle | transport | `sea-t1 | Mock Walking Allowance | 0/per_person_day | walking | null`; `sea-t2 | Mock Transit Day Allowance | 11/per_person_day | public transit | 4.4/960`; `sea-t3 | Mock Taxi Day Allowance | 47/per_person_day | taxi | 4.0/370` |
| San Francisco | attractions | `sfo-a3 | Mock Golden Park | 0/per_person_visit | parks,walking | 4.8/2300`; `sfo-a2 | Mock Cable History Hall | 20/per_person_visit | museums,history | 4.5/720`; `sfo-a1 | Mock Bay Art Museum | 26/per_person_visit | museums,art | 4.7/1250` |
| San Francisco | hotel | `sfo-h1 | Mock Bay Budget Lodge | 125/per_person_night | budget,central | 4.0/610`; `sfo-h2 | Mock Sunset Garden Inn | 165/per_person_night | quiet | 4.4/450`; `sfo-h3 | Mock Embarcadero Hotel | 275/per_person_night | luxury,central | 4.7/870` |
| San Francisco | food | `sfo-f1 | Mock Mission Kitchen | 20/per_person_meal | local,casual | 4.5/640`; `sfo-f2 | Mock Bay Greens | 22/per_person_meal | vegetarian,vegan | 4.5/510`; `sfo-f3 | Mock Wharf Table | 38/per_person_meal | seafood | 4.7/960` |
| San Francisco | transport | `sfo-t1 | Mock Walking Allowance | 0/per_person_day | walking | null`; `sfo-t2 | Mock Transit Day Allowance | 13/per_person_day | public transit | 4.4/1180`; `sfo-t3 | Mock Taxi Day Allowance | 54/per_person_day | taxi | 4.0/410` |
| Los Angeles | attractions | `lax-a3 | Mock Canyon Park | 0/per_person_visit | parks,outdoors | 4.8/1900`; `lax-a1 | Mock Pacific Art Museum | 25/per_person_visit | museums,art | 4.6/1150`; `lax-a2 | Mock Film History Center | 27/per_person_visit | museums,history,film | 4.6/890` |
| Los Angeles | hotel | `lax-h1 | Mock Downtown Budget Lodge | 112/per_person_night | budget,central | 4.0/580`; `lax-h2 | Mock Canyon Garden Inn | 152/per_person_night | quiet | 4.3/420`; `lax-h3 | Mock Pacific Luxury Hotel | 265/per_person_night | luxury,central | 4.7/910` |
| Los Angeles | food | `lax-f1 | Mock Taco Studio | 16/per_person_meal | tacos,local | 4.6/920`; `lax-f2 | Mock Pacific Greens | 21/per_person_meal | vegetarian,vegan | 4.5/520`; `lax-f3 | Mock Coastal Table | 36/per_person_meal | seafood | 4.6/790` |
| Los Angeles | transport | `lax-t1 | Mock Walking Allowance | 0/per_person_day | walking | null`; `lax-t2 | Mock Transit Day Allowance | 9/per_person_day | public transit | 4.0/690`; `lax-t3 | Mock Rideshare Day Allowance | 55/per_person_day | taxi | 4.1/450` |
| Las Vegas | attractions | `las-a3 | Mock Springs Preserve Park | 12/per_person_visit | parks,outdoors | 4.7/1180`; `las-a2 | Mock Desert History Center | 19/per_person_visit | museums,history | 4.5/620`; `las-a1 | Mock Neon Art Hall | 24/per_person_visit | museums,art | 4.6/940` |
| Las Vegas | hotel | `las-h1 | Mock Downtown Budget Lodge | 78/per_person_night | budget,central | 4.0/720`; `las-h2 | Mock Desert Garden Inn | 118/per_person_night | quiet | 4.3/410`; `las-h3 | Mock Strip Luxury Hotel | 235/per_person_night | luxury,central | 4.7/1280` |
| Las Vegas | food | `las-f1 | Mock Desert Cafe | 15/per_person_meal | local,casual | 4.4/610`; `las-f2 | Mock Springs Greens | 19/per_person_meal | vegetarian,vegan | 4.4/430`; `las-f3 | Mock Boulevard Table | 34/per_person_meal | grilled,luxury | 4.6/850` |
| Las Vegas | transport | `las-t1 | Mock Walking Allowance | 0/per_person_day | walking | null`; `las-t2 | Mock Transit Day Allowance | 8/per_person_day | public transit | 4.0/540`; `las-t3 | Mock Taxi Day Allowance | 49/per_person_day | taxi | 4.1/390` |

## Generic three-day comparison baseline

Each request used one traveler and a USD 10,000 hard total limit, so no repair was needed.

| City | Total | Selected / alternatives | Validator / repair |
|---|---:|---|---|
| New York City | 520 | attractions `a3,a1,a2/-`; hotel `h1/h2,h3`; food `f1,f2,f3/-`; transport `t1/t2,t3` | passed / 0 |
| Chicago | 433 | attractions `a3,a2,a1/-`; hotel `h1/h2,h3`; food `f2,f1,f3/-`; transport `t1/t2,t3` | passed / 0 |
| Washington DC | 445 | attractions `a1,a2,a3/-`; hotel `h1/h2,h3`; food `f1,f2,f3/-`; transport `t1/t2,t3` | passed / 0 |
| Miami | 456 | attractions `a3,a2,a1/-`; hotel `h1/h2,h3`; food `f1,f2,f3/-`; transport `t1/t2,t3` | passed / 0 |
| Denver | 411 | attractions `a3,a2,a1/-`; hotel `h1/h2,h3`; food `f1,f2,f3/-`; transport `t1/t2,t3` | passed / 0 |
| Seattle | 466 | attractions `a3,a2,a1/-`; hotel `h1/h2,h3`; food `f1,f2,f3/-`; transport `t1/t2,t3` | passed / 0 |
| San Francisco | 536 | attractions `a3,a2,a1/-`; hotel `h1/h2,h3`; food `f1,f2,f3/-`; transport `t1/t2,t3` | passed / 0 |
| Los Angeles | 495 | attractions `a3,a1,a2/-`; hotel `h1/h2,h3`; food `f1,f2,f3/-`; transport `t1/t2,t3` | passed / 0 |
| Las Vegas | 415 | attractions `a3,a2,a1/-`; hotel `h1/h2,h3`; food `f1,f2,f3/-`; transport `t1/t2,t3` | passed / 0 |

## Existing scenario audit

- New York City has explicit candidate/provider, alias, food-preference fallback, budget, API,
  tool-filtering, planner, graph, and semantic tests. Its `seafood` food preference changes ordering.
- Chicago, Miami, Denver, Seattle, San Francisco, Los Angeles, Las Vegas, and Washington DC appear
  in semantic/evaluation cases; recruiter-readiness scenarios additionally exercise Chicago
  museums/pizza, Seattle seafood/parks, Miami seafood/budgets, Denver hard budgets, and Los Angeles
  outdoor/Asian-food wording.
- None of these references authorizes changing the controlled planner tags, prices, selection,
  semantic parsing, or repair behavior. O5 comparisons therefore use internal IDs and existing
  planner metadata as the contract.
