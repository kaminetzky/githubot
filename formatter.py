class Formatter:
    @staticmethod
    def format_issue(author, number, title, text, url):
        string = ('<b>Issue #{}</b>\n'
                  '<b>Título:</b> {}\n'
                  '<b>Autor:</b> {}\n\n'
                  '{}\n\n'
                  '<a href="{}">Link</a>'.format(number, title, author, text,
                                                 url))
        return string
