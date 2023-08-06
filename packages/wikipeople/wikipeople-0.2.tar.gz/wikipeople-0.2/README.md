# wikipeople

Use the [Wikidata API](https://www.wikidata.org/wiki/Wikidata:Data_access) to get information about people.

## Install
```sh
pip install wikipeople
```

## Examples
Search for concept ID's given a string
```py
>>> from wikipeople import wikipeople as wp
>>> wp.search_wikidata('Andy Murray')
'Q410'
```


Basic info
```py
>>> wp.get_property(wp.search_wikidata('Carl Sagan'), 'P21')
('Q6581097', 'male')
```


Get someone's date of birth
```py
>>> wp.get_date_of_birth(wp.search_wikidata('Carl Sagan'))
'+1934-11-09'
```


Get information about someone's profession
```py
>>> wp.get_profession_hierarchy(wp.search_wikidata('Andy Murray'))
['tennis player', 'athlete', 'sportsperson']
```


Get someone's Country of birth
```py
>>> wp.get_country(wp.get_property(wp.search_wikidata('Andy Murray'), 'P19')[0])
('Q145', 'United Kingdom')
```


Get info in cases when you already have a Wikipedia link (useful if the name isn't enough to disambiguate)
```py
>>> wp.get_concept_id_from_url('https://en.wikipedia.org/wiki/Pat_Kirkwood_(actress)')
'Q7145678'
```
