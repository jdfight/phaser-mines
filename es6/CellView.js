
export class CellView extends Phaser.Sprite
{
  constructor(game, x, y, cell, mines, callback)
  {
    super();
    Phaser.Sprite.call(this, game, x, y, 'mine-tiles', 1)
    game.add.existing(this)
    this.inputEnabled = true
    this.input.pixelPerfectClick = true;
    this.events.onInputDown.add(this.clicked, this)
    this.cell = cell
    this.minefield = mines
    this.state = game
    this.callback = callback

    if(cell._open)
    {
      this.open()
    }
    return this
  }

  open()
  {
    if(this.minefield._isBlown || this.minefield.checkWin()) return;

    if(this.frame != 0 && this.cell._mine)
    {
      //var mine = this.game.add.sprite(this.x, this.y, 'mine-tiles', 4)
    	var explo = this.state.add.sprite(this.x - 10, this.y - 10, 'exploBig', 0)
     	explo.animations.add('explode', [0,1,2,3,4,5,6,7,8,9,10,11,12,13], 24, false)
     	explo.animations.play('explode')
      this.frame = 2
    }
    else
    {
      this.frame = 0
      if(this.cell._num > 0)
      {
        var style = { font: "12px Arial", fill: "#00ff44", align: "center" };
        var text = this.state.add.text(this.x+7, this.y+2, `${this.cell._num}`, style);
      }
    }
  }

  close()
  {
    this.frame = 1
  }

  clicked(sprite)
  {
      this.open()
      this.minefield.openCell(this.cell._x, this.cell._y)

      if(this.cell._num == 0)
      {
        this.minefield.openEmptyNeighbors(this.cell._x, this.cell._y)
      }
      this.callback(this.state)
  }
}
