CC = g++
CFLAGS = -std=c++14

all:
	make apriori
	make charm

apriori: apriori.cpp
	$(CC) $(CFLAGS) $< -o $@.exe

charm: charm.cpp
	$(CC) $(CFLAGS) $< -o $@.exe

clean:
	rm -f apriori.exe charm.exe

