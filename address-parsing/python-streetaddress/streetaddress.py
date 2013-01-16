from addressconf import Directions, Streets, States, Regexes
import re

def parse(location):
	if Regexes.corner.search(location):
		return parse_intersection(location)
	else:
		return parse_address(location)

def parse_intersection(inter):
	match = Regexes.intersection.match(inter)
	if not match:
		return
	match_data = match.groups()
	return normalize_address({'street':match_data[3] or match_data[8],
			'street_type':match_data[4],
			'suffix':match_data[5],
			'prefix':match_data[2],
			'street2':match_data[14] or match_data[19],
			'street_type2':match_data[15],
			'suffix2':match_data[16],
			'prefix2':match_data[13],
			'city':match_data[22],
			'state':match_data[23],
			'postal_code':match_data[24]})

def parse_address(addr):
	match = Regexes.address.match(addr)
	if not match:
		return
	match_data = match.groups()
	return normalize_address({'number':match_data[0],
			'street':match_data[4] or match_data[9] or match_data[1],
			'street_type':match_data[5] or match_data[2],
			'unit':match_data[13],
			'unit_prefix':match_data[12],
			'suffix':match_data[6] or match_data[11],
			'prefix':match_data[3],
			'city':match_data[14],
			'state':match_data[15],
			'postal_code':match_data[16],
			'postal_code_ext':match_data[17]})

def normalize_address(addr):
	addr['state'] = normalize_state(addr['state']) if 'state' in addr and addr['state'] else None
 	addr['street_type'] = normalize_street_type(addr['street_type']) if 'street_type' in addr and addr['street_type'] else None
        addr['prefix'] = normalize_directional(addr['prefix']) if 'prefix' in addr and addr['prefix'] else None
        addr['suffix'] = normalize_directional(addr['suffix']) if 'suffix' in addr and addr['suffix'] else None
        addr['street'] = addr['street'].upper() if 'street' in addr and addr['street'] else None
        addr['street_type2'] = normalize_street_type(addr['street_type2']) if 'street_type2' in addr and addr['street_type2'] else None
	addr['prefix2'] = normalize_directional(addr['prefix2']) if 'prefix2' in addr and addr['prefix2'] else None
        addr['suffix2'] = normalize_directional(addr['suffix2']) if 'suffix2' in addr and addr['suffix2'] else None
        addr['street2'] = addr['street2'].upper() if 'street2' in addr and addr['street2'] else None
        addr['city'] = addr['city'].upper() if 'city' in addr and addr['city'] else None
        addr['unit_prefix'] = addr['unit_prefix'].upper() if 'unit_prefix' in addr and addr['unit_prefix'] else None
	return addr 

def normalize_state(state):
	if len(state) < 3:
		return state.upper()
	else:
		return States.STATE_CODES[state.lower()]

def normalize_street_type(s_type):
	if s_type.lower() in Streets.STREET_TYPES:
		return Streets.STREET_TYPES[s_type.lower()]
	elif s_type.lower() in Streets.STREET_TYPES_LIST:
		return s_type.upper()
      
def normalize_directional(direction):
	if len(direction) < 3:
		return direction.upper()
	else:
		return Directions.DIRECTIONAL[direction.lower()]
