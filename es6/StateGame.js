export class StateGame extends Phaser.State
{
  constructor()
  {
    super()

  }

  preload ()
  {
    var { Minefield } = require('./Minefield')
    this.mines = new Minefield(16, 16, 40)
    this.total_mines = 40;
    this.cells = []
    this.flagged = 0

    this.game.load.spritesheet('mine-tiles', './assets/textures/mine-tiles.png', 20, 20)
    this.game.load.spritesheet('exploBig', './assets/textures/exploBig.png', 40, 40)

    this.game.stage.smoothed = false;
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
      state.setMessage('You Won!')
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
          var cv = new CellView(this, x * 40 + 10, y * 40 + 10, cell, this.mines, this.clearUpdates)
          this.cells.push(cv)
        }
        else
        {
          var cv = new CellView(this, x * 40 + 10, y * 40 + 10, cell, this.mines, this.clearUpdates)
          this.cells.push(cv)
        }
      }
    }

    this.textstyle = { font: "32px Arial", fill: "#00ff44", align: "center" }
    this.msgtext = this.game.add.text(800, 6, "10", this.textstyle)
    this.btnReset = this.game.add.button(800, 300, 'mine-tiles', this.onResetClick, this, 8, 6, 7)

    this.textresetstyle = { font: "24px Arial", fill: "#000000", align: "center" }
    this.resettext = this.game.add.text(810, 302, "Reset", this.textresetstyle)

    this.btnReset.width = 80
    this.btnReset.height = 32
  }

  setMessage(msg) {
    this.msgtext.setText(msg)
  }

  incFlag(amt)
  {
    this.flagged += amt
    this.setMessage(`${this.total_mines - this.flagged}`)
  }

  onResetClick()
  {
    console.log("On Reset")
    this.game.state.start('StateReset')
  }
}
