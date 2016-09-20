export class StateReset extends Phaser.State
{
  constructor()
  {
    super()
  }

  init(w, h, m)
  {
    this.width = w
    this.height = h
    this.mines = m
  }
  create()
  {
    this.game.state.start('StateGame', true, false, this.width, this.height, this.mines)
  }
}
