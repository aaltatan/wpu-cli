from ..db import Database
from .schemas import Layer, Tax


class NotFoundError(Exception):
    pass


class LayersTaxesDatabase(Database):
    def get_taxes(self) -> list[Tax]:
        self.cursor.execute("SELECT * FROM taxes")
        return [Tax(**tax) for tax in self.cursor.fetchall()]

    def get_tax(self, id: int) -> Tax:
        self.cursor.execute(
            "SELECT * FROM taxes WHERE id = ?",
            (id,),
        )
        result = self.cursor.fetchone()
        if not result:
            raise NotFoundError("Tax not found")
        return Tax(**result)

    def add_tax(self, tax: Tax) -> None:
        self.cursor.execute(
            "INSERT INTO taxes (name, description) VALUES (?, ?)",
            (tax.name, tax.description),
        )
        self.conn.commit()

    def delete_tax(self, id: int) -> None:
        self.cursor.execute(
            "DELETE FROM taxes WHERE id = ?",
            (id,),
        )
        self.conn.commit()

    def update_tax(self, id: int, tax: Tax) -> None:
        self.cursor.execute(
            """
            UPDATE taxes
            SET name = ?, description = ?
            WHERE id = ?
            """,
            (tax.name, tax.description, id),
        )
        self.conn.commit()

    def add_layer(self, layer: Layer, tax_id: int) -> None:
        self.cursor.execute(
            """
            INSERT INTO tax_layers (from_, to_, rate, tax_id)
            VALUES (?, ?, ?, ?)
            """,
            (layer.from_, layer.to_, layer.rate, tax_id),
        )
        self.conn.commit()

    def delete_layer(self, id: int) -> None:
        self.cursor.execute(
            "DELETE FROM tax_layers WHERE id = ?",
            (id,),
        )
        self.conn.commit()

    def update_layer(self, id: int, layer: Layer) -> None:
        self.cursor.execute(
            """
            UPDATE tax_layers
            SET from_ = ?, to_ = ?, rate = ?
            WHERE id = ?
            """,
            (layer.from_, layer.to_, layer.rate, id),
        )
        self.conn.commit()

    def get_layers(self, tax_id: int) -> list[Layer]:
        self.cursor.execute(
            """
            SELECT tax_layers.id, 
                   tax_layers.from_, 
                   tax_layers.to_, 
                   tax_layers.rate, 
                   taxes.name AS tax_name
            FROM tax_layers
            INNER JOIN taxes
            ON tax_layers.tax_id = taxes.id
            WHERE tax_id = ?
            """,
            (tax_id,),
        )
        return [Layer(**layer) for layer in self.cursor.fetchall()]

    def get_layer(self, id: int) -> Layer:
        self.cursor.execute(
            "SELECT * FROM tax_layers WHERE id = ?",
            (id,),
        )
        if not self.cursor.fetchone():
            raise NotFoundError("Layer not found")
        return Layer(**self.cursor.fetchone())

    def _create_tables(self) -> None:
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS taxes (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            );
            CREATE TABLE IF NOT EXISTS tax_layers (
                id INTEGER PRIMARY KEY,
                from_ INTEGER,
                to_ INTEGER,
                rate REAL,
                tax_id INTEGER,
                FOREIGN KEY(tax_id) REFERENCES taxes(id)
            );
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                key TEXT UNIQUE NOT NULL,
                value TEXT
            )
            """
        )
        self.conn.commit()
        self.cursor.execute("SELECT * FROM taxes")
        results: list[dict] = self.cursor.fetchall()
        if not results:
            self.cursor.executescript(
                """
                INSERT INTO taxes (name, description) 
                VALUES ("Syrian Layers Tax", "Default taxes");
                INSERT INTO tax_layers (from_, to_, rate, tax_id) 
                VALUES (0, 279000, 0, 1),
                       (279001, 450000, 0.07, 1),
                       (450001, 650000, 0.09, 1),
                       (650001, 850000, 0.11, 1),
                       (850001, 1100000, 0.13, 1),
                       (1100001, 50000000, 0.15, 1);
                """
            )
            self.conn.commit()
