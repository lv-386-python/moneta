from helper import db_helper as db


class Icon:
    """
    Model for interacting with icons.
    """

    def __init__(self, id, css, category):
        self.id = id
        self.css = css
        self.category = category

    def __repr__(self):
        return f"<icon - {self.id}>"

    def __str__(self):
        return f"icon - id:{self.id}"

    @staticmethod
    def get_icons(category):
        """
        Returns a list of icons, available for for a particular category.
        :params: category for which we need a list of icons
        :return: list of available icons
        """
        sql = f"""
            SELECT *
            FROM  image
            WHERE category='{category}';
            """
        query = db.select_sql(sql)
        icon_list = []
        for row in query:
            icon = Icon(*row)
            icon_list.append(icon)
        return icon_list
