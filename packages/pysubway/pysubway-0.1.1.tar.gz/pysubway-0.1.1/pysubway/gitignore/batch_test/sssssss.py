def a():
    try:
        raise SystemError('xxx')
    finally:
        return 1111

def func2():
    try:
        raise ValueError()
    except:
        return 1
    finally:
        return 3


if __name__ == '__main__':
    w  = a()
    print(w)
    print(func2())
