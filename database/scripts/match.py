import pandas as pd

mapping = {
    "ABV-IIITM": "Atal Bihari Vajpayee Indian Institute of Information Technology and Management",
    "PDPM IIITDM": "Pandit Dwarka Prasad Mishra Indian Institute of Information Technology, Design and Manufacturing",
    "IIITDM": "Indian Institute of Information Technology, Design and Manufacturing",
    "MNNIT": "Motilal Nehru National Institute of Technology",
    "SVNIT": "Sardar Vallabhbhai National Institute of Technology",
    "VNIT": "Visvesvaraya National Institute of Technology",
    "MNIT": "Malaviya National Institute of Technology",
    "MANIT": "Maulana Azad National Institute of Technology",
    "IIEST": "Indian Institute of Engineering Science and Technology",
    "IISER": "Indian Institute of Science Education and Research",
    "IISc": "Indian Institute of Science",
    "IIIT": "Indian Institute of Information Technology",
    "IIT": "Indian Institute of Technology",
    "NIT": "National Institute of Technology",
    "BIT": "Birla Institute of Technology",
    "PEC": "Punjab Engineering College",
    "ICT": "Institute of Chemical Technology",
    "JNU": "Jawaharlal Nehru University",
    "HBTU": "Harcourt Butler Technical University",
    "SPA": "School of Planning and Architecture"
}

def expand_institute_name(name):
    if not isinstance(name, str):
        return name

    # longest abbreviations first
    for short in sorted(mapping.keys(), key=len, reverse=True):
        if name.startswith(short):
            return name.replace(short, mapping[short], 1)

    return name

feature = pd.read_csv("features.csv")
coor = pd.read_csv("institutes_coordinates.csv")

feature["Institute_Name"] = feature["Institute_Name"].apply(expand_institute_name)
coor["Institute_Name"] = coor["Institute_Name"].apply(expand_institute_name)

feature.to_csv("features.csv", index=False)
coor.to_csv("institutes_coordinates.csv", index=False)