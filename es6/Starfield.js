export class Starfield extends Phaser.Sprite
{


  constructor(game, x, y)
  {
    super()
    Phaser.Sprite.call(this, game, x, y, 'star2', 1)
    game.add.existing(this)
    this.distance = 300
    this.speed = 3

    this.max = 100
    this.xx = []
    this.yy = []
    this.zz = []

    this.star = game.make.sprite(0, 0, 'star2')
//    this.texture = game.add.renderTexture(this.game.width, this.game.height, 'texture');
    this.texture = game.add.renderTexture(this.game.width, this.game.height, 'texture')

    for (var i = 0; i < this.max; i++)
    {
        this.xx[i] = Math.floor(Math.random() * game.width) - (game.width/2)
        this.yy[i] = Math.floor(Math.random() * game.height) - (game.height/2)
        this.zz[i] = Math.floor(Math.random() * 1700) - 100
    }
  }

  update()
  {
    this.texture.clear()
    for (var i = 0; i < this.max; i++)
    {
        var perspective = this.distance / (this.distance - this.zz[i])
        var sx = this.game.world.centerX + this.xx[i] * perspective
        var sy = this.game.world.centerY + this.yy[i] * perspective

        this.zz[i] += this.speed

        if (this.zz[i] > 300)
        {
            this.zz[i] -= 600
        }
        this.texture.renderXY(this.star, sx, sy)
    }
  }
}
