# Stringa offuscata
offuscata = (
    "\50\51\40\75\76\40\173\40if\40\50fla\147.\166alue\40\75\75\75\40\42fla\147\173\152\123f\52\143\153\13715n7\1374\137\107r34\124\137\1674\131\137\1640\1370\142fus\1434\1643\13768f86127\175\42\51\40\173\40\167in\50\51\40\175\40else\40\173\40l\157\157se\50\51\40\175\40\175"
)

# Decodifica delle sequenze ottali
decodificata = offuscata.encode().decode('unicode_escape')
print(decodificata)
