
export class CellView extends Phaser.Sprite
{
  constructor(game, x, y, cell, mines, callback)
  {
    super()
    Phaser.Sprite.call(this, game, x, y, 'mine-tiles', 1)
    game.add.existing(this)
    this.inputEnabled = true
    this.input.pixelPerfectClick = true;
    this.events.onInputDown.add(this.clicked, this)
    this.cell = cell
    this.minefield = mines
    this.state = game
    this.callback = callback
    //this.scale.set(2,2)
    this.width = 40
    this.height = 40
    this.isFlagged = false
    this.isActive = false
    if(cell._open)
    {
      this.open()
    }
    this.isActive = true
    return this
  }

  open()
  {
    if(this.minefield._isBlown || this.state.isWon) return;

    if(this.frame != 0 && this.cell._mine)
    {
      //var mine = this.game.add.sprite(this.x, this.y, 'mine-tiles', 4)
    	var explo = this.state.add.sprite(this.x, this.y, 'exploBig', 0)
     	explo.animations.add('explode', [0,1,2,3,4,5,6,7,8,9,10,11,12,13], 24, false)
     	explo.animations.play('explode')
      this.frame = 2
      this.state.setMessage("Boom!")
      this.state.shake()
    }
    else
    {
      if(this.isActive && this.frame != 0)
      {
        var smoke = this.state.add.sprite(this.x, this.y, 'smoke', 0)
        smoke.width = 40
        smoke.height = 40
        smoke.animations.add('puff', [0,1,2,3,4,5,6,7,8], Math.round(Math.random() * (30-12+1)+12), false)
        smoke.animations.play('puff')
      }
      this.frame = 0
      if(this.cell._num > 0)
      {
        var style = { font: "24px Arial", fill: "#00ff44", align: "center" };
        var text = this.state.add.text(this.x+15, this.y+6, `${this.cell._num}`, style);
      }
    }
  }

  close()
  {
    this.frame = 1
  }

  clicked(sprite)
  {
      if(this.state.game.input.activePointer.rightButton.isDown)
      {
        if(!this.isFlagged && !this.cell._open)
        {
          this.flag = this.game.add.sprite(this.x, this.y, 'flag')
          //this.flag.scale.set(1.5,1.5)
          this.flag.width = this.width
          this.flag.height = this.height
          this.isFlagged = true
          this.state.incFlag(1)
        }
        else
        {
          this.flag.pendingDestroy = true
          this.isFlagged = false
          this.state.incFlag(-1)
        }
      }
      else if (!this.isFlagged)
      {
        this.clicks += 1
        this.open()
        this.minefield.openCell(this.cell._x, this.cell._y)

        if(this.cell._num == 0)
        {
          this.minefield.openEmptyNeighbors(this.cell._x, this.cell._y)
        }
        this.callback(this.state)
      }
  }
}
