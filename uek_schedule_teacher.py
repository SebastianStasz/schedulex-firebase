def getTeacherData(element):
    name_and_degree = element.text.split(',')
    degree_data = name_and_degree[1].strip()
    degree = degree_data if degree_data != '' else None
    return {'fullName': name_and_degree[0],
            'degree': degree,
            'url_suffix': element.get('href')}
