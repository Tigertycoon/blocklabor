-- M1-C Beispiel: Hello World drucken
-- Voraussetzung: angeschlossener Printer mit Papier und Black Dye

local printer = peripheral.find("printer")
if not printer then
  print("Kein Printer gefunden.")
  return
end

if printer.getPaperLevel() <= 0 then
  print("Kein Papier im Printer.")
  return
end

if printer.getBlack DyeLevel() <= 0 then
  print("Keine Black Dye im Printer.")
  return
end

if not printer.newPage() then
  print("Konnte keine neue Seite starten.")
  return
end

printer.setPageTitle("M1 Hello World")
printer.setCursorPos(1, 1)
printer.write("Hello World")
printer.setCursorPos(1, 3)
printer.write("TUMO Learn with Minecraft")
printer.endPage()

print("Gedruckt. Nimm die Seite aus dem Printer und gib sie in der Quest ab.")
