-- M1-E Beispiel: Turtle Loops + Mini-Quarry
-- Grabt ein kleines Raster (Breite x Laenge).

local width = 4
local length = 16

local function digForward()
  if turtle.detect() then turtle.dig() end
  while not turtle.forward() do
    if turtle.detect() then
      turtle.dig()
    else
      sleep(0.2)
    end
  end
end

local estimatedMoves = (width * (length - 1)) + (width - 1) + 20
if turtle.getFuelLevel() ~= "unlimited" and turtle.getFuelLevel() < estimatedMoves then
  print("Zu wenig Fuel fuer den Quarry-Lauf.")
  return
end

for row = 1, width do
  for step = 1, length - 1 do
    digForward()
  end

  if row < width then
    if row % 2 == 1 then
      turtle.turnRight()
      digForward()
      turtle.turnRight()
    else
      turtle.turnLeft()
      digForward()
      turtle.turnLeft()
    end
  end
end

print("Mini-Quarry Lauf fertig.")
