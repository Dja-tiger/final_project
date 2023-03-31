import os, glob

path = os.environ.get('PROJECT_PATH', '.')


def del_session():
    dir = f'{path}/json_file/sessions'
    for file in os.scandir(dir):
        os.remove(file.path)


if __name__ == '__main__':
    del_session()