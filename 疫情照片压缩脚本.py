import os
import zipfile

file_lists = []


def renameFile(filepath):
    l = ['202002080507郭一欣', '202078040114李松涛', '202078040418吕玉培']
    pathDir = os.listdir(filepath)
    i = 0
    for allDir in pathDir:
        if allDir[-3:] == 'jpg':
            allDir_new = allDir.replace(allDir[:-4], l[i])
            file_lists.append(allDir_new)
            os.rename(os.path.join(filepath, allDir),
                      os.path.join(filepath, allDir_new))
            i += 1


def file2zip(zip_file_name: str, file_names: list):
    with zipfile.ZipFile(zip_file_name, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for fn in file_names:
            parent_path, name = os.path.split(fn)
            zf.write(fn, arcname=name)


if __name__ == '__main__':
    filepath = './'
    renameFile(filepath)
    zip_name = './315.zip'
    file2zip(zip_name, file_lists)
