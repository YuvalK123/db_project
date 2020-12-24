import sys
import pickle


def main():
    names = []
    all_info = []
    directors_f = open(sys.argv[2], 'r', encoding='utf-16', errors='ignore')
    directors_info = directors_f.readlines()
    directors_f.close()
    for line in directors_info:  # [actor, 'actedIn', movie]
        line = line.strip('\n').split('>,<')
        if len(line) < 4 or not line[3].find('>'):
            continue
        tmp = line[1].replace('_', ' ')  # remove dataset markings
        x = tmp.find("(")
        if x > 0:
            tmp = tmp[:x - 2]  # remove brackets
        names.append(tmp)
        all_info.append([tmp, 1])

    people_f = open(sys.argv[1], "r", encoding='utf-16', errors='ignore')
    data = people_f.readlines()
    people_f.close()
    for counter, line in enumerate(data):
        line = line.replace('\x00', '').strip('\n').split('>,<')
        if len(line) < 4 or not line[3].find('>'):
            continue
        for index in range(len(line)):
            line[index] = line[index].replace('<', ' ').replace('>', ' ').replace('_', ' ')  # remove dataset markings
            x = line[index].find("(")
            if x > 0:
                line[index] = line[index][:x - 2]  # remove brackets
        if line[2] == 'actedIn':
            names.append(line[1])
            all_info.append([line[1], 0])
        if line[2] == 'wasBornIn' and line[1] in names:
            all_info[names.index(line[1])].append(line[3])
        elif line[2] == 'diedIn' and line[1] in names:
            loc = all_info[names.index(line[1])]
            if len(loc) == 2:
                loc.append('')
            loc.append(line[3])
        elif line[2] == 'hasGender' and line[1] in names:
            loc = all_info[names.index(line[1])]
            if len(loc) == 2:
                loc.append('')
            if len(loc) == 3:
                loc.append('')
            all_info[names.index(line[1])].append(line[3])

    with open("backup.txt", "wb") as fp:  # Pickling
        pickle.dump(all_info, fp)


if __name__ == '__main__':
    main()
