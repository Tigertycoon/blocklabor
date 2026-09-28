-- M1-D Beispiel: Turtle Basics
-- Baut einen kleinen Tunnel und kehrt zurueck.

local distance = 16

if turtle.getFuelLevel() ~= "unlimited" and turtle.getFuelLevel() < (distance * 2 + 4) then
  print("Zu wenig Fuel. Lege Kohle in Slot 1 und nutze turtle.refuel().")
  return
end

for i = 1, distance do
  if turtle.detect() then turtle.dig() end
  while not turtle.forward() do
    if turtle.detect() then
      turtle.dig()
    else
      sleep(0.2)
    end
  end
end

for i = 1, distance do
  turtle.back()
end

print("Turtle-Test fertig.")
