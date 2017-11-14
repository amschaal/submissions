from bioproject import typeOrganism

organism = typeOrganism()
organism.GenomeSize = 100
organism.OrganismName = 'foo'

with open('test.xml','w') as file:
    file.write(organism.toxml('utf-8'))