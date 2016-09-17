export class StateReset extends Phaser.State
{
  constructor()
  {
    super()
  }

  create()
  {
    this.game.state.start('StateGame')
  }
}
