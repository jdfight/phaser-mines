
export class Minefield {
  constructor(width, height, total_mines)
  {
    this._cells = Array(height).fill().map(()=> Array(width))
    this._width = width
    this._height = height
    this._total_mines = total_mines
    this._isWon = false
    this._isBlown = false
    this._openCount = 0
    this._updated = []
    this.generate()
  }

  generate()
  {
    var {Cell} = require('./Cell')
    var {roll, newDie} = require('./Dice')
    var d100 = newDie(100)
    var dy = newDie(this._height)
    var dx = newDie(this._width)

    var placedMines = 0
    for (var y = 0; y < this._height; y++)
    {
      for (var x = 0; x < this._width; x++)
      {
        this._cells[y][x] = new Cell(x, y, false)
      }
    }

    while (placedMines < this._total_mines)
    {
      var cell = this._cells[roll(1, dy) - 1][roll(1, dx) - 1]
      if(!cell._mine)
      {
        cell._mine = true
        placedMines++
      }
    }
    this.placeNumbers()
    this.openRandomCell()
    //console.log(`Placed ${placedMines} Mines`)
    //this.print()
  }

  placeNumbers()
  {
    for (var y = 0; y < this._height; y++)
    {
      for (var x = 0; x < this._width; x++)
      {
        this.checkNeighbors(x, y)
      }
    }
  }

  clearUpdated()
  {
    this._updated = []
  }

  checkWin()
  {
    return this._isBlown ? false : this._openCount == (this._width * this._height) - this._total_mines
  }

  openRandomCell()
  {
    var cell = this.findRandomOpenCell()
    cell._open = true
    this._openCount++
    this.openEmptyNeighbors(cell._x, cell._y)
    this._updated.push(cell)
  }

  openEmptyNeighbors(x,y)
  {
    var checky = y - 1;
    var checkx = x - 1;

    for(var cy = checky; cy < checky + 3; cy++)
    {
      if(cy > -1 && cy < this._height)
      {
        for (var cx = checkx; cx < checkx + 3; cx++)
        {
          if(cx > -1 && cx < this._width)
          {
            if(!this._cells[cy][cx]._mine && !this._cells[cy][cx]._open)
            {
              if(this._cells[cy][cx]._num == 0)
              {
                this.openCell(cx, cy)
                this.openEmptyNeighbors(cx, cy)
              //  this._updated.push(this._cells[cy][cx])
              }
              else
              {
                this.openCell(cx,cy);
              //  this._updated.push(this._cells[cy][cx])
              }
            }
          }
        }
      }
    }
  }

  openCell(x, y)
  {
    if(!this._isBlown && !this.checkWin())
    {
      this._cells[y][x]._open = true;
      this._updated.push(this._cells[y][x])
      if(this._cells[y][x]._mine == true)
      {
        this._isBlown = true
        //console.log("BLOWN:")
      }
      else
      {
        this._openCount++
      }
    }
  }

  findRandomOpenCell()
  {
    var {roll, newDie} = require('./Dice')
    var dy = newDie(this._height)
    var dx = newDie(this._width)
    var foundCell = false
    var cell = this._cells[0][0]

    while(!foundCell)
    {
      cell = this._cells[roll(1,dy) - 1][roll(1,dx) - 1];
      if(cell._num == 0 && !cell._mine)
      {
         foundCell = true
      }
    }
    return cell
  }

  checkNeighbors(x,y)
  {
    var cell = this._cells[y][x]
    var num = 0
    if(!cell._mine)
    {
      var checky = y - 1;
      var checkx = x - 1;

      for(var cy = checky; cy < checky + 3; cy++)
      {
        for (var cx = checkx; cx < checkx + 3; cx++)
        {
          if(cy > -1 && cy < this._height && cx > -1 && cx < this._width)
          {
            if(this._cells[cy][cx]._mine)
            {
              num++
            }
          }
        }
      }
      cell._num = num;
    }
  }

  getCell(x, y)
  {
    if(x > -1 && x < this._width && y > -1 && y < _height)
    {
      return this._cells[y][x]
    }
    return null
  }

  print()
  {
    var result = ""
    for (var y = 0; y < this._height; y++)
    {
      for (var x = 0; x < this._width; x++)
      {
        if(this._cells[y][x]._mine)
        {
          result += this._cells[y][x]._open ? ' * ' : ' . '
        }
        else
        {
          var num = this._cells[y][x]._num;
          if(this._cells[y][x]._open)
          {
            result += this._cells[y][x]._num > 0 ? ` ${num} ` : "   ";
          }
          else
          {
            result += ' . '
          }
        }
      }
      result += '\n'
    }
    console.log(result)
  }
}
