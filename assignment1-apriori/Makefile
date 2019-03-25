CC = g++
CFLAGS = -std=c++14

all:
	make apriori
	make charm

apriori: apriori.o
	$(CC) $(CFLAGS) $^ -o $@.exe

apriori.o: apriori.cpp
	$(CC) $(CFLAGS) -c $<

charm: charm.o
	$(CC) $(CFLAGS) $< -o $@.exe

charm.o: charm.cpp
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f *.exe *.o

