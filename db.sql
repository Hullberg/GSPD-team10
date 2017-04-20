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
INSERT INTO itemSlot VALUES (x,y,FALSE);
INSERT INTO items (articleName, xCoord, yCoord) VALUES (artName,xCoord,yCoord);

Example of how an item is retrieved from storage and removed from database
SELECT * FROM items where articleName = ?;
Take one of these, and send the robot to that slot
UPDATE itemSLOT SET slotTaken = FALSE WHERE xCoord = ? AND yCoord = ?;
DELETE FROM items WHERE xCoord = ? AND yCoord = ?;
*/


/* Each slot is 50x50, so the center of the bottom left slot is (25,25). */
/* The warehouse must be atleast 150x150 in cm, represented as ints */
/* Robot queue is at (x=25, y=50*(i+1)-25)
(25,25)
(25,75)
(25,125)
etc. etc.
The robot in starting area will be at (x=75, y=25)
*/
INSERT INTO itemSlot VALUES (125,75,FALSE); /* Bottom left item slot */
INSERT INTO itemSlot VALUES (125,125,FALSE);
INSERT INTO itemSlot VALUES (125,175,FALSE);
INSERT INTO itemSlot VALUES (225,75,FALSE); /* Second column, with an empty column so the robot can move there */
INSERT INTO itemSlot VALUES (225,125,FALSE);
INSERT INTO itemSlot VALUES (225,175,FALSE);
INSERT INTO itemSlot VALUES (325,75,FALSE);
INSERT INTO itemSlot VALUES (325,125,FALSE);
INSERT INTO itemSlot VALUES (325,175,FALSE); /* And so on... */
/*
Every second column is empty, in order to let the robots "run down an aisle".
So every "itemslot-row" is: (start at 75, end at 75 from MAX(Y))
INSERT INTO itemSLOT VALUES (125,75,FALSE);
INSERT INTO itemSLOT VALUES (125,125,FALSE);
INSERT INTO itemSLOT VALUES (125,175,FALSE);

Pattern: X starts at column-nr * 100 + 25.
Y goes from 75 to 75 from the top of the warehouse.
*/