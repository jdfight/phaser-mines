export class Cell {
    constructor(x, y, mine)
    {
	    this._x = x;
      this._y = y;
      this._num = 0
	    this._mine = mine
      this._open = false;
    }
}
