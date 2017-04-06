def xpathGetInt(element, path):
	if not path.endswith('text()') and path.endswith('/'):
		path += 'text()'
	else:
		path += '/text()'
	
	result = element.xpath(path)
	if result:
		return int(result[0])
	else:
		return None


def xpathGetStr(element, path):
	if not path.endswith('text()') and path.endswith('/'):
		path += 'text()'
	else:
		path += '/text()'
	
	result = element.xpath(path)
	if result:
		return result[0]
	else:
		return None
