class Formatter:
    @staticmethod
    def format_issue(author, number, title, text, url):
        string = '[{}]\n[#{} - {}]\n{}\n[Link: {}]'.format(author, number,
                                                           title, text, url)
        return string
