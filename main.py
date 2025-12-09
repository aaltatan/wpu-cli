import locale

from devtools import debug


def main():
    debug(locale.localeconv())


if __name__ == "__main__":
    main()
