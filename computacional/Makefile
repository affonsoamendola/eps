source = $(wildcard *.c)
bin = ep1_buffon

CC = gcc
LIBRARY = #-lSDL2 -lSDL2_image -lm
CFLAGS = -g
INCLUDE = #../ff-stb/C/

$(bin) : $(source) 
	$(CC) $(CFLAGS) -o$(bin) $(source) $(LIBRARY)

.PHONY: clean run

clean:
	rm $(bin)
	
run:
	./$(bin)