from dateutil import parser


def parse_date(date_str):
    try:
        return parser.parse(date_str)
    except Exception as e:
        print('Пиздец, {}'.format(str(e)))


if __name__ == '__main__':
    print(parse_date('sun aug. 19 00:27:52 2018'))