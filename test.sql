UPDATE index_items
SET item_id = 100
WHERE item_label = 'pandas';


SELECT * FROM commands;
SELECT * FROM `commands` WHERE item_id = 99;
SELECT MAX(command_id) FROM commands;

SELECT * FROM index_items;

SELECT * FROM examples;

SELECT * FROM commands_examples;

DELETE FROM index_items WHERE item_id = 2;

PRAGMA foreign_keys;

PRAGMA foreign_keys = ON;

SELECT * FROM links;

INSERT INTO links (link_label, link_href, link_type, command_id)
VALUES ('Official documentation',
       'https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html',
       'code',
       99);