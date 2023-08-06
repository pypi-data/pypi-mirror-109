import os
def match(srch: list, dir: str) -> dict:
    os.chdir(dir)
    files = os.listdir()
    files = [file for file in files if os.path.isfile(os.path.join(dir, file))]
    match = {
        'files': files.copy(),
        'matches': []
    }
    temp_matches = []
    for file in files:
        with open(file, 'r') as checking:
            content = (line for line in checking)
            for line in content:
                for string in srch:
                    if string in line:
                        temp_matches.append(string)

        if len(temp_matches) != 0:
            temp_matches = sorted(
                list(set(temp_matches)))
            match['matches'].append(temp_matches.copy())
        else:
            match['matches'].append(None)
        temp_matches.clear()
    return match