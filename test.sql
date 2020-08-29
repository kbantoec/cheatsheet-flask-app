UPDATE index_items
SET item_id = 100
WHERE item_label = 'pandas';

SELECT * FROM commands;

SELECT * FROM index_items;

SELECT * FROM examples;

SELECT * FROM commands_examples;

DELETE FROM index_items WHERE item_id = 2;

PRAGMA foreign_keys;

PRAGMA foreign_keys = ON;