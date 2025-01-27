# Nome del programma di output
TARGET = PROVA

# Compilatore da utilizzare
CC = gcc

# Opzioni di compilazione
CFLAGS = -Wall -Wextra

# File sorgente
SRCS = impldefined.c

# Regola per la compilazione
$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRCS)

# Regola per pulire i file intermedi e l'eseguibile
clean:
	rm -f $(TARGET)

# Imposta la regola 'all' come predefinita
all: $(TARGET)

.PHONY: clean
