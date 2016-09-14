export class StateGame extends Phaser.State
{
  constructor()
  {
    super()
    var { Minefield } = require('./Minefield')
    this.mines = new Minefield(10, 10, 10)
    this.cells = []
  }

  preload ()
  {
    this.game.load.spritesheet('mine-tiles', './assets/textures/mine-tiles.png', 20, 20)
    this.game.load.spritesheet('exploBig', './assets/textures/exploBig.png', 40, 40)
  }

  clearUpdates(state)
  {
    console.log("clearUpdates()")
    state.mines._updated.forEach(function(c)
    {
      for(var i = 0; i < state.cells.length; i++)
      {
        if(c._x == state.cells[i].cell._x && c._y == state.cells[i].cell._y)
        {
          if(c._open)
          {
            state.cells[i].open()
          }
        }
      }
    });
    state.mines.clearUpdated()
    if(state.mines.checkWin() == true)
    {
      console.log("You Won")
    }
  }

  create () {
    this.game.stage.backgroundColor = '#000000'
    var { CellView } = require('./CellView')
    // The player and its settings

    for(var y = 0; y < this.mines._cells.length; y++)
    {
      for (var x = 0; x < this.mines._cells.length; x++)
      {
        var cell = this.mines._cells[y][x]
        if(cell._num == 0 || cell._mine)
        {
          var cv = new CellView(this, x * 20, y * 20, cell, this.mines, this.clearUpdates)
          this.cells.push(cv)
        }
        else
        {
          var cv = new CellView(this, x * 20, y * 20, cell, this.mines, this.clearUpdates)
          this.cells.push(cv)
        }
      }
    }
  }

}
