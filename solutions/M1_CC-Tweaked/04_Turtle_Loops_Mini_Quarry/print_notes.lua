-- M1-E Beispiel: Notizseite fuer Quest drucken
-- Druckt eine kurze Projekt-Notiz.

local printer = peripheral.find("printer")
if not printer then
  print("Kein Printer gefunden.")
  return
end

if printer.getPaperLevel() <= 0 or printer.getBlack DyeLevel() <= 0 then
  print("Printer braucht Papier und Black Dye.")
  return
end

if not printer.newPage() then
  print("Konnte keine neue Seite starten.")
  return
end

printer.setPageTitle("M1-E Notiz")
printer.setCursorPos(1, 1)
printer.write("Mini-Quarry getestet.")
printer.setCursorPos(1, 2)
printer.write("Loop laeuft stabil.")
printer.endPage()

print("Notizseite gedruckt.")
