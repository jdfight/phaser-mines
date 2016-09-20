export class StateGame extends Phaser.State
{
  constructor()
  {
    super()

  }
  init(w, h, m)
  {
    this.gridw = w
    this.gridh = h
    this.total_mines = m
    this.isWon = false
  }

  preload ()
  {
    var { Minefield } = require('./Minefield')

    this.mines = new Minefield(this.gridw, this.gridh, this.total_mines)  // 16 16 40 = intermediate/hard
    this.cells = []
    this.flagged = 0

    this.game.load.spritesheet('mine-tiles', './assets/textures/mine-tiles2.png', 64, 64)
    this.game.load.spritesheet('exploBig', './assets/textures/exploBig.png', 40, 40)
    this.game.load.image('back', './assets/textures/bg-space1.jpg')
    this.game.load.image('star2', './assets/textures/star2.png')
    this.game.load.image('flag', './assets/textures/flag.png')
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
      state.setMessage('You\nWon!')
      state.isWon = true
    }
  }

  create () {
    //var { Starfield } = require('./Starfield')
    this.game.stage.backgroundColor = '#00030c'
    this.game.add.sprite(0,0,'back')
    //this.stars = new Starfield(this.game, 0,0);
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

    this.textstyle = { font: "24px Arial", fill: "#ffffff", align: "center" }
    this.msgtext = this.game.add.text(980, 6, `${this.total_mines}`, this.textstyle)

    this.ngstyle = { font: "24px Arial", fill: "#ffffff", align: "center" }
    this.newgametext = this.game.add.text(980, 220, "New\nGame:", this.textstyle)

    this.btnEasy = this.game.add.button(980, 300, 'mine-tiles', this.onEasyClick, this, 6, 4, 5)
    this.btnMed = this.game.add.button(980, 340, 'mine-tiles', this.onMedClick, this, 6, 4, 5)
    this.btnHard = this.game.add.button(980, 380, 'mine-tiles', this.onHardClick, this, 6, 4, 5)

    this.textresetstyle = { font: "24px Arial", fill: "#000000", align: "center" }
    this.easytext = this.game.add.text(990, 302, "Easy", this.textresetstyle)
    this.medtext = this.game.add.text(990, 342, "Med", this.textresetstyle)
    this.hardtext = this.game.add.text(990, 382, "Hard", this.textresetstyle)

    this.btnEasy.width = 80
    this.btnEasy.height = 32
    this.btnMed.width = 80
    this.btnMed.height = 32
    this.btnHard.width = 80
    this.btnHard.height = 32
  }

  setMessage(msg) {
    this.msgtext.setText(msg)
  }

  incFlag(amt)
  {
    this.flagged += amt
    this.setMessage(`${this.total_mines - this.flagged}`)
  }

  onEasyClick()
  {
    this.Reset(0)
  }
  onMedClick()
  {
    this.Reset(1)
  }
  onHardClick()
  {
    this.Reset(2)
  }
  Reset(diff)
  {
    console.log("On Reset")
    switch (diff)
    {
      case 1:
        this.game.state.start('StateReset', true, false, 16,16,40)
        break
      case 2:
        this.game.state.start('StateReset', true, false, 24,24,100)
        break
      default:
        this.game.state.start('StateReset', true, false, 10,10,10)
        break
    }
  }

}
