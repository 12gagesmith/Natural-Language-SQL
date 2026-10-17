import os
import sqlite3
from pathlib import Path

# By default, cards.db is created beside this script.
# Set CARDS_DB_PATH to choose a different location.
DB_PATH = Path(
    os.environ.get("CARDS_DB_PATH", Path(__file__).with_name("cards.db"))
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS player (
    id         INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS stats (
    player_id INTEGER PRIMARY KEY
        REFERENCES player(id) ON DELETE CASCADE,
    wins      INTEGER NOT NULL DEFAULT 0 CHECK (wins >= 0),
    losses    INTEGER NOT NULL DEFAULT 0 CHECK (losses >= 0)
);

CREATE TABLE IF NOT EXISTS attack (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    cost        INTEGER NOT NULL DEFAULT 0 CHECK (damage >= 0),
    damage      INTEGER NOT NULL DEFAULT 0 CHECK (damage >= 0)
);

CREATE TABLE IF NOT EXISTS card (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    hp          INTEGER NOT NULL CHECK (hp >= 0),
    attack_1_id INTEGER REFERENCES attack(id),
    attack_2_id INTEGER REFERENCES attack(id)
);

CREATE TABLE IF NOT EXISTS deck (
    id       INTEGER PRIMARY KEY,
    name     TEXT NOT NULL,
    owner_id INTEGER NOT NULL
        REFERENCES player(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS player_card (
    player_id      INTEGER NOT NULL
        REFERENCES player(id) ON DELETE CASCADE,
    card_id        INTEGER NOT NULL
        REFERENCES card(id) ON DELETE CASCADE,
    quantity_owned INTEGER NOT NULL DEFAULT 1
        CHECK (quantity_owned >= 0),
    PRIMARY KEY (player_id, card_id)
);

CREATE TABLE IF NOT EXISTS deck_cards (
    deck_id          INTEGER NOT NULL
        REFERENCES deck(id) ON DELETE CASCADE,
    card_id          INTEGER NOT NULL
        REFERENCES card(id) ON DELETE CASCADE,
    quantity_in_deck INTEGER NOT NULL DEFAULT 1
        CHECK (quantity_in_deck > 0),
    PRIMARY KEY (deck_id, card_id)
);
"""

# Fixed example IDs keep the relationships easy to follow.
# INSERT OR IGNORE makes this safe to run again without duplicating the examples.
DUMMY_DATA = [
    (
        "INSERT OR IGNORE INTO player (id, first_name, last_name, email) "
        "VALUES (?, ?, ?, ?)",
        [
            (1, "Ada", "Lovelace", "ada@example.com"),
            (2, "Alan", "Turing", "alan@example.com"),
        ],
    ),
    (
        "INSERT OR IGNORE INTO stats (player_id, wins, losses) VALUES (?, ?, ?)",
        [(1, 5, 2), (2, 3, 4)],
    ),
    (
        """
        INSERT OR IGNORE INTO attack (id, name, description, cost, damage)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (1, "Spark", "A quick electric strike", 1, 20),
            (2, "Thunderclap", "A powerful electric blast", 3, 50),
            (3, "Water Jet", "A focused stream of water", 1, 25),
            (4, "Tidal Wave", "A crashing wave", 3, 55),
        ],
    ),
    (
        """
        INSERT OR IGNORE INTO card (id, name, hp, attack_1_id, attack_2_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (1, "Volt Fox", 60, 1, 2),
            (2, "River Turtle", 80, 3, 4),
            (3, "Little Spark", 40, 1, None),
            (4, "Wave Sprite", 50, 3, None),
        ],
    ),
    (
        "INSERT OR IGNORE INTO deck (id, name, owner_id) VALUES (?, ?, ?)",
        [(1, "Electric Team", 1), (2, "Water Team", 2)],
    ),
    (
        """
        INSERT OR IGNORE INTO player_card (player_id, card_id, quantity_owned)
        VALUES (?, ?, ?)
        """,
        [(1, 1, 2), (1, 2, 1), (1, 3, 3), (2, 2, 2), (2, 4, 4)],
    ),
    (
        """
        INSERT OR IGNORE INTO deck_cards (deck_id, card_id, quantity_in_deck)
        VALUES (?, ?, ?)
        """,
        [(1, 1, 2), (1, 3, 2), (2, 2, 2), (2, 4, 2)],
    ),
]


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        # SQLite requires this to be enabled separately for each connection.
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SCHEMA)

        for sql, rows in DUMMY_DATA:
            conn.executemany(sql, rows)

        # Show a quick summary so you can see that setup and seeding worked.
        counts = {}
        for table in (
            "player",
            "stats",
            "attack",
            "card",
            "deck",
            "player_card",
            "deck_cards",
        ):
            counts[table] = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

    print(f"Database ready: {DB_PATH}")
    print("Rows in each table:")
    for table, count in counts.items():
        print(f"  {table}: {count}")


if __name__ == "__main__":
    main()
