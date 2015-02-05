UPDATE_DEF = {
    'entity_def': {
        'entity_sparql': '?uri a foaf:Organization . ?uri a vivo:ExtensionUnit . ?uri a ufVivo:UFEntity . ',
        'order_by': 'name',
        'type': FOAF.Organization
    },
    'column_defs': {
        'name': [{'predicate': {'ref': RDFS.label, 'single': True}, 'object': {'literal': True}}],
        'type': [{'predicate': {'ref': RDF.type, 'single': False, 'include': ['thing', 'agent', 'org']},
                  'object': {'literal': False, 'enum': 'org_types'}}],
        'within': [{'predicate': {'ref': VIVO.subOrganizationWithin, 'single': False},
                    'object': {'literal': False}}],
        'url': [{'predicate': {'ref': VIVO.webpage, 'single': False},
                 'object': {'literal': False, 'type': VIVO.URLLink, 'name': 'weburi'}},
                {'predicate': {'ref': VIVO.linkURI, 'single': True}, 'object': {'literal': True}}],
        'phone': [{'predicate': {'ref': VIVO.primaryPhone, 'single': True},
                   'object': {'literal': True, 'filter': 'repair_phone_number'}}],
        'email': [{'predicate': {'ref': VIVO.primaryEmail, 'single': True},
                   'object': {'literal': True, 'filter': 'repair_email'}}],
        'address1': [{'predicate': {'ref': VIVO.mailingAddress, 'single': True},
                      'object': {'literal': False, 'type': VIVO.Address, 'name': 'address'}},
                     {'predicate': {'ref': VIVO.address1, 'single': True}, 'object': {'literal': True}}],
        'address2': [{'predicate': {'ref': VIVO.mailingAddress, 'single': True},
                      'object': {'literal': False, 'type': VIVO.Address, 'name': 'address'}},
                     {'predicate': {'ref': VIVO.address2, 'single': True}, 'object': {'literal': True}}],
        'city': [{'predicate': {'ref': VIVO.mailingAddress, 'single': True},
                  'object': {'literal': False, 'type': VIVO.Address, 'name': 'address'}},
                 {'predicate': {'ref': VIVO.addressCity, 'single': True}, 'object': {'literal': True}}],
        'state': [{'predicate': {'ref': VIVO.mailingAddress, 'single': True},
                   'object': {'literal': False, 'type': VIVO.Address, 'name': 'address'}},
                  {'predicate': {'ref': VIVO.addressState, 'single': True}, 'object': {'literal': True}}],
        'zip': [{'predicate': {'ref': VIVO.mailingAddress, 'single': True},
                 'object': {'literal': False, 'type': VIVO.Address, 'name': 'address'}},
                {'predicate': {'ref': VIVO.addressPostalCode, 'single': True}, 'object': {'literal': True}}],
        'photo': [{'predicate': {'ref': VITROP.mainImage, 'single': True},
                   'object': {'literal': False, 'type': VITROP.File, 'name': 'photouri'}},
                  {'predicate': {'ref': VITROP.filename, 'single': True}, 'object': {'literal': True}}],
        'abbreviation': [{'predicate': {'ref': VIVO.abbreviation, 'single': True}, 'object': {'literal': True}}],
        'isni': [{'predicate': {'ref': UFV.isni, 'single': True}, 'object': {'literal': True}}],
        'successor': [{'predicate': {'ref': VIVO.hasSuccessorOrg, 'single': False}, 'object': {'literal': False}}],
        'overview': [{'predicate': {'ref': VIVO.overview, 'single': True}, 'object': {'literal': True}}]
    }
}
