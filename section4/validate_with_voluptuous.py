from voluptuous import Schema, Match


schema = Schema({
    'name': str,
    'price': Match(r'^[0-9,]+$'),
}, required=True)

schema({
    'name': 'ぶどう',
    'price': '3,000',
})

schema({
    'name': None,
    'price': '3,000'
})
