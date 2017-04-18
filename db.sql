/* 
An item is stored in a item slot. 
There can be more than one 'itemA', but only one in each slot, therefore:
Articles with same name can be found at different slots. 
*/
CREATE TABLE items (
ID INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
articleName VARCHAR(30),
xCoord INT(5),
yCoord INT(5)
);

/* 
A slot can be occupied or not, to see where to put new items.
These slots are predetermined, with a set width and depth in which where we can find an item.
As discussed in a meeting, the size of the package must fit the slot, 
and will then be placed in the middle of the slot.
*/

CREATE TABLE itemSlot (
xCoord INT(5),
yCoord INT(5),
slotTaken BOOLEAN,
PRIMARY KEY(xCoord,yCoord);
);

/*
Example of how a new item is stored:
SELECT * FROM itemSlot WHERE slotTaken = FALSE;
From that list we can:
INSERT INTO itemSlot (xCoord,yCoord,TRUE);
INSERT INTO items (articleName, xCoord, yCoord);

Example of how an item is retrieved from storage and removed from database
SELECT * FROM items where articleName = ?;
Take one of these, and send the robot to that slot
UPDATE itemSLOT SET slotTaken = FALSE WHERE xCoord = ? AND yCoord = ?;
DELETE FROM items WHERE xCoord = ? AND yCoord = ?;
*/