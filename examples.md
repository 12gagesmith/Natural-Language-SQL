# Examples of AI Natural Language to SQL
```
USER: Which card has the attack that does the most damage?
QUERY:  WITH card_attacks AS (
  SELECT c.name AS card_name, a.name AS attack_name, a.damage
  FROM card AS c
  JOIN attack AS a ON a.id = c.attack_1_id
  UNION ALL
  SELECT c.name AS card_name, a.name AS attack_name, a.damage
  FROM card AS c
  JOIN attack AS a ON a.id = c.attack_2_id
)
SELECT card_name, attack_name, damage
FROM card_attacks
WHERE damage = (SELECT MAX(damage) FROM card_attacks);
ASSISTANT: River Turtle has the highest-damage attack: Tidal Wave, which does 55 damage.
```
```
USER: How many copies of River Turtle does Ada own?
QUERY:  SELECT COALESCE(SUM(pc.quantity_owned), 0) AS copies_owned
FROM player_card AS pc
JOIN player AS p ON p.id = pc.player_id
JOIN card AS c ON c.id = pc.card_id
WHERE p.first_name = 'Ada'
  AND c.name = 'River Turtle';
ASSISTANT: Ada owns 1 copy of River Turtle.
```
```
USER: Which attack has the best damage-to-cost ratio?
QUERY:  SELECT name, damage * 1.0 / cost AS damage_to_cost_ratio
FROM attack
WHERE cost > 0
  AND damage * 1.0 / cost = (
    SELECT MAX(damage * 1.0 / cost)
    FROM attack
    WHERE cost > 0
  );
ASSISTANT: Water Jet has the best damage-to-cost ratio, at 25.0 damage per cost unit.
```
```
USER: How many decks use the Little Spark card?
QUERY:  SELECT COUNT(DISTINCT dc.deck_id)
FROM deck_cards AS dc
JOIN card AS c ON c.id = dc.card_id
WHERE c.name = 'Little Spark';
ASSISTANT: 1 deck uses the Little Spark card.
```
```
USER: Who has won the most games?
QUERY:  SELECT p.first_name, p.last_name, s.wins
FROM player AS p
JOIN stats AS s ON s.player_id = p.id
WHERE s.wins = (SELECT MAX(wins) FROM stats);
ASSISTANT: Ada Lovelace has won the most games, with 5 wins.
```
```
USER: Who uses cards related to electricity in their decks?
QUERY:  SELECT DISTINCT p.first_name, p.last_name
FROM player AS p
JOIN deck AS d ON d.owner_id = p.id
JOIN deck_cards AS dc ON dc.deck_id = d.id
JOIN card AS c ON c.id = dc.card_id
LEFT JOIN attack AS a1 ON a1.id = c.attack_1_id
LEFT JOIN attack AS a2 ON a2.id = c.attack_2_id
WHERE LOWER(
    COALESCE(c.name, '') || ' ' ||
    COALESCE(a1.name, '') || ' ' || COALESCE(a1.description, '') || ' ' ||
    COALESCE(a2.name, '') || ' ' || COALESCE(a2.description, '')
) LIKE '%electric%'
OR LOWER(
    COALESCE(c.name, '') || ' ' ||
    COALESCE(a1.name, '') || ' ' || COALESCE(a1.description, '') || ' ' ||
    COALESCE(a2.name, '') || ' ' || COALESCE(a2.description, '')
) LIKE '%lightning%'
OR LOWER(
    COALESCE(c.name, '') || ' ' ||
    COALESCE(a1.name, '') || ' ' || COALESCE(a1.description, '') || ' ' ||
    COALESCE(a2.name, '') || ' ' || COALESCE(a2.description, '')
) LIKE '%thunder%'
OR LOWER(
    COALESCE(c.name, '') || ' ' ||
    COALESCE(a1.name, '') || ' ' || COALESCE(a1.description, '') || ' ' ||
    COALESCE(a2.name, '') || ' ' || COALESCE(a2.description, '')
) LIKE '%volt%'
OR LOWER(
    COALESCE(c.name, '') || ' ' ||
    COALESCE(a1.name, '') || ' ' || COALESCE(a1.description, '') || ' ' ||
    COALESCE(a2.name, '') || ' ' || COALESCE(a2.description, '')
) LIKE '%shock%'
OR LOWER(
    COALESCE(c.name, '') || ' ' ||
    COALESCE(a1.name, '') || ' ' || COALESCE(a1.description, '') || ' ' ||
    COALESCE(a2.name, '') || ' ' || COALESCE(a2.description, '')
) LIKE '%spark%'
OR LOWER(
    COALESCE(c.name, '') || ' ' ||
    COALESCE(a1.name, '') || ' ' || COALESCE(a1.description, '') || ' ' ||
    COALESCE(a2.name, '') || ' ' || COALESCE(a2.description, '')
) LIKE '%static%';
ASSISTANT: Ada Lovelace uses cards related to electricity in her deck.
```