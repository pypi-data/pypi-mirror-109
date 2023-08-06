from reportlab.platypus import Table, Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import ttfonts, pdfmetrics


class pdf_creator:

    def __init__(self, path: str):
        """
        :param path: to create file
        """
        self.file = Canvas(path)
        pdfmetrics.registerFont(ttfonts.TTFont("Calibri", "Calibri.ttf"))
        self.file.setFont("Calibri", 14)

    def text(self, string: str, x: int, y: int):
        """"
        :param string: your text
        :param x: string-coordinate
        :param y: string-coordinate
        """
        self.file.drawString(x, y, string)

    def table(self, data: list, x: int, y: int):
        """
        :param data: data-list
        :param x: table-cordinate
        :param y: table-cordinate
        """
        style = [("GRID", (0, 1), (-1, -1), 1, "Black"), ("FONT", (0, 0), (-1, -1), "Calibri", 14),
                 ("BOX", (0, 0), (-1, -1), 1, "Black")]
        table = Table(data=data, style=style)
        table.wrapOn(self.file, 10, 10)
        table.drawOn(self.file, x, y)

    def image(self, path: str, x: int, y: int):
        """
        :param path: to image
        :param x: image-cordinate
        :param y: image-cordinate
        """
        image = Image(path)
        image.drawOn(self.file, x, y)

    def save(self):
        self.file.save()
