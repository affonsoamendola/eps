source = $(wildcard *.c)
bin = ep1_buffon

CC = gcc
LIBRARY = -lm #-lSDL2 -lSDL2_image 
CFLAGS = -O2
INCLUDE = #../ff-stb/C/

$(bin) : $(source) 
	$(CC) $(CFLAGS) -o$(bin) $(source) $(LIBRARY)

.PHONY: clean run

clean:
	rm $(bin)
	
run:
	./$(bin)