class Formatter:
    @staticmethod
    def format_issue(author, number, title, text, url):
        string = ('<i>[{}]</i>\n'
                  '<b>[#{} - {}]</b>\n\n'
                  '{}\n\n'
                  '<a href="{}">[Link]</a>'.format(author, number, title, text,
                                                 url))
        return string
