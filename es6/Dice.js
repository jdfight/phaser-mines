
export function newDie(sides) {
  return () => {
    return Math.round(Math.random() * (sides - 1) + 1)
  }
}

export function roll(times, die)
{
  var result = 0;
  for (var i = 0; i < times; i++)
  {
    result += die()
  }
  return result;
}
