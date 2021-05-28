star = '*'

Sex = [('*')]

Race = [('*')]

Marital_Status = [{('Alone'),('Leave'),('Married'),('NM')},{('*')}]

Age = [{(16,20),(21,25),(26,30),(31,35),(36,40),(41,45),(46,50),(51,55),
        (56,60),(61,65),(66,70),(71,75),(76,80),(81,85),(86,90),(91,95)},
        {(16,25),(26,35),(36,45),(46,55),(56,65),(66,75),(76,85),(86,95)},
        {(16,35),(36,55),(56,75),(76,95)}]


def GeneralizeAge(i,G):
    if G != 4:
        for vector in Age[G-1]:
            if vector[0] <= i and vector[1] >=i:
                break
        return str(vector)
    else:
        return star
    
def GeneralizeSex(str,G):
    if G == 1:
        return star
    else:
        return str

def GeneralizeRace(str,G):
    if G == 1:
        return star
    else:
        return str

a = GeneralizeAge(52,2)
print(a)