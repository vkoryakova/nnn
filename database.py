import MySQLdb as mdb

class QwrSql:
    def __init__(self):
        try:
            self.conn = mdb.connect("localhost", "root", "", "demo_5")
        except mdb.Error as e:
            print(f"Ошибка подулючения: {e}")
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def load_partners(self):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT p.id, p.name, t.name, p.director, p.inn, p.rating, p.discount
                        FROM partners p
                        INNER JOIN type_partner t ON t.id = p.id_type
                        ORDER BY p.id ASC;""")
            res = cur.fetchall()
            return res
        except mdb.Error as e:
            print(f"Ошибка получения данных: {e}")
            raise

    def load_types(self):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT id, name FROM type_partner""")

            res = cur.fetchall()
            return res

        except mdb.Error as e:
            print(f"Ошибка получения данных: {e}")
            raise

    def load_partner(self, partner_id):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT p.name, p.director, p.inn, p.rating, p.discount, t.name
                        FROM partners p
                        INNER JOIN type_partner t ON t.id = p.id_type
                        WHERE p.id = %s""", (partner_id, ))
            res = cur.fetchall()
            return res
        except mdb.Error as e:
            print(f"Ошибка получения данных: {e}")
            raise

    def update_partner(self, partner_id, type_p, name, director, inn, rating, discount):
        try:
            cur = self.conn.cursor()
            cur.execute("""
            UPDATE partners
                SET id_type = %s,
                    name = %s,
                    director = %s,
                    inn = %s,
                    rating = %s,
                    discount = %s
            WHERE id = %s """, (type_p, name, director, inn, rating, discount, partner_id))
            cur.close()
            self.conn.commit()
        except mdb.Error as e:
            print(f"Ошибка обновления данных {e}")
            raise

    def add_partner(self, type_p, name, director, inn, rating, discount):
        try:
            cur = self.conn.cursor()
            cur.execute("""INSERT INTO partners(name, director, inn, rating, discount, id_type) 
                            VALUES(%s, %s, %s, %s, %s, %s)""", (name, director,inn,rating, discount, type_p))
            cur.close()
            self.conn.commit()

        except mdb.Error as e:
            print(f"Ошибка добавления партнера {e}")
            raise

    def delete_partner(self, partner_id):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT COUNT(*) FROM orders WHERE id_partner = %s""", (partner_id,))
            order_count = cur.fetchone()[0]
            if order_count > 0:
                raise Exception("Нельзя удалить партнера с существующими заказами.")
            cur.execute("""DELETE FROM partners WHERE id = %s""", (partner_id,))
            cur.close()
            self.conn.commit()


        except mdb.Error as e:
            print(f"Ошибка удаления партнера {e}")
            raise

    def load_orders(self, partner_id):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT o.id, p.name, o.amount_product, o.date_at FROM orders o
                        INNER JOIN products p ON p.id = o.id_product
                        WHERE o.id_partner = %s
                        ORDER BY o.id ASC""", (partner_id, ))
            res = cur.fetchall()
            cur.close()
            return res
        except mdb.Error as e:
            print(f"Ошибка получения данных: {e}")
            raise

    def load_percent_material(self, order_id):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT t_m.brak_persent FROM type_materials t_m
                        INNER JOIN matreials m ON m.id_type_material = t_m.id
                        INNER JOIN product_material pm ON pm.id_material = m.id
                        INNER JOIN products p ON p.id = pm.id_product
                        INNER JOIN orders o ON o.id_product = p.id
                        WHERE o.id = %s""", (order_id,))

            res = cur.fetchone()
            cur.close()
            return res[0] if res and res[0] is not None else 0
        except mdb.Error as e:
            print(f"Ошибка получения данных: {e}")
            raise

    def calc_space(self, order_id):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT (p.weight * p.height) as s FROM products p 
                        INNER JOIN orders o ON o.id_product = p.id
                        WHERE o.id = %s""", (order_id,))

            res = cur.fetchone()
            cur.close()
            return res[0] if res and res[0] is not None else 0
        except mdb.Error as e:
            print(f"Ошибка получения данных: {e}")
            raise

    def load_amount(self, order_id):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT o.amount_product FROM orders o 
                        WHERE o.id = %s""", (order_id,))

            res = cur.fetchone()
            cur.close()
            return res[0] if res and res[0] is not None else 0
        except mdb.Error as e:
            print(f"Ошибка получения данных: {e}")
            raise
